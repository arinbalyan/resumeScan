# Resume Screener 📄

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

The application consists of two main components:

### Backend (Flask API)
- **Location**: `backend/` directory
- **Purpose**: REST API for resume processing and candidate management
- **Key Files**:
  - `backend/app.py` - Main Flask application with API endpoints
  - `backend/parser.py` - Resume parsing and text extraction
  - `backend/llm_client.py` - Integration with Groq LLM API
  - `backend/requirements.txt` - Backend-specific dependencies

### Frontend (Streamlit)
- **Location**: `frontend/` directory
- **Purpose**: Modern web interface for user interaction
- **Key Files**:
  - `frontend/app.py` - Main Streamlit application
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

## 🔧 Configuration

### Backend Configuration

The backend API supports the following endpoints:

- `GET /` - API health check
- `POST /upload` - Upload and parse resume files
- `GET /candidates` - Retrieve all candidates
- `GET /candidate/<id>` - Get specific candidate details
- `POST /match` - Match candidates against job description

### Frontend Configuration

The Streamlit interface can be configured via environment variables:

- `BACKEND_URL` - Backend API URL (default: `http://localhost:5000`)
- Theme and styling are defined in the application code

## 📁 Project Structure

```
resumescan/
├── .env                    # Environment variables (create this file)
├── .gitignore             # Git ignore patterns
├── pyproject.toml         # Project configuration and dependencies
├── requirements.txt       # Main requirements
├── uv.lock               # uv lock file
├── README.md             # This file
├── resumes.csv           # Candidate database (auto-generated)
└── test_upload.py        # Test script for parser validation

backend/                  # Flask API backend
├── app.py               # Main Flask application
├── parser.py            # Resume parsing logic
├── llm_client.py        # Groq LLM integration
├── requirements.txt     # Backend-specific dependencies
└── uploads/             # Uploaded resume files (auto-created)

frontend/                # Streamlit frontend
├── app.py              # Main Streamlit application
├── api_client.py       # Backend API client
└── requirements.txt    # Frontend-specific dependencies

static/                  # Static assets for web interface
└── styles.css          # CSS styling

templates/               # HTML templates (alternative web interface)
├── base.html
├── index.html
├── upload.html
├── candidates.html
├── candidate.html
├── match_form.html
└── match_results.html
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
   - Verify `LLM_API_URL` is correct
   - Ensure network connectivity to Groq API

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