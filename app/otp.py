import os

# App configuration.

APP_ID = os.getenv("APP_ID")
APP_VERSION = os.getenv("APP_VERSION")

# AWS S3 configuration.

AWS_S3_APP_BUCKET = os.getenv("aws_s3_app_bucket")
AWS_S3_APP_FOLDER = os.getenv("aws_s3_app_folder")

# RDS configuration.

RDS_DB_NAME = os.getenv("RDS_DB_NAME")
RDS_SCHEMA_NAME = os.getenv("RDS_SCHEMA_NAME")
RDS_INSTANCE_NAME = os.getenv("RDS_INSTANCE_NAME")
RDS_DB_DATA_PATH = (
        f"{AWS_S3_APP_FOLDER}/dbMetadata/"
        + (f"{RDS_INSTANCE_NAME}/" if RDS_INSTANCE_NAME else "")
        + f"{RDS_DB_NAME}/{RDS_SCHEMA_NAME}.dbdata"
)
