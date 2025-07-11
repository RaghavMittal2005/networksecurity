import os
from datetime import datetime
import numpy as np
import pandas as pd
"""
Some Constants to used in data ingestion
"""
TARGET_COLUMN:str="Result"
ARTIFACTS_DIR:str="Artifacts"
PIPELINE_NAME:str="NetworkSecurity"
FILE_NAME:str="NetworkData.csv"
TEST_FILE:str="test.csv"
TRAIN_FILE:str="train.csv"
SCHEMA_PATH:str=os.path.join("data_schema","schema.yaml")


DATA_INGESTION_COLLECTION_NAME:str="phisingData"
DATA_INGESTION_DATBASE_NAME:str="Raghav"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_VALID_DIR:str="validated"
DATA_VALIDATION_INVALID_DIR:str="invalidated"
DATA_VALIDATION_DRIFT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE:str="report.yaml"

DATA_TRANSFORMATION_DIR:str="data_transformation"
DATA_TRANSFORMATION_OBJECT_DIR:str="transformed_object"
DATA_TRANSFORMATION_DATA_DIR:str="transformed_data"
PREPROCESS_FILE:str="preprocessing.pkl"
DATA_TRANSFORMATION_PARAMS:dict={
    "missing_values":np.nan,
    "weights":"uniform",
    "n_neighbors":3
}

