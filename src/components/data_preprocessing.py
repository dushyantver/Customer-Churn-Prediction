import os
import sys
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from src.entity.config import DataPreprocessingConfig
from src.entity.artifact import DataPreprocessingArtifacts
from src.utils import save_object
from src.exception import Customer_Exception
from src.logger import logging

class DataTransformation:
    def __init__(self, data_transformation_config=DataPreprocessingConfig()):
        self.data_transformation_config = data_transformation_config
        self.data_transformation_artifact = DataPreprocessingArtifacts


    def get_transformer_object(self):
        logging.info("Data Transformation Initiated")
        try:
            num_col = [
                    'CreditScore',
                    'Age',
                    'Tenure',
                    'Balance',
                    'NumOfProducts',
                    'HasCrCard',
                    'IsActiveMember',
                    'EstimatedSalary',
                    ]
            
            cat_col = ["Geography","Gender"]
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))  # Set with_mean=False for sparse data
                ]
            )
            logging.info("Categorical columns encoding completed")

            preprocessore = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, num_col),
                    ("cat_pipeline", cat_pipeline, cat_col)
                ]
            )
            return preprocessore
        except Exception as e:
            raise Customer_Exception(e, sys)
        
    def initiate_data_transformation(self):
        try:
            data_path = self.data_transformation_config.data_path
            final_data = pd.read_csv(data_path)

            final_data = final_data.drop(["RowNumber","CustomerId","Surname"], axis=1)

            logging.info("Data set loaded for preprocessing")

            train_set, test_set = train_test_split(final_data, test_size=0.2, random_state=23)

            logging.info("train and test data split completed")

            preprocessing_obj = self.get_transformer_object()

            logging.info("Obtaining preprocessing object")

            target_col_name = "Exited"
           # numerical_col = ["writing_score", "reading_score"]

            input_feature_train_df = train_set.drop(columns=[target_col_name], axis=1)
            target_feature_train_df = train_set[target_col_name]

            input_feature_test_df = test_set.drop(columns=[target_col_name], axis=1)
            target_feature_test_df = test_set[target_col_name]

            logging.info("Applying preprocessing")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)  # Use transform instead of fit_transform

            #train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            #test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            print(input_feature_train_arr[1])

            logging.info("Saved preprocessing object")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file,
                obj=preprocessing_obj
            )

            data_transformation_artifact:DataPreprocessingArtifacts = DataPreprocessingArtifacts(
                train_file_path = input_feature_train_arr,
                test_file_path = input_feature_test_arr
            )

            return DataPreprocessingArtifacts

        except Exception as e:
            raise Customer_Exception(e, sys)


