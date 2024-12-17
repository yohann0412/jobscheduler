import pytest
from backend.scheduler.scheduler import Scheduler
from backend.job_submission.job_queue import DistributedJobQueue

def test_job_distribution():
    # Mock node registry and job queue
    job_queue = DistributedJobQueue()
    mock_node_registry = MockNodeRegistry()
    scheduler = Scheduler(job_queue, mock_node_registry)
    
    # Add test jobs to the queue
    test_jobs = [
        {'id': '1', 'command': 'process_data', 'priority': 5},
        {'id': '2', 'command': 'compute_analytics', 'priority': 3}
    ]
    for job in test_jobs:
        job_queue.enqueue(job)
    
    # Distribute jobs
    scheduler.distribute_jobs()
    
    # Assert jobs are correctly distributed
    assert len(mock_node_registry.distributed_jobs) > 0