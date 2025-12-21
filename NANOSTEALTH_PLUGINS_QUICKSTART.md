# NanoStealth Plugin System - Quick Start

## Overview

The NanoStealth Plugin System provides modular, loosely-coupled components that extend platform capabilities without bloating the core engine. Each plugin communicates via JSON with clear contracts and can be swapped or extended independently.

## Installation

```bash
# Install core dependencies
pip install -r requirements-nanostealth.txt

# Install plugin-specific dependencies (optional)
pip install boto3              # For object storage
pip install paho-mqtt          # For MQTT messaging
pip install prometheus-client  # For metrics export
```

## Quick Examples

### 1. Log an Experiment Run

```python
from nanostealth.plugins.data_logging import ExperimentLogger
from nanostealth.plugins.base import PluginConfig

# Configure plugin
config = PluginConfig(
    name="experiment_logger",
    enabled=True,
    config={
        "storage_backend": "sqlite",
        "data_dir": "./data/experiments"
    }
)

# Initialize and use
logger = ExperimentLogger(config)
logger.initialize()

# Log experiment
result = logger.process({
    "run_id": "run_001",
    "timestamp": "2025-12-18T10:30:00Z",
    "formulation": {"polymer": "PLGA", "drug": "Doxorubicin"},
    "codex_scores": {"trueness": 0.75, "flow": 0.68, "toxicity": 0.22}
})

print(f"Logged: {result['run_id']}")
logger.shutdown()
```

### 2. Measure with Sensor

```python
from nanostealth.plugins.hardware import SensorMicroservice

config = PluginConfig(
    name="sensor",
    config={"simulation_mode": True}
)

sensor = SensorMicroservice(config)
sensor.initialize()

# Measure particle size
result = sensor.process({
    "action": "measure",
    "sensor_type": "dls",
    "sample_id": "sample_123"
})

print(f"Size: {result['data']['value']} {result['data']['unit']}")
sensor.shutdown()
```

### 3. Publish Event to Message Bus

```python
from nanostealth.plugins.orchestration import MessageBusPlugin

config = PluginConfig(
    name="message_bus",
    config={
        "bus_type": "mqtt",
        "mqtt": {"broker": "localhost", "port": 1883}
    }
)

bus = MessageBusPlugin(config)
bus.initialize()

# Publish run completion
bus.process({
    "action": "publish",
    "event_type": "run_completed",
    "payload": {"run_id": "run_001", "trueness": 0.75}
})

bus.shutdown()
```

## Available Plugins

### Data & Logging
- **ExperimentLogger**: Store runs in Postgres/SQLite + Parquet
- **MetricsDashboard**: Analytics with Prometheus export

### Storage
- **ObjectStoragePlugin**: S3/MinIO for raw data files
- **DataIngestService**: Auto-register files from WebDAV/SMB

### Hardware
- **SensorMicroservice**: Unified sensor interface (DLS, pH, spectroscopy)
- **ActuatorMicroservice**: Control pumps, valves, shakers

### Orchestration
- **MessageBusPlugin**: Event-driven messaging (MQTT/NATS)
- **WorkflowOrchestrator**: Multi-step workflow execution

## Configuration

Edit `config/nanostealth_plugins.json` to configure plugins:

```json
{
  "nanostealth_plugins": {
    "plugins": {
      "experiment_logger": {
        "enabled": true,
        "type": "data_logging.ExperimentLogger",
        "config": {
          "storage_backend": "postgresql",
          "data_dir": "./data/experiments"
        }
      }
    }
  }
}
```

## Running the Demo

```bash
# Run the comprehensive demo script
python examples/plugin_system_demo.py

# This demonstrates:
# - Experiment logging
# - Metrics tracking
# - Sensor measurements
# - Event publishing
# - Workflow orchestration
```

## Next Steps

1. **Full Documentation**: See [`docs/NANOSTEALTH_PLUGINS.md`](docs/NANOSTEALTH_PLUGINS.md)
2. **Integration Guide**: See [`docs/NANOSTEALTH_INTEGRATION.md`](docs/NANOSTEALTH_INTEGRATION.md)
3. **Architecture**: See [`docs/NANOSTEALTH.md`](docs/NANOSTEALTH.md)

## Plugin Development

Create a new plugin by inheriting from `BasePlugin`:

```python
from nanostealth.plugins.base import BasePlugin, PluginConfig

class MyCustomPlugin(BasePlugin):
    def initialize(self) -> bool:
        # Setup code
        self.status = PluginStatus.ACTIVE
        return True
    
    def shutdown(self) -> bool:
        # Cleanup code
        self.status = PluginStatus.STOPPED
        return True
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Main logic
        return {
            "success": True,
            "data": {"result": "processed"}
        }
```

## Support

- **Documentation**: [docs/NANOSTEALTH_PLUGINS.md](docs/NANOSTEALTH_PLUGINS.md)
- **Issues**: https://github.com/ncsound919/Overlay-Bioware/issues
- **Examples**: See `examples/` directory

## License

MIT License - See LICENSE file for details
