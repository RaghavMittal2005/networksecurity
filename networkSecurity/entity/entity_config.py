import os
from datetime import datetime
import pandas as pd
from networkSecurity.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACTS_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp=timestamp
    
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_NAME,training_pipeline.FILE_NAME)
        self.training_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TRAIN_FILE)
        self.testing_file_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR,training_pipeline.TEST_FILE)
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str=training_pipeline.DATA_INGESTION_DATBASE_NAME
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO



class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.data_valid_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.data_invalid_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.data_drift_report_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_DIR)
        self.valid_training_path:str=os.path.join(self.data_valid_dir,training_pipeline.TRAIN_FILE)
        self.valid_testing_path:str=os.path.join(self.data_valid_dir,training_pipeline.TEST_FILE)
        self.invalid_training_path:str=os.path.join(self.data_invalid_dir,training_pipeline.TRAIN_FILE)
        self.invalid_training_path:str=os.path.join(self.data_invalid_dir,training_pipeline.TEST_FILE)
        self.data_drift_report_path:str=os.path.join(self.data_drift_report_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformed_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR
        )
        self.data_transformed_data_dir:str=os.path.join(self.data_transformed_dir,training_pipeline.DATA_TRANSFORMATION_DATA_DIR)
        self.data_transformed_object_dir:str=os.path.join(self.data_transformed_dir,training_pipeline.DATA_TRANSFORMATION_OBJECT_DIR)
        self.data_transformed_train_file:str=os.path.join(self.data_transformed_data_dir,training_pipeline.TRAIN_FILE.replace('csv','npy'))
        self.data_transformed_test_file:str=os.path.join(self.data_transformed_data_dir,training_pipeline.TEST_FILE.replace('csv','npy'))
        self.data_transformed_obj_file:str=os.path.join(self.data_transformed_object_dir,training_pipeline.PREPROCESS_FILE)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir=os.path.join(training_pipeline_config.artifact_dir,training_pipeline.MODEL_TRAINER_DIR)
        self.trained_model_file:str=os.path.join(self.model_trainer_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_FILE)
        self.expected_accuracy:float=training_pipeline.MODEL_EXPECTED_ACCURACY
        self.overfitting_threshold:float=training_pipeline.MODEL_OVERFITTING_THRESH
  