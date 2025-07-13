import yaml
import os,sys
import pandas as pd
import numpy as np
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml(file_path:str)->dict:
    try:
        with open(file_path,"rb") as f:
            return yaml.safe_load(f)

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml(file:str,report:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file):
                os.remove(file)
        os.makedirs(os.path.dirname(file),exist_ok=True)
        with open(file,"w") as f:
            yaml.dump(report,f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_np_array(file_path:str,array:np.array):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as f:
            np.save(arr=array,file=f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_obj(file_path:str,obj:object):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as f:
            pickle.dump(obj=obj,file=f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_object(file_path:str):
    try:
        if os.path.exists(file_path):
            with open(file_path,"rb") as f:
                return pickle.load(f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def load_numpy_array(file_path:str):
    try:
        if os.path.exists(file_path):
            with open(file_path,"rb") as f:
                return np.load(file=f)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def evaluate_model(x_train,y_train,x_test,y_test,models:dict,params:dict):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gs=GridSearchCV(model,param_grid=param)
            gs.fit(x_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)

            y_test_pred=model.predict(x_test)
            test_r2_score=r2_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_r2_score
        return report

        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
