import os
import sys
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.entity_config import TrainingPipelineConfig
from networkSecurity.entity.entity_config import DataIngestionConfig,DataValidationConfig
from networkSecurity.entity.artifact_config import IngestionPara,DataValidationArtifact
from networkSecurity.components.dataIngestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation
from datetime import datetime

if __name__=='__main__':
    try:
        trainconfig=TrainingPipelineConfig(datetime.now())
        dataingestconfig=DataIngestionConfig(trainconfig)
        data_ingestion=DataIngestion(dataingestconfig)
        logging.info("Ingestion initiated")
        ingestion_artifact=data_ingestion.initiate_dataIngestion()
        print(ingestion_artifact) 
        data_validation_config=DataValidationConfig(trainconfig)
        data_validation=DataValidation(ingestion_artifact,data_validation_config)
        logging.info("Data Validation initiated")
        data_validation_artifact=data_validation.initiate_validation()
        logging.info("Data Validation Done")

        
    except Exception as e:
        raise NetworkSecurityException(e,sys)