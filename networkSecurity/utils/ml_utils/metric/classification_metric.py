from networkSecurity.entity.artifact_config import DataValidationArtifact,DataTransformationArtifact,ClassificationMetric
from networkSecurity.entity.entity_config import DataTransformationConfig
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from sklearn.metrics import f1_score,recall_score,precision_score,classification_report
import os,sys

def get_classification_score(y_true,y_pred):
    try:
        f1 = f1_score(y_true,y_pred)
        recall=recall_score(y_true,y_pred)
        precision=precision_score(y_true,y_pred)
        classification_metric =  ClassificationMetric(f1_score=f1,
                    precision_score=precision, 
                    recall_score=recall)
        return classification_metric

    except Exception as e:
        raise NetworkSecurityException(e,sys)
