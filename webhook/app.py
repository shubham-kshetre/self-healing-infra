#!/usr/bin/env python3
import json
import logging
import docker
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = docker.from_env()

def restart_container(container_name):
    """
    Restart a Docker container by name
    """
    try:
        logger.info(f"Attempting to restart container: {container_name}")
        container = client.containers.get(container_name)
        container.restart()
        logger.info(f"Successfully restarted container: {container_name}")
        return True
    except docker.errors.NotFound:
        logger.error(f"Container {container_name} not found")
        return False
    except Exception as e:
        logger.error(f"Error restarting container {container_name}: {str(e)}")
        return False

@app.route('/alert', methods=['POST'])
def receive_alert():
    """
    Endpoint to receive alerts from Alertmanager
    """
    try:
        data = request.json
        logger.info(f"Received alert: {json.dumps(data)}")
        
        # Process alerts
        if 'alerts' in data:
            for alert in data['alerts']:
                # Check if alert is firing (not resolved)
                if alert.get('status') == 'firing':
                    alert_name = alert.get('labels', {}).get('alertname')
                    container_name = 'sample-service'  # Default to our sample service
                    
                    # Take action based on alert type
                    if alert_name == 'HighCPUUsage':
                        logger.info(f"High CPU usage detected in {container_name}, restarting...")
                        restart_container(container_name)
                    
                    elif alert_name == 'HighMemoryUsage':
                        logger.info(f"High memory usage detected in {container_name}, restarting...")
                        restart_container(container_name)
                    
                    elif alert_name == 'ContainerDown':
                        logger.info(f"Container {container_name} is down, attempting to restart...")
                        restart_container(container_name)
        
        return jsonify({"status": "success", "message": "Alert processed"}), 200
    
    except Exception as e:
        logger.error(f"Error processing alert: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Simple health check endpoint
    """
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    logger.info("Starting webhook receiver service...")
    app.run(host='0.0.0.0', port=5000) 