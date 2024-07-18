import os
import sys

from src.components.data_ingestion import DataIngestion
from src.entity.config import DataIngestionConfig
from src.entity.artifact import DataIngestionArtifacts
from src.exception import Customer_Exception
from src.logger import logging

class Train_pipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
    
    def start_data_ingestion(self)->DataIngestionArtifacts:
        logging.info("Entered data ingestion pass of training pipeline")
        try:
            logging.info("getting data from s3")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("completed data ingestion")

            return data_ingestion_artifact
        except Exception as e:
            raise Customer_Exception(e, sys)