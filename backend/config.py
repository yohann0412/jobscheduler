# File: distributed-job-scheduler/backend/config.py

import os
from typing import Dict, Any

class Config:
    """
    Centralized configuration management
    """
    # Core Scheduler Configuration
    SCHEDULER_HOST = os.getenv('SCHEDULER_HOST', 'localhost')
    SCHEDULER_PORT = int(os.getenv('SCHEDULER_PORT', 8000))
    
    # Node Agent Configuration
    NODE_AGENT_MAX_WORKERS = int(os.getenv('NODE_AGENT_MAX_WORKERS', 4))
    NODE_AGENT_HEARTBEAT_INTERVAL = int(os.getenv('NODE_AGENT_HEARTBEAT_INTERVAL', 30))
    
    # Job Queue Configuration
    JOB_QUEUE_MAX_SIZE = int(os.getenv('JOB_QUEUE_MAX_SIZE', 1000))
    JOB_QUEUE_PRIORITY_LEVELS = int(os.getenv('JOB_QUEUE_PRIORITY_LEVELS', 3))
    
    # Fault Tolerance Configuration
    FAULT_TOLERANCE_RETRY_LIMIT = int(os.getenv('FAULT_TOLERANCE_RETRY_LIMIT', 3))
    FAULT_TOLERANCE_TIMEOUT = int(os.getenv('FAULT_TOLERANCE_TIMEOUT', 60))
    
    # Performance Monitoring
    METRICS_COLLECTION_INTERVAL = int(os.getenv('METRICS_COLLECTION_INTERVAL', 60))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///job_scheduler.db')
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Returns a dictionary of all configuration settings
        """
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith('__') and not callable(value)
        }
    
    @classmethod
    def validate_config(cls):
        """
        Validate configuration settings
        """
        # Add specific validation logic
        if cls.SCHEDULER_PORT <= 0 or cls.SCHEDULER_PORT > 65535:
            raise ValueError("Invalid scheduler port")
        
        if cls.NODE_AGENT_MAX_WORKERS <= 0:
            raise ValueError("Max workers must be positive")