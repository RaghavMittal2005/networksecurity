import os
import sys
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.entity_config import TrainingPipelineConfig
from networkSecurity.entity.entity_config import DataIngestionConfig
from networkSecurity.components.dataIngestion import DataIngestion
from datetime import datetime

if __name__=='__main__':
    try:
        trainconfig=TrainingPipelineConfig(datetime.now())
        dataingestconfig=DataIngestionConfig(trainconfig)
        data_ingestion=DataIngestion(dataingestconfig)
        logging.info("Ingestion initiated")
        ingestion_artifact=data_ingestion.initiate_dataIngestion()
        print(ingestion_artifact)


    except Exception as e:
        raise NetworkSecurityException(e,sys)