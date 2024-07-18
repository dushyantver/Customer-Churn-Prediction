import os
import sys
import boto3
#from botocore.exceptions import ClientError
from src.logger import logging
from src.exception import Customer_Exception


class S3Operation:
    def __init__(self):
        self.s3_client = boto3.client("s3")
        self.s3_resource = boto3.resource("s3")

    def upload_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = True,
    ) -> None:
        """
        Method Name :   upload_file
        Description :   This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename
        Output      :   Folder is created in s3 bucket
        """
        logging.info("Entered the upload_file method of S3Operation class")
        try:
            logging.info(
                f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            self.s3_resource.meta.client.upload_file(
                from_filename, bucket_name, to_filename
            )
            logging.info(
                f"Uploaded {from_filename} file to {to_filename} file in {bucket_name} bucket"
            )

            if remove:
                os.remove(from_filename)
                logging.info(f"Removed {from_filename} after upload")
            else:
                logging.info(f"Did not remove {from_filename} after upload")
            
            logging.info("Exited the upload_file method of S3Operation class")

        except Exception as e:
            raise Customer_Exception(e,sys)

    def download_file(
        self,
        from_filename: str,
        to_filename: str,
        bucket_name: str,
        remove: bool = False,
    ) -> None:
        """
        Method Name :   download_file
        Description :   This method downloads the from_filename file from bucket_name bucket with to_filename as local filename
        Output      :   File is downloaded from S3 bucket
        """
        logging.info("Entered the download_file method of S3Operation class")
        try:
            logging.info(
                f"Downloading {from_filename} file from {bucket_name} bucket to {to_filename}"
            )

            self.s3_resource.meta.client.download_file(
                bucket_name, from_filename, to_filename
            )
            logging.info(
                f"Downloaded {from_filename} file from {bucket_name} bucket to {to_filename}"
            )

            if remove:
                self.delete_file(from_filename, bucket_name)
                logging.info(f"Removed {from_filename} after download")
            else:
                logging.info(f"Did not remove {from_filename} after download")
            
            logging.info("Exited the download_file method of S3Operation class")

        except Exception as e:
            raise Customer_Exception(e,sys)

    def delete_file(self, filename: str, bucket_name: str) -> None:
        """
        Method Name :   delete_file
        Description :   This method deletes the file with filename from bucket_name bucket 
        Output      :   File is deleted from S3 bucket
        """
        logging.info(f"Deleting {filename} file from {bucket_name} bucket")
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=filename)
            logging.info(f"Deleted {filename} file from {bucket_name} bucket")
        except Exception as e:
            raise Customer_Exception(e,sys)
        
