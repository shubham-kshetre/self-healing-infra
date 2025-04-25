#!/usr/bin/env python3
import os
import time
import threading
import logging
from flask import Flask, jsonify
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Counter('sample_request_count', 'App Request Count')
MEMORY_USAGE = Gauge('sample_memory_usage', 'Memory Usage Simulation')
CPU_USAGE = Gauge('sample_cpu_usage', 'CPU Usage Simulation')
REQUEST_LATENCY = Histogram('sample_request_latency_seconds', 'Request latency in seconds')

# Initialize with normal values
MEMORY_USAGE.set(50)  # 50% usage
CPU_USAGE.set(20)     # 20% usage

def simulate_load():
    """
    Simulate changing load patterns over time
    """
    while True:
        try:
            # Normally low usage with occasional spikes
            if os.environ.get('SIMULATE_HIGH_LOAD') == 'true':
                # Simulate high load for testing self-healing
                MEMORY_USAGE.set(90)  # 90% usage (high)
                CPU_USAGE.set(90)     # 90% usage (high)
                logger.info("Simulating high resource usage...")
            else:
                # Normal operation with slight variations
                import random
                memory = random.randint(30, 70)
                cpu = random.randint(10, 50)
                MEMORY_USAGE.set(memory)
                CPU_USAGE.set(cpu)
                logger.info(f"Normal operation - Memory: {memory}%, CPU: {cpu}%")
            
            time.sleep(15)  # Update every 15 seconds
        except Exception as e:
            logger.error(f"Error in load simulation: {str(e)}")
            time.sleep(5)

@app.route('/')
def index():
    REQUEST_COUNT.inc()
    with REQUEST_LATENCY.time():
        return jsonify({
            "status": "running", 
            "memory": MEMORY_USAGE._value.get(), 
            "cpu": CPU_USAGE._value.get()
        })

@app.route('/memory-spike')
def memory_spike():
    """Endpoint to trigger a memory spike for testing"""
    MEMORY_USAGE.set(95)
    logger.warning("Memory spike triggered")
    return jsonify({"status": "memory spike triggered", "memory": 95})

@app.route('/cpu-spike')
def cpu_spike():
    """Endpoint to trigger a CPU spike for testing"""
    CPU_USAGE.set(95)
    logger.warning("CPU spike triggered")
    return jsonify({"status": "cpu spike triggered", "cpu": 95})

if __name__ == '__main__':
    # Start Prometheus metrics server on port 8000
    start_http_server(8080)
    logger.info("Prometheus metrics server started on port 8080")
    
    # Start the load simulation in a separate thread
    load_thread = threading.Thread(target=simulate_load, daemon=True)
    load_thread.start()
    logger.info("Load simulation started")
    
    # Start Flask app on port 5000
    app.run(host='0.0.0.0', port=5000) 