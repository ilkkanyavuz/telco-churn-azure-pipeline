import json
import logging
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import numpy as np
from azure.storage.blob import BlobServiceClient
# import requests  # will be used when we simulate an API call
# from azure.storage.blob import BlobServiceClient  # for Azure Blob upload

def load_config(config_path: str = "config.json") -> dict:
    """
    Load pipeline configuration from a JSON file.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def setup_logging(log_file: str) -> None:
    """
    Configure basic logging to file and console.
    """
    log_file_path = Path(log_file)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ],
    )

def fetch_data_from_api(api_url: str, timeout: int = 30) -> pd.DataFrame:
    """
    Load the Telco Customer Churn dataset from a local CSV file.
    Parameters are kept for future use when the pipeline is switched
    from a static CSV to a real HTTP API.
    """
    # Example: real API call pattern (kept as a reference for future use)
    # response = requests.get(api_url, timeout=timeout)
    # response.raise_for_status()
    # data_json = response.json()
    # df = pd.json_normalize(data_json)
    # logging.info("Loaded Telco churn data from API %s with shape %s", api_url, df.shape)
    # return df

    # Current implementation: simulate API by reading from local CSV
    csv_path = Path("data_source") / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found at {csv_path}")

    df = pd.read_csv(csv_path)
    logging.info("Loaded Telco churn data from %s with shape %s", csv_path, df.shape)
    return df

def save_raw_dataframe(df: pd.DataFrame, output_dir: str, file_prefix: str, date_format: str) -> Path:
    """
    Save the raw DataFrame to a CSV file in the raw layer and return the file path.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now(timezone.utc).strftime(date_format)
    file_name = f"{file_prefix}_{date_str}_raw.csv"
    full_path = output_path / file_name

    df.to_csv(full_path, index=False)
    logging.info("Saved raw data to %s", full_path)

    return full_path

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the Telco Customer Churn dataset to make it analysis-ready.

    - Convert TotalCharges to numeric.
    - Drop rows where tenure is 0 and TotalCharges is missing.
    - Map SeniorCitizen from 0/1 to "No"/"Yes".
    - Enforce numeric dtypes on key columns.
    """
    logging.info("Starting basic transformations on Telco churn dataset")
    # Work on a copy to avoid side effects on the original DataFrame
    df_processed = df.copy()

    # 1) TotalCharges: string -> numeric, invalid values become NaN
    df_processed["TotalCharges"] = pd.to_numeric(
        df_processed["TotalCharges"], errors="coerce"
    )

    # 2) Drop rows where tenure is 0 and TotalCharges is NaN (very new customers)
    mask_tenure_zero = df_processed["tenure"] == 0
    mask_total_missing = df_processed["TotalCharges"].isna()
    rows_to_drop = df_processed[mask_tenure_zero & mask_total_missing]

    if not rows_to_drop.empty:
        logging.info(
            "Dropping %d rows with tenure=0 and missing TotalCharges",
            len(rows_to_drop),
        )
        df_processed = df_processed.drop(rows_to_drop.index)

    # 3) SeniorCitizen: 0/1 -> "No"/"Yes" for readability in reports
    df_processed["SeniorCitizen"] = df_processed["SeniorCitizen"].map(
        {0: "No", 1: "Yes"}
    )

    # 4) Ensure numeric dtypes on key numeric columns
    numeric_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    for col in numeric_cols:
        df_processed[col] = pd.to_numeric(df_processed[col], errors="coerce")

    logging.info("Finished transformations. Processed shape: %s", df_processed.shape)

    # 5) Create tenure segments for analysis (0-12, 13-24, 25-36, 36+)
    bins = [0, 12, 24, 36, np.inf]
    labels = ["0-12", "13-24", "25-36", "36+"]

    df_processed["segment_tenure"] = pd.cut(
        df_processed["tenure"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )

    logging.info("Added segment_tenure column for tenure bucketing")

    return df_processed

def save_processed_dataframe(df: pd.DataFrame, output_dir: str, file_prefix: str, date_format: str) -> Path:
    """
    Save the processed DataFrame to a CSV file in the processed layer and return the file path.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now(timezone.utc).strftime(date_format)
    file_name = f"{file_prefix}_{date_str}_processed.csv"
    full_path = output_path / file_name

    df.to_csv(full_path, index=False)
    logging.info("Saved processed data to %s", full_path)

    return full_path


def upload_file_to_azure_blob(
    local_path: Path,
    connection_string: str,
    container_name: str,
    folder: str,
) -> None:
    """
    Upload a local file to Azure Blob Storage under the given container and folder.

    The blob name is built from the folder prefix and the local file name, so that we can
    keep a simple raw/processed/archive structure inside the container.
    """
    if not local_path.exists():
        logging.warning("Local file does not exist, skipping upload: %s", local_path)
        return

    # 1) Connect to Blob
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # 2) Get container client
    container_client = blob_service_client.get_container_client(container_name)

    # 3) Create blob folder
    blob_name = f"{folder}/{local_path.name}"

    logging.info("Uploading %s to container %s as blob %s", local_path, container_name, blob_name)

    # 4) Open file and upload
    with open(local_path, "rb") as data:
        container_client.upload_blob(
            name=blob_name,
            data=data,
            overwrite=True,
        )

    logging.info("Upload completed: %s", blob_name)


def main() -> None:
    """
    Orchestrate the Telco churn data ingestion:
    1) load config, 2) fetch data, 3) save raw, 4) transform,
    5) save processed, 6) upload both to Azure Blob.
    """
    config = load_config()

    setup_logging(config["paths"]["log_file"])
    logger = logging.getLogger("telco_churn_ingestion")
    logger.info("Starting Telco churn ingestion pipeline")

    # Read settings from config
    api_url = config["api"]["base_url"]
    timeout = config["api"]["timeout_seconds"]

    raw_dir = config["paths"]["local_raw_dir"]
    processed_dir = config["paths"]["local_processed_dir"]

    file_prefix = config["ingestion"]["file_prefix"]
    date_format = config["ingestion"]["date_format"]

    container_name = config["azure_blob"]["container_name"]
    raw_folder = config["azure_blob"]["raw_folder"]
    processed_folder = config["azure_blob"]["processed_folder"]
    connection_string = config["azure_blob"]["connection_string"]

    # Normally we would read the connection string from an environment variable
    # import os
    # connection_string = os.getenv(connection_string_env)

    try:
        # 1) Fetch data
        logger.info("Fetching data from API: %s", api_url)
        df_raw = fetch_data_from_api(api_url, timeout)

        # 2) Save raw
        raw_file_path = save_raw_dataframe(df_raw, raw_dir, file_prefix, date_format)

        # 3) Transform
        df_processed = transform_data(df_raw)

        # 4) Save processed
        processed_file_path = save_processed_dataframe(df_processed, processed_dir, file_prefix, date_format)

        # 5) Upload to Azure Blob
        logger.info("Uploading files to Azure Blob Storage")
        upload_file_to_azure_blob(raw_file_path, connection_string, container_name, raw_folder)
        upload_file_to_azure_blob(processed_file_path, connection_string, container_name, processed_folder)

        logger.info("Telco churn ingestion pipeline completed successfully")

    except Exception as e:
        logger.exception("Telco churn ingestion pipeline failed: %s", e)
        # In a real production scenario, we might re-raise the exception
        # or notify an alerting system.


if __name__ == "__main__":
    main()