import os,sys
import mlflow.sklearn
import pandas as pd
from networkSecurity.entity.artifact_config import DataTransformationArtifact,ModelTrainerArtifact
from networkSecurity.entity.entity_config import ModelTrainerConfig
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

from networkSecurity.utils.main_util.util import load_numpy_array,load_object,save_np_array,evaluate_model,save_obj
from networkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networkSecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
import mlflow
import dagshub
dagshub.init(repo_owner='RaghavMittal2005', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        self.model_trainer_config=model_trainer_config
        self.data_transformation_artifact=data_transformation_artifact

    def track_mlflow(self,model,classifiactionmetrics):
       try:
          with mlflow.start_run():
             f1=classifiactionmetrics.f1_score
             recall=classifiactionmetrics.recall_score
             precision=classifiactionmetrics.precision_score
             mlflow.log_metric("f1_score",f1)
             mlflow.log_metric("recall_score",recall)
             mlflow.log_metric("precision_score",precision)
             mlflow.sklearn.log_model(model,"best model")
       

       except Exception as e:
          raise NetworkSecurityException(e,sys)

    def model_train(self,x_train,y_train,x_test,y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best','random'],
                'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                'criterion':['gini', 'entropy', 'log_loss'],
                
                #'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            }
            model_report:dict=evaluate_model(x_train,y_train,x_test,y_test,models=models,params=params)
            best_model_name = max(model_report, key=model_report.get)  # ✅ gets key with max value
            best_model_score = model_report[best_model_name]

            

            
            best_model = models[best_model_name]
            best_model.fit(x_train,y_train)
            y_train_pred=best_model.predict(x_train)
            y_test_pred=best_model.predict(x_test)

            train_classification_report=get_classification_score(y_train,y_train_pred)
            test_classification_report=get_classification_score(y_test,y_test_pred)

            #track with mlflow
            self.track_mlflow(best_model,train_classification_report)
            self.track_mlflow(best_model,test_classification_report)

            preprocessor=load_object(self.data_transformation_artifact.transformed_object_path)

            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file)
            os.makedirs(model_dir_path,exist_ok=True)
            
            Network_model=NetworkModel(processor=preprocessor,model=best_model)
            save_obj(self.model_trainer_config.trained_model_file,obj=Network_model)

            save_obj("final_models/model.pkl",best_model)
            save_obj("final_models/preprocessor.pkl",preprocessor)

            model_trainer_artifact=ModelTrainerArtifact(
                
                test_data_artifact=test_classification_report,
                
                trained_data_artifact=train_classification_report,
                trained_model_file=self.model_trainer_config.trained_model_file
            )
            
            return model_trainer_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_training(self) -> ModelTrainerArtifact:
        try:
          transformed_train_file = self.data_transformation_artifact.transformed_train_path
          transformed_test_file = self.data_transformation_artifact.transformed_test_path

          train_df = load_numpy_array(transformed_train_file)
          test_df = load_numpy_array(transformed_test_file)

          x_train, y_train, x_test, y_test = (
            train_df[:, :-1],
            train_df[:, -1],
            test_df[:, :-1],
            test_df[:, -1],
          )
          model_train_artifact = self.model_train(x_train, y_train, x_test, y_test)
          return model_train_artifact

        except Exception as e:
         raise NetworkSecurityException(e, sys)

