from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    data_file_path:str

@dataclass
class DataPreprocessingArtifacts:
    train_file_path:str
    test_file_path:str
    