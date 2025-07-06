import os
import json
import sys
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

import certifi
ca=certifi.where()
from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging

class NetworkSecurity():


    def __init__(self):
        try:
            pass
        except Exception as e:

            raise NetworkSecurityException(e,sys)
    def csv_to_json(self,filepath):
        try:
            data = pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            records= list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_to_db(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.client = MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            result = self.collection.insert_many(self.records)
            return result
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__ == "__main__":
    try:
        ns=NetworkSecurity()
        filepath="network_data\phisingData.csv"
        records=ns.csv_to_json(filepath)
        DataBase="Raghav"
        collection="phisingData"
        result=ns.insert_to_db(records,DataBase,collection)
        print(records)
    except Exception as e:
        logging.error(e,exc_info=True)
        raise NetworkSecurityException(e,sys)
