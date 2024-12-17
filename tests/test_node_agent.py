import pytest
from backend.node_agent.agent import NodeAgent

def test_job_execution():
    agent = NodeAgent(max_workers=2)
    
    test_job = {
        'id': 'test_job_1',
        'type': 'compute',
        'duration': 1
    }
    
    result = agent.execute_job(test_job)
    
    assert result['job_id'] == 'test_job_1'
    assert result['status'] in ['RUNNING', 'COMPLETED']