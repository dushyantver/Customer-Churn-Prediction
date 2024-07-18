import os
import sys
from src.constants.training_pipeline import *
from src.entity.config import DataIngestionConfig
from src.entity.artifact import DataIngestionArtifacts
from src.exception import Customer_Exception
from src.logger import logging
from src.cloud_storage.s3_operations import S3Operation

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.s3 = S3Operation()

    def get_data_from_s3(self):
        try:
            logging.info(f"Getting data from s3 bucket in data ingestion")
            self.s3.download_file(
                from_filename = "data/Churn_Modelling.csv",
                to_filename = "D:/Data_analytics_new/MLOPS/Customer-Churn-Prediction/artifacts/Churn_Modelling.csv" ,
                bucket_name=self.data_ingestion_config.bucket_name
            )
            logging.info(f"Data downloaded from s3 bucket in data ingestion")
        except Exception as e:
            raise Customer_Exception(e,sys)


    def initiate_data_ingestion(self)->DataIngestionArtifacts:
        logging.info("Entered the initiate data ingestion method")
        try:
            self.get_data_from_s3()
            data_ingestion_artifact:DataIngestionArtifacts = DataIngestionArtifacts(
                data_file_path=self.data_ingestion_config.data_import_path)
            logging.info(f"Data ingestion completed")
            return data_ingestion_artifact
        except Exception as e:
            raise Customer_Exception(e,sys)
