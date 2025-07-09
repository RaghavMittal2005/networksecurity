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



DATA_INGESTION_COLLECTION_NAME:str="phisingData"
DATA_INGESTION_DATBASE_NAME:str="Raghav"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_NAME:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2
