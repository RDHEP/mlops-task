# MLOps Task

## Overview

This project processes financial time-series data using Python. It reads market data from a CSV file, calculates a rolling mean over the closing prices, generates trading signals, records execution metrics, and logs the execution. The application can be run locally or inside a Docker container.

## Features

- Loads configuration from a YAML file
- Reads financial time-series data from CSV
- Calculates rolling mean
- Generates trading signals
- Measures execution latency
- Saves metrics to `metrics.json`
- Logs execution details to `run.log`
- Runs inside Docker

## Requirements

- Python 3.12
- pandas
- numpy
- PyYAML

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

## Run with Docker

Build the Docker image:

```bash
docker build -t mlops-task .
```

Run the container:

```bash
docker run --rm mlops-task
```

## Output Files

The application generates:

- `metrics.json` – contains execution metrics in JSON format
- `run.log` – contains execution logs

Example `metrics.json`:

```json
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4989,
  "latency_ms": 40.29,
  "seed": 42,
  "status": "success"
}
```
