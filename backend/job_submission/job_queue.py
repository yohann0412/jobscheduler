# File: distributed-job-scheduler/backend/job_submission/job_queue.py

import threading
from queue import PriorityQueue
import time
from typing import List, Dict, Any

class DistributedJobQueue:
    """
    Thread-safe distributed job queue with advanced features
    """
    def __init__(self, max_size: int = 1000, priority_levels: int = 3):
        self.queue = PriorityQueue(maxsize=max_size)
        self.jobs = {}  # In-memory job store
        self.max_size = max_size
        self.priority_levels = priority_levels
        self.lock = threading.Lock()
    
    def enqueue(self, job: Dict[str, Any]) -> None:
        """
        Add a job to the queue
        """
        with self.lock:
            if len(self.jobs) >= self.max_size:
                raise Exception("Job queue is full")
            
            # Normalize priority
            priority = max(0, min(job.get('priority', self.priority_levels // 2), 
                                   self.priority_levels - 1))
            
            # Lower number = higher priority
            queue_priority = (priority, job.get('submitted_at', time.time()))
            
            self.queue.put((queue_priority, job))
            self.jobs[job['id']] = job
    
    def dequeue(self) -> Dict[str, Any]:
        """
        Get and remove the next job from the queue
        """
        with self.lock:
            if not self.queue.empty():
                _, job = self.queue.get()
                del self.jobs[job['id']]
                return job
            return None
    
    def get_job(self, job_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific job by ID
        """
        return self.jobs.get(job_id)
    
    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        Get all jobs in the queue
        """
        return list(self.jobs.values())
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a specific job
        """
        with self.lock:
            if job_id in self.jobs:
                # Remove from internal job store
                del self.jobs[job_id]
                
                # Rebuild queue without the cancelled job
                temp_queue = PriorityQueue()
                while not self.queue.empty():
                    item = self.queue.get()
                    if item[1]['id'] != job_id:
                        temp_queue.put(item)
                
                self.queue = temp_queue
                return True
            return False
    
    def update_job_status(self, job_id: str, status: str) -> None:
        """
        Update status of a specific job
        """
        with self.lock:
            if job_id in self.jobs:
                self.jobs[job_id]['status'] = status