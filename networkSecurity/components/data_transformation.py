from networkSecurity.entity.artifact_config import DataValidationArtifact,DataTransformationArtifact
from networkSecurity.entity.entity_config import DataTransformationConfig
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
import os,sys
import pandas as pd
import numpy as np
from networkSecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_PARAMS
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networkSecurity.utils.main_util.util import save_np_array,save_obj

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        self.data_validation_artifact=data_validation_artifact
        self.data_transformation_config=data_transformation_config

    def data_transform(cls)->Pipeline:
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_PARAMS)
            processor:Pipeline=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Data Transformation started")
            data_transformed_train_file:str=self.data_transformation_config.data_transformed_train_file
            data_transformed_test_file:str=self.data_transformation_config.data_transformed_test_file

            train_df:pd.DataFrame=pd.read_csv(self.data_validation_artifact.valid_train_path)
            test_df:pd.DataFrame=pd.read_csv(self.data_validation_artifact.valid_test_path)

            train_input_feat=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target=train_df[TARGET_COLUMN].replace(-1,0)
            test_input_feat=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target=test_df[TARGET_COLUMN].replace(-1,0)

            preprocessor=self.data_transform()
            preprocessor_obj=preprocessor.fit(train_input_feat)
            train_feature_transform=preprocessor_obj.transform(train_input_feat)
            test_feature_transform = preprocessor_obj.transform(test_input_feat) 

            train_arr=np.c_[train_feature_transform,np.array(train_target)]
            test_arr=np.c_[test_feature_transform,np.array(test_target)]

            save_np_array(file_path=data_transformed_train_file,array=train_arr)
            save_np_array(file_path=data_transformed_test_file,array=test_arr)
            save_obj(file_path=self.data_transformation_config.data_transformed_obj_file,obj=preprocessor_obj)

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_path=self.data_transformation_config.data_transformed_obj_file,
                transformed_test_path=self.data_transformation_config.data_transformed_test_file,
                transformed_train_path=self.data_transformation_config.data_transformed_train_file
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        