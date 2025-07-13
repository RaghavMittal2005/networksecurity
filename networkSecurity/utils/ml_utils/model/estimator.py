from networkSecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
import os,sys

class NetworkModel:
    def __init__(self,processor,model):
        try:
            self.processor = processor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def predict(self,X):
        try:
            transformed_data = self.processor.transform(X)
            result = self.model.predict(transformed_data)
            return result
        except Exception as e:
            raise NetworkSecurityException(e,sys)