# NanoStealth Modular Plugins

## Overview

NanoStealth plugins are small, modular components that extend the core platform's capabilities without bloating the main engine. Each plugin is loosely coupled, communicates via JSON, and can be swapped or extended independently.

## Architecture Principles

1. **Loose Coupling**: Plugins communicate via JSON input/output with clear contracts
2. **Modularity**: Each plugin handles a specific concern (data, hardware, orchestration, AI)
3. **Swappable**: Plugins can be replaced without affecting the core engine
4. **Observable**: All plugins report status and health metrics
5. **Scalable**: Plugins can run as independent microservices

## Plugin Categories

### Data and Logging Components

#### Experiment Logger
**Purpose**: Stores each run (inputs, Codex scores, outputs, lab measurements) in structured storage (Postgres/SQLite + Parquet).

**Features**:
- Full provenance tracking for audit and replay
- Support for PostgreSQL (production) or SQLite (dev)
- Optional Parquet export for time-series analysis
- Queryable run history with filters

**Contract Example**:
```json
{
  "run_id": "run_2025_001",
  "timestamp": "2025-12-18T10:30:00Z",
  "formulation": {
    "polymer": "PLGA",
    "drug": "Doxorubicin",
    "drug_loading": 5.0,
    "particle_size": 100.0,
    "surface_modification": "PEG"
  },
  "codex_scores": {
    "trueness": 0.75,
    "flow": 0.68,
    "toxicity": 0.22
  },
  "lab_measurements": {
    "actual_size": 102.5,
    "pdi": 0.12,
    "zeta_potential": -25.3
  }
}
```

#### Metrics Dashboard
**Purpose**: Lightweight analytics layer to visualize Trueness/Flow/Toxicity over time and across projects.

**Features**:
- Prometheus metrics export for Grafana integration
- Time-series analytics with statistics
- Benchmark tracking across engine versions
- Performance monitoring (latency, iterations, error rates)

**Prometheus Metrics Exported**:
- `nanostealth_trueness`: Targeting accuracy score
- `nanostealth_flow`: Circulation kinetics score
- `nanostealth_toxicity`: Off-target toxicity score
- `nanostealth_latency_seconds`: Processing latency
- `nanostealth_optimizer_iterations`: Optimizer convergence
- `nanostealth_runs_total`: Total runs counter
- `nanostealth_errors_total`: Error counter by type

### Storage Components

#### Object Storage Plugin
**Purpose**: S3-compatible (MinIO) storage for raw data with metadata tracking in Postgres.

**Features**:
- Upload/download files to S3-compatible storage
- Automatic content hashing (SHA256)
- Metadata searchability via PostgreSQL
- Presigned URLs for secure access
- Support for AWS S3, MinIO, or other S3-compatible services

**Use Cases**:
- Store instrument raw data files
- Archive experimental results
- Share data with collaborators
- Long-term retention for compliance

#### Data Ingest Service
**Purpose**: Mounts lab/cloud drives via WebDAV/SMB and auto-registers new files with hashes and timestamps.

**Features**:
- Automatic file discovery and registration
- Content hash tracking for deduplication
- Directory watching for new files
- Metadata association with experiments
- Integration with object storage for archival

### Hardware and Sensing Components

#### Sensor Microservice
**Purpose**: Python/MCU bridge abstracting physical measurements (spectroscopy, turbidity, DLS, pH) via HTTP or MQTT API.

**Features**:
- Unified interface for diverse sensors
- Simulation mode for testing without hardware
- MQTT support for async measurements
- Calibration tracking
- Error handling and retry logic

**Supported Sensors**:
- Dynamic Light Scattering (DLS)
- Spectroscopy (UV-Vis, fluorescence)
- Turbidity meters
- pH meters
- Zeta potential analyzers
- Temperature sensors

#### Actuator Microservice
**Purpose**: Control pumps, valves, shakers, or 3D-printed fixtures via Arduino/ESP32.

**Features**:
- Request/response pattern matching sensors
- Safe shutdown with all-stop capability
- State tracking for actuators
- Simulation mode for development
- Extensible for custom actuators

### Orchestration and Workflow Components

#### Message Bus Plugin
**Purpose**: Event-driven architecture using MQTT/NATS/RabbitMQ for system-wide events.

**Features**:
- Pub/sub messaging for decoupled components
- Standard event types (run_completed, hardware_measurement_ready, benchmark_finished)
- Event history for debugging
- Callback subscriptions for HTTP endpoints
- Extensible for custom events

**Standard Events**:
- `run_completed`: Optimization run finished successfully
- `run_failed`: Optimization run failed with error
- `hardware_measurement_ready`: Sensor measurement available
- `benchmark_finished`: Performance benchmark completed
- `optimization_converged`: Optimizer reached convergence
- `sensor_calibrated`: Sensor calibration completed
- `actuator_error`: Actuator encountered error
- `storage_uploaded`: File uploaded to object storage

#### Workflow Orchestrator
**Purpose**: HTTP/gRPC wrapper exposing NanoStealth for workflow engines (IvoryOS, Windmill).

**Features**:
- Sequential workflow execution
- Service registry for available components
- Integration with external workflow engines
- Step-by-step result tracking
- Failure handling and recovery

## Installation

### Prerequisites

```bash
# Python 3.11+
python --version

# PostgreSQL (for metadata)
psql --version

# MinIO or S3-compatible storage
mc --version

# MQTT Broker (Mosquitto)
mosquitto --version
```

### Install Plugin Dependencies

```bash
# Install NanoStealth with all plugin dependencies
pip install -r requirements-nanostealth.txt

# Optional: Install plugin-specific dependencies
pip install boto3  # For object storage
pip install paho-mqtt  # For MQTT messaging
pip install prometheus-client  # For metrics export
```

### Configure Plugins

1. Copy the plugin configuration template:
```bash
cp config/nanostealth_plugins.json config/nanostealth_plugins.local.json
```

2. Edit `config/nanostealth_plugins.local.json` with your settings:
   - Database credentials
   - S3/MinIO endpoints
   - MQTT broker address
   - Enable/disable specific plugins

3. Set environment variables:
```bash
export POSTGRES_PASSWORD=your_password
export S3_ACCESS_KEY=your_access_key
export S3_SECRET_KEY=your_secret_key
export MQTT_USERNAME=your_mqtt_user
export MQTT_PASSWORD=your_mqtt_password
```

## Usage Examples

### Example 1: Log an Experiment Run

```python
from nanostealth.plugins import PluginRegistry
from nanostealth.plugins.data_logging import ExperimentLogger
from nanostealth.plugins.base import PluginConfig

# Create plugin configuration
config = PluginConfig(
    name="experiment_logger",
    enabled=True,
    config={
        "storage_backend": "postgresql",
        "data_dir": "./data/experiments",
        "enable_parquet": True,
        "postgresql": {
            "host": "localhost",
            "port": 5432,
            "database": "nanostealth",
            "user": "nanostealth",
            "password": "your_password"
        }
    }
)

# Create and initialize plugin
logger = ExperimentLogger(config)
logger.initialize()

# Log a run
result = logger.process({
    "run_id": "run_2025_001",
    "timestamp": "2025-12-18T10:30:00Z",
    "formulation": {
        "polymer": "PLGA",
        "drug": "Doxorubicin",
        "drug_loading": 5.0,
        "particle_size": 100.0
    },
    "codex_scores": {
        "trueness": 0.75,
        "flow": 0.68,
        "toxicity": 0.22
    },
    "lab_measurements": {
        "actual_size": 102.5,
        "pdi": 0.12
    }
})

print(result)
# Output: {"success": True, "run_id": "run_2025_001", ...}
```

### Example 2: Measure with Sensor

```python
from nanostealth.plugins.hardware import SensorMicroservice
from nanostealth.plugins.base import PluginConfig

config = PluginConfig(
    name="sensor_service",
    enabled=True,
    config={
        "communication_mode": "mqtt",
        "simulation_mode": True
    }
)

sensor = SensorMicroservice(config)
sensor.initialize()

# Perform DLS measurement
result = sensor.process({
    "action": "measure",
    "sensor_type": "dls",
    "sample_id": "sample_123",
    "parameters": {
        "num_reads": 5
    }
})

print(result)
# Output: {"success": True, "data": {"value": 100.2, "unit": "nm", ...}}
```

### Example 3: Publish Event to Message Bus

```python
from nanostealth.plugins.orchestration import MessageBusPlugin
from nanostealth.plugins.base import PluginConfig

config = PluginConfig(
    name="message_bus",
    enabled=True,
    config={
        "bus_type": "mqtt",
        "mqtt": {
            "broker": "localhost",
            "port": 1883
        }
    }
)

bus = MessageBusPlugin(config)
bus.initialize()

# Publish run completion event
result = bus.process({
    "action": "publish",
    "event_type": "run_completed",
    "payload": {
        "run_id": "run_2025_001",
        "trueness": 0.75,
        "flow": 0.68
    },
    "metadata": {
        "source": "nanostealth_core",
        "run_id": "run_2025_001"
    }
})

print(result)
# Output: {"success": True, "message": "Event run_completed published"}
```

### Example 4: Upload to Object Storage

```python
from nanostealth.plugins.storage import ObjectStoragePlugin
from nanostealth.plugins.base import PluginConfig

config = PluginConfig(
    name="object_storage",
    enabled=True,
    config={
        "default_bucket": "nanostealth-data",
        "s3": {
            "endpoint_url": "http://localhost:9000",
            "access_key": "minioadmin",
            "secret_key": "minioadmin"
        }
    }
)

storage = ObjectStoragePlugin(config)
storage.initialize()

# Upload a file
result = storage.process({
    "action": "upload",
    "file_path": "/path/to/data.csv",
    "object_key": "experiments/run_2025_001/data.csv",
    "metadata": {
        "run_id": "run_2025_001",
        "experiment_type": "optimization",
        "instrument": "DLS"
    }
})

print(result)
# Output: {"success": True, "data": {"url": "...", "content_hash": "...", ...}}
```

### Example 5: Execute Workflow

```python
from nanostealth.plugins.orchestration import WorkflowOrchestrator
from nanostealth.plugins.base import PluginConfig

config = PluginConfig(
    name="orchestrator",
    enabled=True,
    config={"engine_type": "builtin"}
)

orchestrator = WorkflowOrchestrator(config)
orchestrator.initialize()

# Execute a multi-step workflow
result = orchestrator.process({
    "action": "execute",
    "workflow_id": "optimization_workflow_v1",
    "steps": [
        {
            "step_id": "formulate",
            "service": "opentrons",
            "operation": "synthesize",
            "parameters": {"polymer": "PLGA", "drug_load": 5.0}
        },
        {
            "step_id": "characterize",
            "service": "sensor",
            "operation": "measure_dls",
            "parameters": {"sample_id": "sample_123"}
        },
        {
            "step_id": "optimize",
            "service": "nanostealth",
            "operation": "optimize_formulation",
            "parameters": {"target_trueness": 0.75}
        }
    ]
})

print(result)
# Output: {"success": True, "data": {"execution_id": "...", "status": "completed", ...}}
```

## Integration with Core NanoStealth

### Plugin Registry Pattern

```python
from nanostealth.plugins import PluginRegistry
from nanostealth.plugins.data_logging import ExperimentLogger, MetricsDashboard
from nanostealth.plugins.hardware import SensorMicroservice, ActuatorMicroservice

# Create registry
registry = PluginRegistry()

# Register plugin classes
registry.register_plugin_class("experiment_logger", ExperimentLogger)
registry.register_plugin_class("metrics_dashboard", MetricsDashboard)
registry.register_plugin_class("sensor", SensorMicroservice)
registry.register_plugin_class("actuator", ActuatorMicroservice)

# Create plugin instances from config
logger_config = PluginConfig(name="logger", enabled=True, config={...})
logger = registry.create_plugin("experiment_logger", logger_config)

# Get active plugins
active_plugins = registry.get_active_plugins()

# Get registry status
status = registry.get_registry_status()
```

## Monitoring and Observability

### Prometheus Metrics

Metrics are exposed at `/metrics` endpoint for Prometheus scraping:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'nanostealth'
    static_configs:
      - targets: ['localhost:8001']
    scrape_interval: 15s
```

### Grafana Dashboards

Import pre-built dashboards from `config/grafana-dashboards/`:
- `nanostealth-metrics.json`: Trueness/Flow/Toxicity time-series
- `nanostealth-performance.json`: Latency and throughput metrics
- `nanostealth-benchmarks.json`: Version comparison and improvement tracking

## Best Practices

1. **Always validate inputs**: Check required fields before processing
2. **Handle errors gracefully**: Return structured error responses
3. **Log important events**: Use structured logging for debugging
4. **Monitor resource usage**: Track memory and CPU for long-running plugins
5. **Test with simulation mode**: Develop without hardware dependencies
6. **Version your contracts**: Document JSON input/output schemas
7. **Use environment variables**: Never hardcode credentials

## Troubleshooting

### Plugin won't initialize
- Check database connectivity
- Verify credentials in environment variables
- Review plugin logs for specific errors

### MQTT connection failed
- Ensure MQTT broker is running: `mosquitto -v`
- Check firewall rules for port 1883
- Verify credentials if authentication is enabled

### Object storage errors
- Test MinIO/S3 connectivity: `mc ls myminio`
- Verify bucket exists and permissions are correct
- Check endpoint URL format

## Contributing

To add a new plugin:

1. Create plugin class inheriting from `BasePlugin`
2. Implement `initialize()`, `shutdown()`, and `process()` methods
3. Define clear JSON contracts in docstring
4. Add configuration to `nanostealth_plugins.json`
5. Write tests for plugin functionality
6. Update this documentation

## License

MIT License - See LICENSE file for details

## Support

- Documentation: https://github.com/ncsound919/Overlay-Bioware/docs
- Issues: https://github.com/ncsound919/Overlay-Bioware/issues
- Community: Join discussions in project forums
