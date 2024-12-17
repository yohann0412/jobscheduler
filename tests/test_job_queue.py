import pytest
from backend.job_submission.job_queue import DistributedJobQueue

def test_job_queue_enqueue_and_dequeue():
    queue = DistributedJobQueue(max_size=10)
    
    # Test enqueue
    job = {'id': '1', 'command': 'test_job', 'priority': 5}
    queue.enqueue(job)
    
    # Test get_job
    retrieved_job = queue.get_job('1')
    assert retrieved_job == job
    
    # Test dequeue
    dequeued_job = queue.dequeue()
    assert dequeued_job == job