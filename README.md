# Smart  Resume Screener 📄
#### ARIN BALYAN 22BAI10041
A comprehensive resume screening and candidate matching application that uses AI to automatically parse, analyze, and score resumes against job descriptions. Built with Flask backend API and Streamlit frontend for an intuitive user experience.

## 🚀 Features

- **Resume Parsing**: Extract information from PDF, DOCX, and TXT files
- **AI-Powered Matching**: Uses LLM (Groq API) to score candidates against job descriptions
- **Candidate Management**: Store and manage candidate information in CSV format
- **Modern UI**: Responsive Streamlit interface with dark theme
- **RESTful API**: Flask-based backend with CORS support
- **File Upload**: Secure file upload with validation
- **Analytics Dashboard**: View statistics and insights
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🏗️ Architecture

The application follows a modern client-server architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        Resume Screener                          │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (Streamlit)              │  Backend (Flask API)       │
│  ┌─────────────────────────┐       │  ┌─────────────────────┐   │
│  │   📱 User Interface     │◄──────┤  │   🌐 REST API       │   │
│  │   📊 Dashboard          │       │  │   📁 File Upload    │   │
│  │   📤 Upload Interface   │       │  │   🔍 Candidate Mgmt │   │
│  │   👥 Candidate Viewer    │       │  │   🤖 LLM Integration│   │
│  └─────────────────────────┘       │  └─────────────────────┘   │
│           │                        │           │               │
│           ▼                        │           ▼               │
│  ┌─────────────────────────┐       │  ┌─────────────────────┐   │
│  │   💾 Local Storage      │       │  │   📄 Resume Parser  │   │
│  │   CSV Export/Import     │       │  │   📊 Data Extractor │   │
│  └─────────────────────────┘       │  │   💾 CSV Database   │   │
│                                    │  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

```
User Upload → File Validation → Text Extraction → Section Parsing → LLM Analysis → Candidate Storage → Results Display
     ↓              ↓               ↓                ↓              ↓              ↓              ↓
   PDF/DOCX/    Security Check   PDFMiner/      Skills/Contact/  Groq API     CSV Storage   Streamlit
   TXT Files     (Werkzeug)      Docx libs      Education/Exp   llama-3.1     (resumes.csv)  Dashboard
```

### Backend (Flask API)
- **Location**: `backend/` directory
- **Purpose**: REST API for resume processing and candidate management
- **Technology Stack**:
  - Flask web framework with CORS support
  - PDFMiner.six for PDF text extraction
  - python-docx for Word document processing
  - Requests library for LLM API communication
  - CSV for data persistence
- **Key Files**:
  - `backend/app.py` - Main Flask application with API endpoints
  - `backend/parser.py` - Resume parsing and text extraction logic
  - `backend/llm_client.py` - Integration with Groq LLM API
  - `backend/requirements.txt` - Backend-specific dependencies

### Frontend (Streamlit)
- **Location**: `frontend/` directory
- **Purpose**: Modern web interface for user interaction
- **Technology Stack**:
  - Streamlit for reactive web interface
  - Custom CSS for dark theme styling
  - Session state management for navigation
  - RESTful API client for backend communication
- **Key Files**:
  - `frontend/app.py` - Main Streamlit application with UI components
  - `frontend/api_client.py` - API client for backend communication

## 📋 Prerequisites

- **Python**: 3.13 or higher (specified in `pyproject.toml`)
- **uv**: Fast Python package installer and resolver
- **Groq API Key**: For LLM-powered candidate scoring
- **Git**: For version control

## 🛠️ Installation

### 1. Install uv (Python Package Manager)

#### Windows
```powershell
# Download and install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### macOS/Linux
```bash
# Using curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

#### Alternative: Install from GitHub
```bash
# Clone the uv repository
git clone https://github.com/astral-sh/uv.git
cd uv
cargo install --path crates/uv
```

### 2. Clone the Repository
```bash
git clone <repository-url>
cd resumescan
```

### 3. Install Dependencies
```bash
# Install all project dependencies using uv
uv sync

# Alternative: Install from requirements files
uv pip install -r requirements.txt
uv pip install -r backend/requirements.txt
uv pip install -r frontend/requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Flask Secret Key (generate a secure random key)
SECRET_KEY=your-secret-key-here

# LLM API Configuration
LLM_API_KEY=your-groq-api-key-here
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
LLM_MODEL=llama-3.1-8b-instant

# Optional: Backend URL (if running on different port/host)
BACKEND_URL=http://localhost:5000
```

#### Getting a Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key to your `.env` file

## 🚀 Quick Start

### Start the Backend API
```bash
# From project root
uv run python backend/app.py

# Or using Python directly
python backend/app.py
```

The backend will start on `http://localhost:5000`

### Start the Frontend Interface
```bash
# Open new terminal and run
uv run streamlit run frontend/app.py

# Or using Python directly
streamlit run frontend/app.py
```

The frontend will start on `http://localhost:8501`

## 📖 Usage

### Uploading Resumes

1. **Access the Application**: Open `http://localhost:8501` in your browser
2. **Navigate to Upload**: Click "📤 Upload Resume" in the sidebar
3. **Select Files**: Upload PDF, DOCX, or TXT resume files
4. **Process**: Click "🚀 Process Resumes" to parse and store candidates

### Job Matching

1. **Go to Match Page**: Click "🎯 Match Jobs" in the sidebar
2. **Enter Job Description**: Paste the job requirements in the text area
3. **Set Criteria**: Adjust minimum score threshold (0.0 to 1.0)
4. **Find Matches**: Click "🔍 Find Matches" to get AI-powered results

### Viewing Candidates

1. **Browse Candidates**: Click "👥 Candidates" to view all processed resumes
2. **View Details**: Click "👁️ View Details" for comprehensive candidate information
3. **Quick Match**: Use "🎯 Quick Match" for instant job matching

## 🤖 LLM Integration & Prompts

### AI-Powered Candidate Scoring

The application uses **Groq API** with the `llama-3.1-8b-instant` model to intelligently score candidates against job descriptions. The LLM analyzes the candidate's skills section and provides structured feedback including:

- **Score**: Float between 0.0 (no match) and 1.0 (perfect match)
- **Justification**: Detailed explanation of the scoring decision
- **Matches**: List of specific skills that match the job requirements
- **Recommendation**: Overall assessment and next steps

### Prompt Engineering

#### Core Prompt Template

```python
# From backend/llm_client.py
prompt = (
    "You are a technical recruiter. Compare the candidate's Skills section "
    "with the Job Description and evaluate fit.\n\n"
    "Return ONLY JSON in the following format:\n"
    '{"score": <float between 0.0 and 1.0>, "justification": <string>, "matches": [<skills>], "recommendation": <string>}\n\n'
    "IMPORTANT: The score must be a float between 0.0 (no match) and 1.0 (perfect match).\n"
    "For example: 0.85 means 85% match, 0.5 means 50% match.\n\n"
    "Job Description:\n" + job_desc + "\n\n" +
    "Candidate Skills Section:\n" + resume_skills_text
)
```

#### Scoring Guidelines

The LLM follows these scoring principles:

| Score Range | Interpretation | Example Scenarios |
|-------------|----------------|-------------------|
| **0.8 - 1.0** | Excellent Match | Candidate has most/all required skills |
| **0.6 - 0.8** | Good Match | Strong overlap with key requirements |
| **0.4 - 0.6** | Moderate Match | Some relevant skills, gaps in others |
| **0.2 - 0.4** | Weak Match | Limited relevant skills |
| **0.0 - 0.2** | Poor Match | Minimal or no skill overlap |

#### Prompt Examples

**Example 1: Software Engineer Position**
```json
{
  "score": 0.85,
  "justification": "Strong match with 8+ years Python experience, cloud expertise, and modern development practices",
  "matches": ["Python", "AWS", "Docker", "React", "PostgreSQL"],
  "recommendation": "Interview recommended - excellent technical background"
}
```

**Example 2: Data Scientist Position**
```json
{
  "score": 0.62,
  "justification": "Good foundation in Python and statistics, but lacks deep learning and big data experience",
  "matches": ["Python", "Machine Learning", "Statistics", "Pandas"],
  "recommendation": "Consider for junior role or after additional training"
}
```

#### LLM Configuration

```python
# Environment variables for LLM setup
LLM_API_KEY=your-groq-api-key-here          # Groq API key
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions  # API endpoint
LLM_MODEL=llama-3.1-8b-instant              # Model selection
```

**Temperature Setting**: 0.0 (deterministic responses for consistent scoring)

**Max Tokens**: 300 (sufficient for detailed justification)

### Integration Architecture

```
Frontend (Streamlit) → API Client → Backend (Flask) → LLM Client → Groq API
       ↓                    ↓              ↓              ↓           ↓
   Job Description   HTTP POST /match   rate_candidate()   build_prompt()
   + Min Score      → JSON Request     → LLM Analysis    → JSON Response
```

## 🔧 Configuration

### Backend Configuration

The backend API supports the following RESTful endpoints:

#### Core Endpoints

| Method | Endpoint | Description | Request/Response Format |
|--------|----------|-------------|------------------------|
| `GET` | `/` | API health check and version info | Returns: `{"success": true, "message": "Resume Screener API", "version": "2.0"}` |
| `POST` | `/upload` | Upload and parse resume files | **Request**: `multipart/form-data` with `resume` file<br>**Response**: Candidate data with parsed information |
| `GET` | `/candidates` | Retrieve all candidates | **Response**: Array of candidate objects |
| `GET` | `/candidate/<id>` | Get specific candidate details | **Response**: Single candidate object with skills_list array |
| `POST` | `/match` | Match candidates against job description | **Request**: `{"job_description": "text", "min_score": 0.7}`<br>**Response**: Ranked candidates with scores and analysis |

#### Detailed Endpoint Documentation

**POST /upload**
- **Purpose**: Upload and parse resume files
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `resume`: File field containing PDF, DOCX, or TXT file
- **Response Format**:
```json
{
  "success": true,
  "message": "Resume uploaded and parsed successfully",
  "data": {
    "candidate": {
      "id": "1",
      "filename": "john_doe_resume.pdf",
      "name": "John Doe",
      "email": "john.doe@email.com",
      "phone": "+1-555-0123",
      "skills": "Python; JavaScript; React; Node.js",
      "education": "Bachelor's in Computer Science",
      "experience": "5+ years software development",
      "text": "Full resume text content...",
      "created_at": "2025-01-15T10:30:00"
    }
  }
}
```

**POST /match**
- **Purpose**: AI-powered candidate matching against job descriptions
- **Content-Type**: `application/json`
- **Request Body**:
```json
{
  "job_description": "Senior Python Developer with AWS experience needed for fintech startup...",
  "min_score": 0.7
}
```
- **Response Format**:
```json
{
  "success": true,
  "message": "Matched 3 candidates against job description",
  "data": {
    "job_description": "Senior Python Developer...",
    "results": [
      {
        "candidate_id": "1",
        "candidate_name": "John Doe",
        "score": 0.85,
        "justification": "Strong match with 8+ years Python experience...",
        "matches": ["Python", "AWS", "Docker", "React"],
        "recommendation": "Interview recommended",
        "candidate_data": { /* full candidate object */ }
      }
    ],
    "total_candidates": 10,
    "matched_candidates": 3,
    "min_score": 0.7,
    "timestamp": "2025-01-15T10:30:00"
  }
}
```

### Frontend Configuration

The Streamlit interface can be configured via environment variables:

- `BACKEND_URL` - Backend API URL (default: `http://localhost:5000`)
- Theme and styling are defined in the application code

## 📁 Project Structure

```
resumescan/
├── .env                    # Environment variables (create this file)
│   ├── SECRET_KEY          # Flask application secret
│   ├── LLM_API_KEY         # Groq API authentication
│   ├── LLM_API_URL         # Groq API endpoint
│   └── LLM_MODEL           # Model selection (llama-3.1-8b-instant)
├── .gitignore             # Git ignore patterns
├── .python-version        # Python version specification
├── pyproject.toml         # Project configuration and dependencies
├── requirements.txt       # Main requirements file
├── uv.lock               # uv package manager lock file
├── README.md             # This file
├── resumes.csv           # Candidate database (auto-generated)
├── test_upload.py        # Test script for parser validation
└── Demo-Video-Arin.mp4   # Project demonstration video

backend/                          # Flask API backend
├── app.py                       # Main Flask application & API routes
│   ├── File upload handling     # Multipart form-data processing
│   ├── Resume parsing           # PDF/DOCX/TXT text extraction
│   ├── Candidate management     # CRUD operations for candidates
│   ├── LLM integration          # Groq API communication
│   └── CSV data persistence     # Candidate storage in CSV format
├── parser.py                    # Resume parsing & text extraction
│   ├── PDF processing           # pdfminer.six integration
│   ├── DOCX processing          # python-docx integration
│   ├── Section extraction       # Skills, education, experience parsing
│   └── Contact extraction       # Email, phone, name detection
├── llm_client.py                # Groq LLM API integration
│   ├── Prompt engineering       # Structured prompt templates
│   ├── Response parsing         # JSON response handling
│   ├── Error handling           # API failure recovery
│   └── Score calculation        # Candidate-job matching algorithm
├── requirements.txt             # Backend-specific dependencies
└── uploads/                     # Uploaded resume files (auto-created)
    ├── ARIN_BALYAN.pdf         # Sample resume file
    ├── C1061.pdf               # Sample resume file
    └── C1070.pdf               # Sample resume file

frontend/                        # Streamlit web frontend
├── app.py                      # Main Streamlit application
│   ├── UI components           # Dashboard, upload, candidates, matching
│   ├── Navigation system       # Sidebar navigation with session state
│   ├── Theme styling           # Dark theme with custom CSS
│   ├── File upload interface   # Drag-and-drop resume upload
│   └── Results visualization   # Candidate cards and match results
├── api_client.py               # Backend API communication
│   ├── HTTP client             # Requests session management
│   ├── Error handling          # API failure recovery
│   ├── File upload support     # Binary file handling
│   └── Response parsing        # JSON response processing
└── requirements.txt            # Frontend-specific dependencies
```

## 🧪 Testing

### Run Parser Tests

Test the resume parsing functionality:

```bash
# Ensure test_resume.txt exists, then run:
python test_upload.py
```

The test script will validate:
- Text extraction from resume files
- Contact information parsing (name, email, phone)
- Skills section identification
- Education and experience extraction

### Manual Testing

1. **Upload Test Files**: Use the web interface to upload sample resumes
2. **Verify Parsing**: Check that information is correctly extracted
3. **Test Matching**: Create a job description and verify candidate scoring
4. **Check Storage**: Verify data is properly stored in `resumes.csv`

## 🔒 Security Considerations

- **File Upload Validation**: Only PDF, DOCX, and TXT files are accepted
- **Secure Filename Handling**: Uses Werkzeug's `secure_filename` function
- **CORS Configuration**: Properly configured for frontend-backend communication
- **Environment Variables**: Sensitive data stored in `.env` file (gitignored)
- **Input Sanitization**: Basic validation of uploaded content

## 🚀 Deployment

### Local Production Deployment

1. **Install Dependencies**:
   ```bash
   uv sync --extra production
   ```

2. **Set Production Environment**:
   ```bash
   export FLASK_ENV=production
   export STREAMLIT_SERVER_HEADLESS=true
   ```

3. **Run Backend**:
   ```bash
   nohup python backend/app.py > backend.log 2>&1 &
   ```

4. **Run Frontend**:
   ```bash
   nohup streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0 > frontend.log 2>&1 &
   ```

### Docker Deployment (Future)

Docker support can be added by creating:
- `Dockerfile.backend` for Flask API
- `Dockerfile.frontend` for Streamlit app
- `docker-compose.yml` for orchestration

## 📊 Data Storage

- **Candidate Data**: Stored in `resumes.csv` with columns:
  - `id`: Unique candidate identifier
  - `filename`: Original resume filename
  - `name`: Extracted candidate name
  - `email`: Contact email address
  - `phone`: Phone number
  - `skills`: Skills as semicolon-separated values
  - `education`: Education information
  - `experience`: Work experience details
  - `text`: Full resume text content
  - `created_at`: Processing timestamp

## 🔧 Troubleshooting

### Common Issues

1. **Backend Connection Failed**:
   - Ensure backend is running on port 5000
   - Check `BACKEND_URL` environment variable
   - Verify CORS configuration

2. **Resume Parsing Errors**:
   - Check file format (PDF, DOCX, TXT only)
   - Ensure file is not corrupted
   - Verify encoding is UTF-8 compatible

3. **LLM API Errors**:
    - Check `LLM_API_KEY` is valid and has credits
    - Verify `LLM_API_URL` is correct (should be `https://api.groq.com/openai/v1/chat/completions`)
    - Ensure network connectivity to Groq API (test with: `curl -H "Authorization: Bearer $LLM_API_KEY" $LLM_API_URL`)
    - Verify model name is correct (`llama-3.1-8b-instant`)
    - Check API rate limits (Groq has generous free tier limits)
    - Monitor API response times (timeout set to 60 seconds)

4. **LLM Response Parsing Issues**:
    - LLM may return non-JSON responses if prompt structure fails
    - Check that resume skills section extraction is working properly
    - Verify job description is not empty or malformed
    - Review LLM response logs in backend console output
    - Test with simple job descriptions to isolate parsing issues

5. **Scoring Inconsistencies**:
    - LLM scoring can vary with different prompt phrasings
    - Consider the context length (skills section + job description)
    - Very short skills sections may lead to lower accuracy
    - Complex job descriptions with many requirements may need simplification

4. **File Upload Issues**:
   - Check available disk space
   - Verify upload directory permissions
   - Ensure file size limits are appropriate

### Debug Mode

Enable debug logging by setting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Groq API** for fast LLM inference
- **Streamlit** for the beautiful frontend framework
- **Flask** for the robust backend API
- **pdfminer.six** for PDF text extraction
- **python-docx** for Word document processing

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing documentation
- Review troubleshooting section above

---

**Happy Resume Screening!** 🎯
