import streamlit as st
import requests
import json
import pandas as pd
from typing import List, Dict, Any
import os
from datetime import datetime
import base64
from api_client import ResumeScreenerAPI

# Page configuration
st.set_page_config(
    page_title="Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design
def load_css():
    st.markdown("""
    <style>
    /* Dark theme with white and gray colors */
    :root {
        --primary-color: #ffffff;
        --secondary-color: #333333;
        --accent-color: #e2e8f0;
        --success-color: #e0e0e0;
        --warning-color: #cccccc;
        --error-color: #ffffff;
        --background-color: #2d3748;
        --surface-color: #4a5568;
        --text-primary: #ffffff;
        --text-secondary: #e2e8f0;
        --border-color: #718096;
        --card-background: #4a5568;
        --sidebar-background: #2d3748;
    }

    /* Global styles */
    body {
        background-color: var(--background-color);
        color: var(--text-primary);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Sidebar styling */
    .sidebar-header {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1rem;
        color: var(--text-primary);
    }

    .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: var(--text-primary);
        background-color: transparent;
    }

    .nav-item:hover {
        background-color: var(--surface-color);
        transform: translateX(4px);
    }

    .nav-item.active {
        background-color: var(--primary-color);
        color: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }

    /* Card styling */
    .metric-card {
        background: var(--card-background);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        color: var(--text-primary);
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .metric-card h2, .metric-card h3 {
        color: var(--text-primary);
        margin: 0;
    }

    /* Button styling */
    .stButton button {
        border-radius: 0.75rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        padding: 0.75rem 1.5rem;
    }

    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* File uploader styling */
    .upload-area {
        border: 2px dashed var(--border-color);
        border-radius: 1rem;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        background: var(--surface-color);
        color: var(--text-primary);
    }

    .upload-area:hover {
        border-color: var(--primary-color);
        background: rgba(255, 255, 255, 0.05);
    }

    /* Ensure all text is readable */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }

    p, span, div, label {
        color: var(--text-primary) !important;
    }

    /* Sidebar specific styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-background) !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    /* Navigation improvements for dark theme */
    .nav-item.active {
        background-color: var(--primary-color);
        color: var(--background-color) !important;
        box-shadow: 0 2px 8px rgba(255, 255, 255, 0.2);
    }

    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }

    .slide-in {
        animation: slideIn 0.4s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }

    /* Main container styling */
    .main .block-container {
        background-color: var(--background-color) !important;
        color: var(--text-primary) !important;
    }

    /* Streamlit button styling */
    .stButton button {
        background-color: var(--surface-color) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    .stButton button:hover {
        background-color: var(--accent-color) !important;
        border-color: var(--primary-color) !important;
    }

    /* Text input styling */
    .stTextInput input, .stTextArea textarea {
        background-color: var(--surface-color) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* File uploader styling */
    .stFileUploader {
        background-color: var(--surface-color) !important;
        border: 2px dashed var(--border-color) !important;
        border-radius: 0.5rem;
        padding: 1rem;
        color: var(--text-primary) !important;
    }

    /* Select box styling */
    .stSelectbox div[data-baseweb="select"] div {
        background-color: var(--surface-color) !important;
        color: var(--text-primary) !important;
    }

    /* Slider styling */
    .stSlider div[data-testid="stTickBar"] {
        background-color: var(--border-color) !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .metric-card {
            padding: 1rem;
        }
        .nav-item {
            padding: 0.5rem 0.75rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize API client
api = ResumeScreenerAPI()

# Sidebar navigation component
def sidebar_navigation():
    st.markdown('<div class="sidebar-header">', unsafe_allow_html=True)
    st.markdown("## 📄 Resume Screener")
    st.markdown("Professional resume screening and matching")
    st.markdown('</div>', unsafe_allow_html=True)

    nav_items = {
        "🏠 Dashboard": "dashboard",
        "📤 Upload Resume": "upload",
        "👥 Candidates": "candidates",
        "🎯 Match Jobs": "match",
        "📊 Analytics": "analytics"
    }

    current_page = st.session_state.get('current_page', 'dashboard')

    for label, page in nav_items.items():
        is_active = current_page == page
        active_class = "active" if is_active else ""

        st.markdown(f"""
        <div class="nav-item {active_class}" onclick="setPage('{page}')">
            {label}
        </div>
        """, unsafe_allow_html=True)

        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.current_page = page
            st.rerun()

    # Theme is now fixed to black/gray scheme
    st.session_state.theme = "classic"

# Main content area
def main_content():
    current_page = st.session_state.get('current_page', 'dashboard')

    if current_page == "dashboard":
        show_dashboard()
    elif current_page == "upload":
        show_upload()
    elif current_page == "candidates":
        show_candidates()
    elif current_page == "match":
        show_matching()
    elif current_page == "analytics":
        show_analytics()

# Dashboard page
def show_dashboard():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("📊 Dashboard")
    st.markdown("Welcome to the Resume Screener Dashboard")

    # Get real statistics from backend
    try:
        stats_result = api.get_stats()
        if stats_result.get('success'):
            stats = stats_result.get('data', {})
            total_candidates = stats.get('total_candidates', 0)
            avg_score = stats.get('avg_score', 0.0)
        else:
            total_candidates = 0
            avg_score = 0.0
    except:
        total_candidates = 0
        avg_score = 0.0

    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>👥 Total Candidates</h3>
            <h2>{total_candidates}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📄 Resumes Processed</h3>
            <h2>{total_candidates}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🎯 Matches Found</h3>
            <h2>0</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Avg. Score</h3>
            <h2>{avg_score:.1f}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Quick Actions")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📤 Upload New Resume", use_container_width=True):
            st.session_state.current_page = "upload"
            st.rerun()

    with col2:
        if st.button("🎯 Run Job Matching", use_container_width=True):
            st.session_state.current_page = "match"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Upload page
def show_upload():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("📤 Upload Resume")

    st.markdown("Upload PDF, DOCX, or TXT resume files for processing.")

    # File uploader with custom styling
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Choose resume files",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_files:
        st.success(f"📎 {len(uploaded_files)} file(s) selected")

        if st.button("🚀 Process Resumes", type="primary", use_container_width=True):
            with st.spinner("Processing resumes..."):
                success_count = 0
                for file in uploaded_files:
                    st.info(f"Processing: {file.name}")
                    try:
                        # Upload file to backend
                        result = api.upload_resume_file(file)
                        if result.get('success'):
                            success_count += 1
                            st.success(f"✅ {file.name} processed successfully")
                        else:
                            st.error(f"❌ Failed to process {file.name}: {result.get('message')}")
                    except Exception as e:
                        st.error(f"❌ Error processing {file.name}: {str(e)}")

                if success_count > 0:
                    st.success(f"🎉 Successfully processed {success_count} resume(s)!")

                # Refresh candidate list
                st.rerun()

    st.markdown("### Supported Formats")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📄 **PDF Files**\nPortable Document Format")
    with col2:
        st.info("📝 **DOCX Files**\nMicrosoft Word documents")
    with col3:
        st.info("📃 **TXT Files**\nPlain text files")

    st.markdown('</div>', unsafe_allow_html=True)

# Candidates page
def show_candidates():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("👥 Candidates")

    # Get candidates from API
    try:
        result = api.get_candidates()
        if result.get('success'):
            # Backend returns: {"success": True, "message": "...", "data": [candidates]}
            candidates = result.get('data', [])
            
            # Verify we got a list
            if not isinstance(candidates, list):
                st.error(f"Unexpected data format from backend. Expected list, got {type(candidates)}")
                candidates = []
        else:
            st.error(f"Failed to fetch candidates: {result.get('message')}")
            candidates = []
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")
        candidates = []

    if not candidates:
        st.info("👋 No candidates uploaded yet. Start by uploading some resumes!")
        if st.button("📤 Go to Upload", use_container_width=True):
            st.session_state.current_page = "upload"
            st.rerun()
        return

    st.success(f"📊 Found {len(candidates)} candidates")

    # Display candidates in a nice table
    for candidate in candidates:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                name = candidate.get('name') or candidate.get('filename', 'Unknown')
                st.subheader(name)
                st.write(f"📧 {candidate.get('email', 'N/A')}")
                st.write(f"📞 {candidate.get('phone', 'N/A')}")

            with col2:
                skills = candidate.get('skills', '').split(';') if candidate.get('skills') else []
                st.write("**Skills:**")
                for skill in skills[:3]:  # Show first 3 skills
                    st.markdown(f"• {skill}")
                if len(skills) > 3:
                    st.write(f"... +{len(skills) - 3} more")

            with col3:
                if st.button("👁️ View Details", key=f"view_{candidate['id']}"):
                    # Store selected candidate ID for detail view
                    st.session_state.selected_candidate = candidate['id']
                    st.session_state.current_page = "candidate_detail"
                    st.rerun()

                if st.button("🎯 Quick Match", key=f"match_{candidate['id']}"):
                    st.session_state.match_candidate = candidate['id']
                    st.session_state.current_page = "match"
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Matching page
def show_matching():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("🎯 Job Matching")

    st.markdown("Enter a job description to find the best matching candidates.")

    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the job description here...",
        help="Be specific about requirements, skills, and experience needed"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        min_score = st.slider(
            "Minimum Match Score", 
            0.0, 
            1.0, 
            0.7, 
            0.01,
            help="LLM returns scores from 0.0 (no match) to 1.0 (perfect match)"
        )

    with col2:
        max_candidates = st.selectbox(
            "Max Results", 
            [1, 5, 10, 15, 20], 
            index=1,
            help="Maximum number of candidates to display"
        )

    if st.button("🔍 Find Matches", type="primary", use_container_width=True):
        if not job_description.strip():
            st.error("Please enter a job description")
            return

        with st.spinner("Analyzing candidates..."):
            try:
                # Call backend API for matching
                result = api.match_candidates(job_description, min_score)

                if result.get('success'):
                    # Backend returns data object with 'results' array
                    data = result.get('data', {})
                    matches = data.get('results', [])

                    if matches:
                        st.success(f"🎯 Found {len(matches)} matching candidates")

                        for i, match in enumerate(matches[:max_candidates]):
                            score = match.get('score', 0)
                            candidate_name = match.get('candidate_name', 'Unknown')
                            justification = match.get('justification', 'No reasoning provided')

                            # Convert score to percentage for display
                            score_percentage = score * 100

                            with st.container():
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h4>{candidate_name}</h4>
                                    <p><strong>Match Score: {score:.2f} ({score_percentage:.0f}%)</strong></p>
                                    <p>{justification}</p>
                                </div>
                                """, unsafe_allow_html=True)

                                # Show matches if available
                                candidate_matches = match.get('matches', [])
                                if candidate_matches:
                                    st.write("**Matching Skills:**")
                                    for skill in candidate_matches[:5]:  # Show top 5 matches
                                        st.markdown(f"• {skill}")
                    else:
                        st.warning("No matches found. Try adjusting your criteria or minimum score.")
                else:
                    st.error(f"Matching failed: {result.get('message')}")

            except Exception as e:
                st.error(f"Error during matching: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# Analytics page
def show_analytics():
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("📊 Analytics")

    st.info("📈 Analytics dashboard coming soon!")

    st.markdown('</div>', unsafe_allow_html=True)

# Main application
def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'

    # Load custom CSS
    load_css()

    # JavaScript for navigation
    st.markdown("""
    <script>
    function setPage(page) {
        // This would be handled by Streamlit buttons
    }
    </script>
    """, unsafe_allow_html=True)

    # Layout with sidebar and main content
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: var(--surface-color);
        border-right: 1px solid var(--border-color);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        sidebar_navigation()

    main_content()

if __name__ == "__main__":
    main()