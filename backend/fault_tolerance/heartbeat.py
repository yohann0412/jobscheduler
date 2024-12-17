import threading
import time
import logging
from typing import Dict, Any, Callable

class HeartbeatMonitor:
    """
    Monitor node health and manage fault tolerance
    """
    def __init__(self, 
                 node_registry=None, 
                 check_interval: int = 30, 
                 max_missed_heartbeats: int = 3):
        self.node_registry = node_registry
        self.check_interval = check_interval
        self.max_missed_heartbeats = max_missed_heartbeats
        self.logger = logging.getLogger('HeartbeatMonitor')
        self.node_health = {}
    
    def start_monitoring(self):
        """
        Start background heartbeat monitoring
        """
        def monitor():
            while True:
                if self.node_registry is not None:
                    self._check_node_health()
                else:
                    self.logger.warning("Node registry is not set, skipping heartbeat monitoring.")
                    time.sleep(self.check_interval)
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def _check_node_health(self):
        """
        Check health of all registered nodes
        """
        active_nodes = self.node_registry.get_active_nodes()
        
        for node in active_nodes:
            node_id = node['id']
            last_heartbeat = node.get('last_heartbeat', 0)
            
            # Track missed heartbeats
            if node_id not in self.node_health:
                self.node_health[node_id] = {
                    'missed_beats': 0,
                    'status': 'HEALTHY'
                }
            
            time_since_last_beat = time.time() - last_heartbeat
            
            if time_since_last_beat > self.check_interval:
                self.node_health[node_id]['missed_beats'] += 1
                
                if (self.node_health[node_id]['missed_beats'] > 
                    self.max_missed_heartbeats):
                    self._handle_node_failure(node_id)
            else:
                # Reset missed beats if node responds
                self.node_health[node_id]['missed_beats'] = 0
                self.node_health[node_id]['status'] = 'HEALTHY'
    
    def _handle_node_failure(self, node_id: str):
        """
        Handle node that has missed too many heartbeats
        """
        self.logger.warning(f"Node {node_id} is considered failed")
        
        # Mark node as inactive
        if self.node_registry is not None:
            self.node_registry.mark_node_inactive(node_id)
        
        # Trigger node recovery or job redistribution
        self._redistribute_node_jobs(node_id)
    
    def _redistribute_node_jobs(self, failed_node_id: str):
        """
        Redistribute jobs from failed node
        """
        # Retrieve and redistribute jobs from failed node
        if self.node_registry is not None:
            failed_node_jobs = self.node_registry.get_node_jobs(failed_node_id)
            
            # Find alternative nodes for job redistribution
            active_nodes = self.node_registry.get_active_nodes()
            
            if active_nodes:
                for job in failed_node_jobs:
                    target_node = self._select_alternative_node(active_nodes)
                    target_node.receive_jobs([job])
    
    def _select_alternative_node(self, nodes: Dict[str, Any]) -> Any:
        """
        Select an alternative node for job redistribution
        """
        # Simple load balancing strategy
        return min(nodes, key=lambda node: node.get('current_load', 0))