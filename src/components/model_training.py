import os
import sys

from src.logger import logging
from src.exception import Customer_Exception
from src.constants.training_pipeline import *
from src.entity.artifact import DataPreprocessingArtifacts
from src.entity.artifact import ModelTrainingArtifacts
from src.entity.config import ModelTrainingConfig

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping,TensorBoard
import datetime

class Model_Trainer:
    def __init__(self, data_preprocessing_artifact:DataPreprocessingArtifacts ):
        self.model_training_config = ModelTrainingConfig
        self.model_training_artifact = ModelTrainingArtifacts
        self.data_preprocessing_artifact:DataPreprocessingArtifacts = data_preprocessing_artifact()

    def model_initiation(self):
        try:

            logging.info("Starting Model init")
            ## Build Our ANN Model
            model=Sequential([
                Dense(64,activation='relu',input_shape=(12,)), ## HL1 Connected wwith input layer
                Dense(32,activation='relu'), ## HL2
                Dense(1,activation='sigmoid')  ## output layer
                ]
                )
            model.summary()
            opt=tf.keras.optimizers.Adam(learning_rate=0.01)
            loss=tf.keras.losses.BinaryCrossentropy()

            logging.info("Model Compilation Started")
            model.compile(optimizer=opt,loss="binary_crossentropy",metrics=['accuracy'])
            return model
        except Exception as e:
            raise Customer_Exception(e,sys) 

    def initiate_model_training(self):

        try:
            logging.info("loading the train and test array set")
            train_array = self.data_preprocessing_artifact.train_data
            test_array = self.data_preprocessing_artifact.test_data

            logging.info("Spliting train and test set array")
            X_train, X_test, Y_train, Y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            logging.info("Model Training Started")
            model=self.model_initiation()
            ## Set up Early Stopping
            early_stopping_callback=EarlyStopping(monitor='val_loss',patience=10,restore_best_weights=True)
            ### Train the model
            history=model.fit(
                X_train,Y_train,validation_data=(X_test,Y_test),epochs=100,
                callbacks=[tensorflow_callback,early_stopping_callback]
                )
            
            logging.info("Model Training Completed")

            model_file_path = self.model_training_config.artifact_dir

            model.save(model_file_path)

            logging.info("model is saved")

            model_training_artifact: ModelTrainingArtifacts = ModelTrainingArtifacts(
                trained_model_file_path =  model_file_path
            ) 
            return ModelTrainingArtifacts
        except Exception as e:
            raise Customer_Exception(e,sys)
        




            
