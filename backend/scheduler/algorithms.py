# File: distributed-job-scheduler/backend/scheduler/algorithms.py

import heapq
import time
from typing import List, Dict, Any

class JobSchedulingAlgorithms:
    """
    Advanced job scheduling strategies
    """
    @staticmethod
    def round_robin(jobs: List[Dict[str, Any]], num_nodes: int):
        """
        Distribute jobs evenly across nodes
        """
        distributed_jobs = [[] for _ in range(num_nodes)]
        for i, job in enumerate(jobs):
            node_index = i % num_nodes
            distributed_jobs[node_index].append(job)
        return distributed_jobs
    
    @staticmethod
    def priority_scheduling(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Schedule jobs based on priority and submission time
        """
        priority_queue = []
        for job in jobs:
            heapq.heappush(priority_queue, (
                job.get('priority', 10),  # Default priority
                job.get('submitted_at', time.time()),
                job
            ))
        
        return [heapq.heappop(priority_queue)[2] for _ in range(len(priority_queue))]