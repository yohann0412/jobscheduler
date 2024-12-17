# File: distributed-job-scheduler/backend/performance/metrics.py

import time
import threading
import logging
from typing import Dict, Any, List

class PerformanceMetrics:
    """
    Comprehensive performance metrics collection and analysis
    """
    def __init__(self, collection_interval: int = 60):
        self.metrics = {
            'jobs_processed': 0,
            'total_processing_time': 0,
            'average_job_duration': 0,
            'node_utilization': {},
            'queue_metrics': {
                'queue_length': 0,
                'wait_times': []
            }
        }
        self.collection_interval = collection_interval
        self.logger = logging.getLogger('PerformanceMetrics')
        self.lock = threading.Lock()
    
    def record_job_completion(self, job: Dict[str, Any]):
        """
        Record metrics for a completed job
        """
        with self.lock:
            self.metrics['jobs_processed'] += 1
            job_duration = job.get('end_time', time.time()) - job.get('start_time', time.time())
            
            self.metrics['total_processing_time'] += job_duration
            self.metrics['average_job_duration'] = (
                self.metrics['total_processing_time'] / self.metrics['jobs_processed']
            )
            
            # Record wait time
            wait_time = job.get('start_time', time.time()) - job.get('submitted_at', time.time())
            self.metrics['queue_metrics']['wait_times'].append(wait_time)
    
    def update_node_utilization(self, node_id: str, utilization: float):
        """
        Update utilization for a specific node
        """
        with self.lock:
            self.metrics['node_utilization'][node_id] = utilization
    
    def update_queue_length(self, length: int):
        """
        Update current queue length
        """
        with self.lock:
            self.metrics['queue_metrics']['queue_length'] = length
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive performance summary
        """
        with self.lock:
            return {
                'total_jobs_processed': self.metrics['jobs_processed'],
                'average_job_duration': self.metrics['average_job_duration'],
                'node_utilization': self.metrics['node_utilization'],
                'queue_metrics': {
                    'current_length': self.metrics['queue_metrics']['queue_length'],
                    'average_wait_time': (
                        sum(self.metrics['queue_metrics']['wait_times']) / 
                        len(self.metrics['queue_metrics']['wait_times'])
                        if self.metrics['queue_metrics']['wait_times'] else 0
                    )
                },
                'timestamp': time.time()
            }
    
    def start_periodic_reporting(self):
        """
        Start background thread for periodic metric reporting
        """
        def report_metrics():
            while True:
                summary = self.get_performance_summary()
                self.logger.info(f"Performance Summary: {summary}")
                time.sleep(self.collection_interval)
        
        reporting_thread = threading.Thread(target=report_metrics, daemon=True)
        reporting_thread.start()