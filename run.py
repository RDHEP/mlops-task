import argparse
import yaml
import pandas as pd
import numpy as np
import json
import logging
import time
import os


def get_arguments():
    parser = argparse.ArgumentParser(description="MLOps Task")

    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--config", required=True, help="Configuration YAML file")
    parser.add_argument("--output", required=True, help="Output metrics JSON")
    parser.add_argument("--log-file", required=True, help="Log file")

    return parser.parse_args()


def load_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    return config


def validate_config(config):
    required_fields = ["seed", "window", "version"]

    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")

    print("Configuration validation successful!")

def load_dataset(input_path):

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file '{input_path}' not found.")

    # Read the file as a single text column
    data = pd.read_csv(input_path, header=None)

    # Split each row on commas
    data = data[0].str.split(",", expand=True)

    # First row contains the column names
    data.columns = data.iloc[0]

    # Remove the header row from the data
    data = data[1:].reset_index(drop=True)

    # Clean up column names
    data.columns = data.columns.str.strip().str.lower()

    # Convert numeric columns
    numeric_cols = ["open", "high", "low", "close", "volume_btc", "volume_usd"]

    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col])

    return data

def calculate_rolling_mean(data, window):

    data["rolling_mean"] = data["close"].rolling(window=window).mean()

    return data

def generate_signal(data):

    data["signal"] = (data["close"] > data["rolling_mean"]).astype(int)

    return data


if __name__ == "__main__":
    args = get_arguments()

    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    start_time = time.time()

    config = load_config(args.config)

    validate_config(config)
    logging.info("Configuration loaded successfully.")

    data = load_dataset(args.input)
    logging.info(f"Dataset loaded successfully with {len(data)} rows.")

    data = calculate_rolling_mean(data, config["window"])

    data = generate_signal(data)

    print("Input File :", args.input)
    print("Config File:", args.config)
    print("Output File:", args.output)
    print("Log File   :", args.log_file)

    print("\nConfiguration Loaded")
    print("Seed    :", config["seed"])
    print("Window  :", config["window"])
    print("Version :", config["version"])

    print("\nDataset Loaded Successfully!")
    print("Rows    :", len(data))
    print("Columns :", list(data.columns))

    print("\nFirst 10 rows:")
    print(data[["close", "rolling_mean", "signal"]].head(10))

    rows_processed = len(data)
    signal_rate = data["signal"].mean()
    print("Rows Processed:", rows_processed)
    print("Signal Rate:", signal_rate)


    end_time = time.time()
    latency_ms = (end_time - start_time) * 1000
    metrics = {
        "rows_processed": rows_processed,
        "signal_rate": float(round(signal_rate, 4)),
        "latency_ms": float(round(latency_ms, 2))
    }
    logging.info("Metrics calculated successfully.")
    print("\nMetrics Dictionary:")
    print(metrics)
    with open(args.output, "w") as file:
        json.dump(metrics, file, indent=4)
    logging.info(f"Metrics saved to {args.output}.")
    print("\nMetrics saved successfully!")
    print("\nLatency:", latency_ms, "ms")

