from networkSecurity.entity.artifact_config import IngestionPara,DataValidationArtifact
from networkSecurity.entity.entity_config import DataValidationConfig
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from scipy.stats import ks_2samp
import os,sys
import pandas as pd
from networkSecurity.utils.main_util.util import read_yaml,write_yaml
from networkSecurity.constant.training_pipeline import SCHEMA_PATH

class DataValidation:
    def __init__(self,data_ingestion_artifact:IngestionPara,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_config=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml(SCHEMA_PATH)
            

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def no_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            no_of_col=len(self._schema_config['columns'].keys())
            print(no_of_col)
            data_col=len(dataframe.columns)
            if data_col==no_of_col:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def valid_col(self,dataframe:pd.DataFrame)->bool:
        try:
            for col,dtype in self._schema_config['columns'].items():
                actual=str(dataframe[col].dtype)
                if actual!=dtype:
                    return False
                
            return True

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def check_data_drift(self,base_df:pd.DataFrame,curr_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            report={}
            stat=True
            for col in base_df.columns:
                d1=base_df[col]
                d2=curr_df[col]
                status=ks_2samp(d1,d2)
                if threshold<status.pvalue:
                    ret=False
                    stat=False
                else:
                    ret=True
                report.update({
                    col:{
                        "p_value":float(status.pvalue),
                        "drift_status":ret
                    }
                })
                drift_report_file_path=self.data_validation_config.data_drift_report_path
                
                write_yaml(file=drift_report_file_path,report=report)

                
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_validation(self)->DataValidationArtifact:
        try:
            train_path=self.data_ingestion_config.training_path
            test_path=self.data_ingestion_config.testing_path
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            status=self.no_of_columns(train_df)
            if not status:
                logging.info("Error in no. of column of train data")
            status=self.no_of_columns(test_df)
            if not status:
                logging.info("Error in no. of column of test data")
            status=self.valid_col(train_df)
            if not status:
                logging.info("Error in dtype of train data")
            status=self.valid_col(train_df)
            if not status:
                logging.info("Error in dtype of train data")
            status=self.valid_col(test_df)
            if not status:
                logging.info("Error in dtype of test data")

            status=self.check_data_drift(base_df=train_df,curr_df=test_df)
            os.makedirs(self.data_validation_config.data_valid_dir,exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_training_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_testing_path,index=False,header=True)
            data_validation_artifact= DataValidationArtifact(
                validation_status=status,
                valid_test_path=self.data_validation_config.valid_testing_path,
                valid_train_path=self.data_validation_config.valid_training_path,
                invalid_test_path=None,
                invalid_train_path=None,
                drift_report_path=self.data_validation_config.data_drift_report_path
            )
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

