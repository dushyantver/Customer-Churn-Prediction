import os
import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataTransformation
from src.entity.config import DataIngestionConfig
from src.entity.config import DataPreprocessingConfig
from src.entity.artifact import DataIngestionArtifacts
from src.entity.artifact import DataPreprocessingArtifacts
from src.exception import Customer_Exception
from src.logger import logging

class Train_pipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_preprocessing_config = DataPreprocessingConfig()
    
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
        
    def data_transformation(self)->DataPreprocessingArtifacts:
        logging.info("Entered data transformation pass of training pipeline")
        try:
            data_transformation = DataTransformation(data_transformation_config = self.data_preprocessing_config)
            data_preprocessing_artifact = data_transformation.initiate_data_transformation()
            logging.info("completed data transformation")
            return data_preprocessing_artifact
        except Exception as e:
            raise Customer_Exception(e, sys)
