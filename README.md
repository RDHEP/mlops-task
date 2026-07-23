# MLOps Task

## Overview

This project processes financial time-series data using Python.

### Features

- Loads configuration from YAML
- Reads CSV dataset
- Calculates rolling mean
- Generates trading signals
- Saves metrics to JSON
- Logs execution
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

```bash
docker build -t mlops-task .
docker run --rm mlops-task
```
