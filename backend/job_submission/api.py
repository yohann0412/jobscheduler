from flask import Flask, request, jsonify
import uuid
import logging
import time  # Ensure time is imported
import traceback  # Add traceback for more detailed error logging
from typing import Dict, Any
from .job_queue import DistributedJobQueue

class JobSubmissionAPI:
    """
    RESTful API for job submission and management
    """
    def __init__(self, job_queue: DistributedJobQueue):
        self.app = Flask(__name__)
        self.job_queue = job_queue
        self.logger = logging.getLogger('JobSubmissionAPI')
        
        # Add error handler for detailed logging
        self.app.errorhandler(Exception)(self.handle_global_exception)
        
        self._setup_routes()
    
    def handle_global_exception(self, e):
        """
        Global error handler to provide more detailed error information
        """
        self.logger.error(f"Unhandled Exception: {str(e)}")
        self.logger.error(f"Exception Details: {traceback.format_exc()}")
        return jsonify({
            "error": "Internal Server Error",
            "details": str(e),
            "trace": traceback.format_exc()
        }), 500
    
    def _setup_routes(self):
        """
        Define API endpoints
        """
        self.app.route('/jobs', methods=['POST'])(self.submit_job)
        self.app.route('/jobs', methods=['GET'])(self.list_jobs)
        self.app.route('/jobs/<job_id>', methods=['GET'])(self.get_job_status)
        self.app.route('/jobs/<job_id>', methods=['DELETE'])(self.cancel_job)
    
    def submit_job(self):
        """
        Submit a new job to the queue
        """
        try:
            # Log incoming request details
            self.logger.info(f"Received job submission request")
            self.logger.info(f"Request JSON: {request.json}")
            
            job_data = request.json
            if not job_data:
                return jsonify({"error": "Invalid job data"}), 400
            
            # Explicitly log time module usage for debugging
            current_time = time.time()
            self.logger.info(f"Current timestamp: {current_time}")
            
            job = self._prepare_job(job_data)
            self.job_queue.enqueue(job)
            
            return jsonify({
                "job_id": job['id'],
                "status": "QUEUED"
            }), 201
        
        except Exception as e:
            # Log full traceback for debugging
            self.logger.error(f"Job submission error: {e}")
            self.logger.error(traceback.format_exc())
            return jsonify({
                "error": "Job submission failed",
                "details": str(e),
                "trace": traceback.format_exc()
            }), 500
    
    def _prepare_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and prepare job for submission
        """
        required_fields = ['command', 'type']
        for field in required_fields:
            if field not in job_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Explicitly check time module
        try:
            current_time = time.time()
            self.logger.info(f"Time check in _prepare_job: {current_time}")
        except Exception as e:
            self.logger.error(f"Time module error: {e}")
            raise
        
        return {
            'id': str(uuid.uuid4()),
            'status': 'QUEUED',
            'priority': job_data.get('priority', 5),
            'submitted_at': time.time(),  # Explicitly use time.time()
            'timeout': job_data.get('timeout', 3600),  # Add timeout with default
            **job_data
        }
    
    def list_jobs(self):
        """
        List all jobs in the queue
        """
        jobs = self.job_queue.get_all_jobs()
        return jsonify(jobs), 200
    
    def get_job_status(self, job_id: str):
        """
        Get status of a specific job
        """
        job = self.job_queue.get_job(job_id)
        if job:
            return jsonify(job), 200
        return jsonify({"error": "Job not found"}), 404
    
    def cancel_job(self, job_id: str):
        """
        Cancel a queued job
        """
        try:
            if self.job_queue.cancel_job(job_id):
                return jsonify({"message": "Job cancelled successfully"}), 200
            return jsonify({"error": "Job not found or cannot be cancelled"}), 404
        except Exception as e:
            self.logger.error(f"Job cancellation error: {e}")
            return jsonify({"error": str(e)}), 500
    
    def run(self, host='0.0.0.0', port=8000):
        """
        Run the Flask application
        """
        # Additional logging to verify time module
        try:
            current_time = time.time()
            self.logger.info(f"Application startup time check: {current_time}")
        except Exception as e:
            self.logger.error(f"Critical error with time module: {e}")
        
        self.app.run(host=host, port=port)