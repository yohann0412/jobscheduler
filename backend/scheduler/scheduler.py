# File: distributed-job-scheduler/backend/scheduler/scheduler.py

import logging
from typing import List, Dict, Any
from backend.config import Config
from .algorithms import JobSchedulingAlgorithms

class Scheduler:
    """
    Central job scheduling and distribution system
    """
    def __init__(self, job_queue, node_registry):
        self.job_queue = job_queue
        self.node_registry = node_registry
        self.logger = logging.getLogger('Scheduler')
    
    def distribute_jobs(self):
        """
        Distribute jobs across available nodes
        """
        available_nodes = self.node_registry.get_active_nodes()
        pending_jobs = self.job_queue.get_all_jobs()
        
        # Use least loaded node scheduling
        node_loads = {node['id']: node['current_load'] for node in available_nodes}
        job_distribution = JobSchedulingAlgorithms.least_loaded_node_scheduling(
            pending_jobs, node_loads
        )
        
        # Send jobs to respective nodes
        for node_id, jobs in job_distribution.items():
            self._send_jobs_to_node(node_id, jobs)
    
    def _send_jobs_to_node(self, node_id: str, jobs: List[Dict[str, Any]]):
        """
        Send jobs to a specific node
        """
        try:
            # Placeholder for actual job dispatch mechanism
            node = self.node_registry.get_node(node_id)
            # In real implementation, this would use RPC or message queue
            node.receive_jobs(jobs)
        except Exception as e:
            self.logger.error(f"Failed to send jobs to node {node_id}: {e}")