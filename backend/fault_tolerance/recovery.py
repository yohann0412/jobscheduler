# File: distributed-job-scheduler/backend/fault_tolerance/recovery.py

import logging
from typing import List, Dict, Any

class JobRecoveryManager:
    """
    Manage job recovery and retry mechanisms
    """
    def __init__(self, 
                 max_retries: int = 3, 
                 retry_delay: int = 60):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.logger = logging.getLogger('JobRecoveryManager')
    
    def recover_failed_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempt to recover a failed job
        """
        current_retries = job.get('retries', 0)
        
        if current_retries < self.max_retries:
            # Increment retry count
            job['retries'] = current_retries + 1
            
            # Optional: Add delay before retry
            job['next_retry_at'] = time.time() + self.retry_delay
            
            # Reset job status for retry
            job['status'] = 'QUEUED'
            
            self.logger.info(f"Recovering job {job['id']}, attempt {job['retries']}")
            return job
        else:
            # Mark job as permanently failed
            job['status'] = 'FAILED'
            self.logger.error(f"Job {job['id']} exceeded max retries")
            return job
    
    def batch_recovery(self, failed_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recover multiple failed jobs
        """
        recovered_jobs = []
        for job in failed_jobs:
            recovered_job = self.recover_failed_job(job)
            recovered_jobs.append(recovered_job)
        
        return recovered_jobs
    
    def log_job_failure(self, job: Dict[str, Any], error: str):
        """
        Log detailed job failure information
        """
        failure_log = {
            'job_id': job['id'],
            'error': error,
            'timestamp': time.time(),
            'retry_count': job.get('retries', 0)
        }
        
        # In a real system, this would write to a persistent log
        self.logger.error(f"Job Failure: {failure_log}")