import sys

from src.exception import Customer_Exception
from src.logger import logging
from src.pipeline.training_pipeline import Train_pipeline

def start_training():
    try:
        train_pipeline = Train_pipeline()
        train_pipeline.data_transformation()

    except Exception as e:
        raise Customer_Exception(e, sys)


if __name__ == "__main__":
    start_training()