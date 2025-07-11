import yaml
import os,sys
import pandas as pd
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
import pickle

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