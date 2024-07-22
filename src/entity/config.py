import os
from dataclasses import dataclass
from src.constants.training_pipeline import *

## Data Ingestion Configuration
@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.s3_data_folder:str = S3_DATA_FOLDER
        self.bucket_name:str = BUCKET_NAME
        self.artifact_dir:str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
        self.data_path:str = os.path.join(self.s3_data_folder, "Churn_Modelling.csv")

        self.data_import_path:str = os.path.join(self.data_path, "imported_data")


## Data Preprocessing Configuration
@dataclass
class DataPreprocessingConfig:
    def __init__(self):
        self.data_path = "D:\\Data_analytics_new\\MLOPS\\Customer-Churn-Prediction\\artifacts\\Churn_Modelling.csv"
        self.preprocessor_obj_file: str = os.path.join("artifacts", "preprocessor.pkl")

## Model Training Configuration
@dataclass
class ModelTrainingConfig:
    def __init__(self):
        self.artifact_dir:str = os.path.join("artifacts", "model.h5")