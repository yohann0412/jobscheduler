# File: distributed-job-scheduler/backend/performance/benchmarking.py

import time
import multiprocessing
import random
from typing import Dict, Any, List, Callable

class SystemBenchmark:
    """
    Comprehensive system benchmarking utility
    """
    @staticmethod
    def cpu_benchmark(duration: int = 10) -> Dict[str, Any]:
        """
        Measure CPU performance through intensive computation
        """
        def cpu_intensive_task():
            """Generate prime numbers to stress CPU"""
            def is_prime(n):
                if n < 2:
                    return False
                for i in range(2, int(n ** 0.5) + 1):
                    if n % i == 0:
                        return False
                return True
            
            primes = []
            start_time = time.time()
            while time.time() - start_time < duration:
                num = random.randint(10000, 100000)
                if is_prime(num):
                    primes.append(num)
            
            return len(primes)
        
        start_time = time.time()
        
        # Use all available CPU cores
        with multiprocessing.Pool() as pool:
            results = pool.map(
                lambda _: cpu_intensive_task(), 
                range(multiprocessing.cpu_count())
            )
        
        end_time = time.time()
        
        return {
            'total_primes_found': sum(results),
            'execution_time': end_time - start_time,
            'cpu_cores_used': multiprocessing.cpu_count()
        }
    
    @staticmethod
    def memory_benchmark(memory_size: int = 100_000_000) -> Dict[str, Any]:
        """
        Measure memory allocation and access performance
        """
        start_time = time.time()
        
        # Create large list and perform operations
        large_list = [random.random() for _ in range(memory_size)]
        
        # Simulate memory-intensive operations
        sum_result = sum(large_list)
        sorted_result = sorted(large_list)
        
        end_time = time.time()
        
        return {
            'memory_size': memory_size,
            'sum_result': sum_result,
            'execution_time': end_time - start_time,
            'memory_used': len(large_list) * 8  # Assuming 8 bytes per float
        }
    
    @staticmethod
    def io_benchmark(file_size: int = 1_000_000) -> Dict[str, Any]:
        """
        Measure I/O performance through file operations
        """
        import tempfile
        
        start_time = time.time()
        
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            # Write large random data
            data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=file_size))
            temp_file.write(data.encode())
            temp_file.flush()
            
            # Read back the data
            temp_file.seek(0)
            read_data = temp_file.read()
        
        end_time = time.time()
        
        return {
            'file_size': file_size,
            'write_read_time': end_time - start_time,
            'data_integrity': len(read_data) == file_size
        }
    
    def run_comprehensive_benchmark(self) -> Dict[str, Any]:
        """
        Run a complete system benchmark
        """
        return {
            'cpu_benchmark': self.cpu_benchmark(),
            'memory_benchmark': self.memory_benchmark(),
            'io_benchmark': self.io_benchmark(),
            'timestamp': time.time()
        }