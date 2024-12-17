# File: distributed-job-scheduler/backend/node_agent/agent.py

import multiprocessing
import threading
import logging
import time
import psutil
from typing import Dict, Any

class NodeAgent:
    """
    Manages job execution and resource monitoring for a single compute node
    """
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.worker_pool = multiprocessing.Pool(processes=max_workers)
        self.active_jobs: Dict[str, Any] = {}
        self.logger = logging.getLogger('NodeAgent')
    
    def execute_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a job using worker pool
        """
        try:
            job_id = job['id']
            self.active_jobs[job_id] = job
            
            result = self.worker_pool.apply_async(self._run_job, (job,))
            
            return {
                'job_id': job_id,
                'status': 'RUNNING',
                'result': result.get(timeout=job.get('timeout', 3600))
            }
        except Exception as e:
            self.logger.error(f"Job execution failed: {e}")
            return {
                'job_id': job.get('id'),
                'status': 'FAILED',
                'error': str(e)
            }
    
    def _run_job(self, job: Dict[str, Any]) -> Any:
        """
        Internal method to run a specific job
        """
        # Placeholder job execution logic
        job_type = job.get('type')
        if job_type == 'compute':
            # Simulate computation
            time.sleep(job.get('duration', 5))
        elif job_type == 'data_processing':
            # Simulate data processing
            time.sleep(job.get('duration', 10))
        
        return f"Completed job {job.get('id')}"