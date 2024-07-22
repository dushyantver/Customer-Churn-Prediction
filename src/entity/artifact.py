from dataclasses import dataclass
import numpy as np

@dataclass
class DataIngestionArtifacts:
    data_file_path:str

@dataclass
class DataPreprocessingArtifacts:
    train_data: np.ndarray
    test_data: np.ndarray

@dataclass
class ModelTrainingArtifacts:
    trained_model_file_path:str
    
    