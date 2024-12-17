# File: distributed-job-scheduler/backend/main.py

import logging
import time
from backend.config import Config
from scheduler.scheduler import Scheduler
from node_agent.agent import NodeAgent
from job_submission.api import JobSubmissionAPI
from job_submission.job_queue import DistributedJobQueue
from fault_tolerance.heartbeat import HeartbeatMonitor
from performance.metrics import PerformanceMetrics

class NodeRegistry:
    """
    Placeholder node registry to resolve HeartbeatMonitor initialization
    """
    def __init__(self):
        self.nodes = []
    
    def get_active_nodes(self):
        return self.nodes
    
    def mark_node_inactive(self, node_id):
        pass
    
    def get_node_jobs(self, node_id):
        return []

def setup_logging():
    """
    Configure logging for the application
    """
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=Config.LOG_FORMAT
    )

def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger('DistributedJobScheduler')
    
    try:
        # Validate configuration
        Config.validate_config()
        
        # Initialize node registry
        node_registry = NodeRegistry()
        
        # Initialize core components
        job_queue = DistributedJobQueue(
            max_size=Config.JOB_QUEUE_MAX_SIZE,
            priority_levels=Config.JOB_QUEUE_PRIORITY_LEVELS
        )
        
        node_agent = NodeAgent(
            max_workers=Config.NODE_AGENT_MAX_WORKERS
        )
        
        # Initialize performance metrics
        metrics_collector = PerformanceMetrics(
            collection_interval=Config.METRICS_COLLECTION_INTERVAL
        )
        metrics_collector.start_periodic_reporting()
        
        # Initialize job submission API
        job_api = JobSubmissionAPI(job_queue)
        
        # Initialize scheduler with job queue and node registry
        scheduler = Scheduler(job_queue, node_registry)
        
        # Initialize heartbeat monitoring with node registry
        heartbeat_monitor = HeartbeatMonitor(
            node_registry=node_registry, 
            check_interval=Config.NODE_AGENT_HEARTBEAT_INTERVAL
        )
        heartbeat_monitor.start_monitoring()
        
        # Start job submission API
        job_api.run(
            host=Config.SCHEDULER_HOST, 
            port=Config.SCHEDULER_PORT
        )
    
    except Exception as e:
        logger.error(f"Scheduler initialization failed: {e}")
        raise

if __name__ == "__main__":
    main()