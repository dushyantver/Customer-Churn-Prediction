import os
import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_preprocessing import DataTransformation
from src.components.model_training import Model_Trainer
from src.entity.config import DataIngestionConfig
from src.entity.config import DataPreprocessingConfig
from src.entity.config import ModelTrainingConfig
from src.entity.artifact import DataIngestionArtifacts
from src.entity.artifact import DataPreprocessingArtifacts
from src.entity.artifact import ModelTrainingArtifacts

from src.exception import Customer_Exception
from src.logger import logging

class Train_pipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_preprocessing_config = DataPreprocessingConfig()
        self.model_training_config = ModelTrainingConfig()
        #self.data_preprocessing_artifact = DataPreprocessingArtifacts
    
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
        
    def start_data_transformation(self)->DataPreprocessingArtifacts:
        logging.info("Entered data transformation pass of training pipeline")
        try:
            data_transformation = DataTransformation(data_transformation_config = self.data_preprocessing_config)
            data_preprocessing_artifact = data_transformation.initiate_data_transformation()
            logging.info("completed data transformation")
            return data_preprocessing_artifact
        except Exception as e:
            raise Customer_Exception(e, sys)
        
    def start_model_training(self, data_preprocessing_artifact:DataPreprocessingArtifacts)->ModelTrainingArtifacts:
        logging.info("Entered model training pass of training pipeline")
        try:
            model_trainer = Model_Trainer(data_preprocessing_artifact = data_preprocessing_artifact)
            model_training_artifact = model_trainer.initiate_model_training()
            logging.info("completed model training")
            return model_training_artifact
        except Exception as e:
            raise Customer_Exception(e, sys)
        
    def run_pipeline(self)->None:
        logging.info("Entered the run pipline")
        try:
            data_transformation_artifact1:DataPreprocessingArtifacts = self.start_data_transformation()
            model_training_artifact:ModelTrainingArtifacts = self.start_model_training(data_preprocessing_artifact=data_transformation_artifact1)
            logging.info("Exited the run pipeline")
        except Exception as e:
            raise Customer_Exception(e, sys)
