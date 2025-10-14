# app.py - API Backend for Resume Screener
import os
import csv
import json
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from parser import parse_resume
from llm_client import rate_candidate
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Use absolute path for CSV file in project root (parent of backend directory)
CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resumes.csv")
ALLOWED_EXT = {"pdf", "docx", "txt"}

print(f"DEBUG: CSV_PATH is set to: {CSV_PATH}")
print(f"DEBUG: UPLOAD_FOLDER is set to: {UPLOAD_FOLDER}")

def allowed_file(fn):
    return "." in fn and fn.rsplit(".",1)[1].lower() in ALLOWED_EXT

def write_csv_record(rec: dict):
    """Append record dict to resumes.csv (create header if not exists)."""
    fieldnames = ["id","filename","name","email","phone","skills","education","experience","text"]
    write_header = not os.path.exists(CSV_PATH)
    try:
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            if write_header:
                writer.writeheader()
            writer.writerow(rec)
            print(f"DEBUG: Successfully wrote record to CSV: {rec['id']}")
    except Exception as e:
        print(f"DEBUG: Error writing to CSV: {str(e)}")
        print(f"DEBUG: Record keys: {list(rec.keys())}")
        print(f"DEBUG: Expected fieldnames: {fieldnames}")
        raise

def read_all_records():
    """Read all from resumes.csv into list of dicts."""
    if not os.path.exists(CSV_PATH):
        print(f"DEBUG: CSV file does not exist at {CSV_PATH}")
        return []

    print(f"DEBUG: CSV file exists, reading from {CSV_PATH}")
    try:
        with open(CSV_PATH, 'r', encoding="utf-8") as f:
            content = f.read()
            print(f"DEBUG: CSV content length: {len(content)}")
            print(f"DEBUG: First 200 chars: {content[:200]}")

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            print(f"DEBUG: Parsed {len(rows)} rows")

            for i, row in enumerate(rows):
                print(f"DEBUG: Row {i}: {row}")
                if i >= 2:  # Only show first few rows
                    break

            return rows
    except Exception as e:
        print(f"DEBUG: Error reading CSV: {str(e)}")
        return []

def get_record_by_id(rec_id: str):
    recs = read_all_records()
    for rec in recs:
        if rec["id"] == rec_id:
            return rec
    return None

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Enable CORS for frontend communication
CORS(app, origins=["http://localhost:8501", "http://127.0.0.1:8501"])

# Response helper functions
def success_response(data=None, message="Success", code=200):
    response = {"success": True, "message": message}
    if data is not None:
        response["data"] = data
    return jsonify(response), code

def error_response(message="Error", code=400, error=None):
    response = {"success": False, "message": message}
    if error:
        response["error"] = str(error)
    return jsonify(response), code

@app.route("/")
def index():
    return success_response({"message": "Resume Screener API", "version": "2.0"})

@app.route("/upload", methods=["POST"])
def upload():
    try:
        print("DEBUG: Upload endpoint called")
        if "resume" not in request.files:
            return error_response("No file part in the request", 400)

        file = request.files["resume"]
        print(f"DEBUG: File received: {file.filename}")
        if file.filename == "":
            return error_response("No file selected", 400)

        if not file or not allowed_file(file.filename):
            return error_response(f"Invalid file type. Allowed: {', '.join(ALLOWED_EXT)}", 400)

        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        print(f"DEBUG: Saving file to: {path}")
        file.save(path)
        print(f"DEBUG: File saved successfully")

        ext = filename.rsplit(".", 1)[1].lower()
        print(f"DEBUG: File extension: {ext}")
        print(f"DEBUG: About to parse resume...")
        parsed = parse_resume(path, ext)
        print(f"DEBUG: Resume parsed successfully")
        print(f"DEBUG: Parsed keys: {list(parsed.keys())}")

        recs = read_all_records()
        new_id = str(len(recs) + 1)

        # Extract skills from skills_section (parser returns skills_section, not skills list)
        skills_section = parsed.get("skills_section") or ""
        # Convert skills_section text to a simple string (keep newlines as semicolons for CSV)
        skills_str = skills_section.replace("\n", "; ").strip()

        rec = {
            "id": new_id,
            "filename": filename,
            "name": parsed.get("name") or "",
            "email": parsed.get("email") or "",
            "phone": parsed.get("phone") or "",
            "skills": skills_str,
            "education": parsed.get("education") or "",
            "experience": parsed.get("experience") or "",
            "text": parsed.get("text") or "",
            "created_at": datetime.now().isoformat()
        }

        write_csv_record(rec)

        return success_response({
            "candidate": rec,
            "message": "Resume uploaded and parsed successfully"
        })

    except Exception as e:
        import traceback
        print(f"DEBUG: Upload exception: {str(e)}")
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        return error_response(f"Upload failed: {str(e)}", 500, e)

@app.route("/candidates")
def candidates():
    try:
        recs = read_all_records()
        print(f"DEBUG Backend: About to return {len(recs)} candidates")
        print(f"DEBUG Backend: First candidate: {recs[0] if recs else 'None'}")
        print(f"DEBUG Backend: First candidate type: {type(recs[0]) if recs else 'N/A'}")
        response_data = success_response(recs, f"Retrieved {len(recs)} candidates")
        print(f"DEBUG Backend: Response data: {response_data[0].get_json()}")
        return response_data
    except Exception as e:
        print(f"DEBUG Backend: Error: {str(e)}")
        return error_response(f"Failed to retrieve candidates: {str(e)}", 500, e)

@app.route("/candidate/<rec_id>")
def candidate(rec_id):
    try:
        rec = get_record_by_id(rec_id)
        if rec is None:
            return error_response(f"Candidate with ID {rec_id} not found", 404)

        skills = rec["skills"].split(";") if rec.get("skills") else []
        rec["skills_list"] = skills

        return success_response(rec, "Candidate retrieved successfully")
    except Exception as e:
        return error_response(f"Failed to retrieve candidate: {str(e)}", 500, e)

@app.route("/match", methods=["POST"])
def match():
    try:
        if not request.is_json:
            return error_response("Content-Type must be application/json", 400)

        data = request.get_json()
        if not data:
            return error_response("No JSON data provided", 400)

        job_desc = data.get("job_description", "").strip()
        if not job_desc:
            return error_response("Job description is required", 400)

        min_score = data.get("min_score", 0.0)

        recs = read_all_records()
        results = []

        for rec in recs:
            skills_section_text = rec.get("skills_section", "") or rec.get("text", "")[:2000]

            try:
                resp = rate_candidate(skills_section_text, job_desc)
                score = float(resp.get("score", 0.0))
                justification = resp.get("justification", resp.get("raw", ""))
                matches = resp.get("matches", [])
                recommendation = resp.get("recommendation", "")

                # Only include if score meets minimum threshold
                if score >= min_score:
                    results.append({
                        "candidate_id": rec["id"],
                        "candidate_name": rec.get("name") or rec.get("filename"),
                        "score": score,
                        "justification": justification,
                        "matches": matches,
                        "recommendation": recommendation,
                        "candidate_data": rec
                    })

            except Exception as e:
                # Include error cases with score 0
                results.append({
                    "candidate_id": rec["id"],
                    "candidate_name": rec.get("name") or rec.get("filename"),
                    "score": 0.0,
                    "justification": f"LLM error: {str(e)}",
                    "matches": [],
                    "recommendation": "",
                    "candidate_data": rec,
                    "error": str(e)
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return success_response({
            "job_description": job_desc,
            "results": results,
            "total_candidates": len(recs),
            "matched_candidates": len(results),
            "min_score": min_score,
            "timestamp": datetime.now().isoformat()
        }, f"Matched {len(results)} candidates against job description")

    except Exception as e:
        return error_response(f"Matching failed: {str(e)}", 500, e)

if __name__ == "__main__":
    app.run(debug=True)