# Self-Healing Infrastructure System

A basic self-healing infrastructure system that automatically detects failures in Docker containers and performs recovery actions.

## Components

- **Prometheus**: Metrics collection
- **Alertmanager**: Alert triggering
- **Webhook Receiver**: Custom service that processes alerts and performs healing actions
- **cAdvisor**: Container metrics exporter
- **Sample Service**: Example service that exposes metrics and can be used for testing

## Architecture

1. Prometheus collects metrics from containers via cAdvisor
2. When metrics exceed thresholds, Prometheus fires alerts
3. Alertmanager receives these alerts and forwards them to the webhook receiver
4. The webhook receiver performs healing actions (container restart)

## Setup and Run

1. Clone this repository
2. Start the services:
```bash
docker-compose up -d
```

## Testing the Self-Healing

### Trigger a CPU/Memory Spike

```bash
# Memory spike
curl http://localhost:5000/memory-spike

# CPU spike
curl http://localhost:5000/cpu-spike
```

Alternatively, set the environment variable in docker-compose.yml:
```yaml
sample-service:
  environment:
    - SIMULATE_HIGH_LOAD=true
```

### Monitor the System

1. Access Prometheus UI: http://localhost:9090
2. Access Alertmanager UI: http://localhost:9093
3. View cAdvisor metrics: http://localhost:8080

## Logs

To check if the healing action was performed:
```bash
docker logs webhook-receiver
```

## Customization

You can modify the alert thresholds in `prometheus/rules.yml` to trigger healing at different values. 