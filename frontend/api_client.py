import requests
import json
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeScreenerAPI:
    """API client for communicating with the Flask backend"""

    def __init__(self, base_url: Optional[str] = None):
        """Initialize API client with backend URL"""
        if base_url:
            self.base_url = base_url.rstrip('/')
        else:
            # Default to localhost, but can be overridden by environment
            self.base_url = os.getenv('BACKEND_URL', 'http://localhost:5000')

        self.session = requests.Session()
        self.session.timeout = 30  # 30 second timeout

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {method} {url} - {str(e)}")
            raise

    def upload_resume(self, file_path: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """Upload a resume file to the backend"""
        try:
            filepath = Path(file_path)
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(filepath, 'rb') as file:
                files = {'resume': (filename or filepath.name, file, 'application/octet-stream')}
                response = self._make_request('POST', '/upload', files=files)

            return {
                'success': True,
                'data': response.json(),
                'message': 'Resume uploaded successfully'
            }

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to upload resume'
            }

    def upload_resume_file(self, file) -> Dict[str, Any]:
        """Upload a resume file object to the backend"""
        try:
            files = {'resume': file}
            response = self._make_request('POST', '/upload', files=files)

            return {
                'success': True,
                'data': response.json(),
                'message': 'Resume uploaded successfully'
            }

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to upload resume'
            }

    def get_candidates(self) -> Dict[str, Any]:
        """Get all candidates from backend"""
        try:
            response = self._make_request('GET', '/candidates')
            result = response.json()
            
            # Backend returns: {"success": True, "message": "...", "data": [candidates]}
            # Return it directly without wrapping again
            return result

        except Exception as e:
            logger.error(f"Failed to fetch candidates: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': [],
                'count': 0,
                'message': 'Failed to retrieve candidates'
            }

    def get_candidate(self, candidate_id: str) -> Dict[str, Any]:
        """Get a specific candidate by ID"""
        try:
            response = self._make_request('GET', f'/candidate/{candidate_id}')
            result = response.json()
            
            # Backend returns: {"success": True, "message": "...", "data": candidate_dict}
            # Return it directly
            return result

        except Exception as e:
            logger.error(f"Failed to fetch candidate {candidate_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': None,
                'message': f'Failed to retrieve candidate {candidate_id}'
            }

    def match_candidates(self, job_description: str, min_score: float = 0.0) -> Dict[str, Any]:
        """Match candidates against job description"""
        try:
            data = {
                'job_description': job_description.strip(),
                'min_score': min_score
            }

            response = self._make_request('POST', '/match', json=data)
            result = response.json()
            
            # Backend returns: {"success": True, "message": "...", "data": {results, total_candidates, ...}}
            # Return it directly - no need to re-sort or re-filter, backend already does this
            return result

        except Exception as e:
            logger.error(f"Matching failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': [],
                'count': 0,
                'message': 'Failed to perform candidate matching'
            }

    def get_stats(self) -> Dict[str, Any]:
        """Get application statistics"""
        try:
            candidates_result = self.get_candidates()

            if not candidates_result['success']:
                return {
                    'success': False,
                    'error': 'Failed to get candidate data',
                    'data': {}
                }

            candidates = candidates_result['data']

            # Calculate statistics
            total_candidates = len(candidates)
            avg_score = 0.0

            if total_candidates > 0:
                # This would need actual score data from the backend
                # For now, we'll return basic stats
                pass

            stats = {
                'total_candidates': total_candidates,
                'total_resumes': total_candidates,
                'avg_score': avg_score,
                'last_updated': None
            }

            return {
                'success': True,
                'data': stats,
                'message': 'Statistics retrieved successfully'
            }

        except Exception as e:
            logger.error(f"Failed to get stats: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': {},
                'message': 'Failed to retrieve statistics'
            }

    def health_check(self) -> Dict[str, Any]:
        """Check if backend is healthy"""
        try:
            response = self._make_request('GET', '/')
            return {
                'success': True,
                'status': response.status_code,
                'message': 'Backend is healthy'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Backend health check failed'
            }