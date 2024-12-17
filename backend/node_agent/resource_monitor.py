# File: distributed-job-scheduler/backend/node_agent/resource_monitor.py

import psutil
import time
import logging
from typing import Dict, Any

class ResourceMonitor:
    """
    Comprehensive system resource monitoring
    """
    def __init__(self, monitoring_interval: int = 60):
        self.monitoring_interval = monitoring_interval
        self.logger = logging.getLogger('ResourceMonitor')
    
    def monitor_resources(self) -> Dict[str, Any]:
        """
        Collect comprehensive system resource metrics
        """
        return {
            'timestamp': time.time(),
            'cpu': {
                'usage': psutil.cpu_percent(interval=1),
                'cores': psutil.cpu_count(logical=False),
                'logical_cores': psutil.cpu_count(logical=True)
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'used_percent': psutil.virtual_memory().percent
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'free': psutil.disk_usage('/').free,
                'used_percent': psutil.disk_usage('/').percent
            },
            'network': {
                'bytes_sent': psutil.net_io_counters().bytes_sent,
                'bytes_recv': psutil.net_io_counters().bytes_recv
            }
        }
    
    def start_continuous_monitoring(self):
        """
        Start background monitoring thread
        """
        def monitor():
            while True:
                resources = self.monitor_resources()
                self.logger.info(f"System Resources: {resources}")
                time.sleep(self.monitoring_interval)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()