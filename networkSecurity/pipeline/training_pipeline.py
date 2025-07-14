import os,sys
import numpy as np
import pandas as pd
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.entity_config import TrainingPipelineConfig,DataTransformationConfig
from networkSecurity.entity.entity_config import DataIngestionConfig,DataValidationConfig,ModelTrainerConfig
from networkSecurity.entity.artifact_config import IngestionPara,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
from networkSecurity.components.dataIngestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.components.data_transformation import DataTransformation
from networkSecurity.components.model_trainer import ModelTrainer
from datetime import datetime


class TrainingPipeline:
    def __init__(self):
        try:
            self.training_pipeline_config = TrainingPipelineConfig()

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion=DataIngestion(dataIngestionconfig=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_dataIngestion()
            logging.info(f"Data ingestion is completed. Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self, data_ingestion_artifact: IngestionPara):
        try:
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation = DataValidation(data_validation_config=self.data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_validation()
            logging.info(f"Data validation is completed. Artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data transformation is completed. Artifact: {data_transformation_artifact}")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_model_trainer(self, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_training()
            logging.info(f"Model trainer is completed. Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.initiate_data_ingestion()
            data_validation_artifact = self.initiate_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.initiate_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.initiate_model_trainer(data_transformation_artifact)
            logging.info(f"Training pipeline is completed. Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)