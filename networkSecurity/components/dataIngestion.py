import os
import sys
from typing import List
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from networkSecurity.entity.entity_config import DataIngestionConfig
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.artifact_config import IngestionPara
import pymongo
from pymongo import MongoClient

from dotenv import load_dotenv

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,dataIngestionconfig:DataIngestionConfig):
        try:
            self.dataIngestionconfig=dataIngestionconfig
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def raw_export_to_df(self):
        try:
            self.database_name=self.dataIngestionconfig.database_name
            self.collection_name=self.dataIngestionconfig.collection_name
            self.mongo_client=MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[self.database_name][self.collection_name]
            dataframe=pd.DataFrame(list(collection.find()))
            if "_id" in dataframe.columns.to_list():
                df=dataframe.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_to_feature_store(self,database:pd.DataFrame):
        try:
            feature_store_path=self.dataIngestionconfig.feature_store_path
            dir_path=os.path.dirname(feature_store_path)
            os.makedirs(dir_path,exist_ok=True)
            database.to_csv(feature_store_path,index=False,header=True)
            return database
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def train_test_split(self,database=pd.DataFrame):
        try:
            split_ratio=self.dataIngestionconfig.train_test_split_ratio
            train_data,test_data=train_test_split(database,test_size=split_ratio)
            logging.info("Data splitted")
            train_path=self.dataIngestionconfig.training_file_path
            os.makedirs(os.path.dirname(train_path), exist_ok=True)
            train_data.to_csv(train_path, index=False, header=True)

            test_path=self.dataIngestionconfig.testing_file_path
            os.makedirs(os.path.dirname(test_path),exist_ok=True)
            test_data.to_csv(test_path,index=False,header=True)
            logging.info("Exported test and train data")

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initiate_dataIngestion(self):
        try:
            database=self.raw_export_to_df()
            database=self.export_to_feature_store(database=database)
            self.train_test_split(database=database)
            
            ingestion_artifact=IngestionPara(training_path=self.dataIngestionconfig.training_file_path,testing_path=self.dataIngestionconfig.testing_file_path)
            return ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
