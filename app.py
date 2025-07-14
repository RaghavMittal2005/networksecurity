import os,sys
import certifi

ca=certifi.where()
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')
import pymongo
from pymongo import MongoClient

from networkSecurity.exception.exception import NetworkSecurityException
from networkSecurity.logging.logger import logging
from networkSecurity.entity.entity_config import TrainingPipelineConfig
from networkSecurity.pipeline.training_pipeline import TrainingPipeline
import pandas as pd
from networkSecurity.utils.main_util.util import load_object
from networkSecurity.utils.ml_utils.model.estimator import NetworkModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, status, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates(directory="./templates")

from networkSecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME,DATA_INGESTION_DATBASE_NAME
client=MongoClient(MONGO_DB_URL,tlsCAFile=ca)
database=client[DATA_INGESTION_DATBASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]
app=FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url='/docs')

@app.get("/train")
async def train():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training Done")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        preprocessor=load_object(file_path="final_models/preprocessor.pkl")
        model=load_object(file_path="final_models/model.pkl")
        network_model=NetworkModel(processor=preprocessor,model=model)
        print(df.iloc[0])
        prediction=network_model.predict(df)
        print(prediction)
        df['prediction']=prediction
        df.to_csv(path_or_buf="prediction_data/output.csv")
        table_html=df.to_html(classes='table table striped')
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
        




if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)
