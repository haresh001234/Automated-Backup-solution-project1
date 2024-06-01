import subprocess
import os
import datetime
import logging
import boto3
from botocore.exceptions import NoCredentialsError

# Configuration
LOCAL_DIRECTORY = "/path/to/local/directory"
REMOTE_SERVER = "user@remote_server:/path/to/remote/directory"
LOG_FILE = "/path/to/logfile.log"
USE_CLOUD_STORAGE = False  # Set to True if using cloud storage
S3_BUCKET = "your-s3-bucket-name"
AWS_ACCESS_KEY = "your-access-key"
AWS_SECRET_KEY = "your-secret-key"

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def backup_to_remote():
    try:
        logging.info("Starting backup to remote server...")
        result = subprocess.run(["rsync", "-avz", LOCAL_DIRECTORY, REMOTE_SERVER], capture_output=True, text=True)

        if result.returncode == 0:
            logging.info("Backup to remote server completed successfully.")
            return True
        else:
            logging.error(f"Backup to remote server failed with error: {result.stderr}")
            return False
    except Exception as e:
        logging.error(f"An error occurred during backup to remote server: {e}")
        return False


def backup_to_s3():
    try:
        logging.info("Starting backup to AWS S3...")
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

        for root, dirs, files in os.walk(LOCAL_DIRECTORY):
            for file in files:
                file_path = os.path.join(root, file)
                s3_key = os.path.relpath(file_path, LOCAL_DIRECTORY)
                s3.upload_file(file_path, S3_BUCKET, s3_key)

        logging.info("Backup to AWS S3 completed successfully.")
        return True
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return False
    except NoCredentialsError:
        logging.error("AWS credentials not available.")
        return False
    except Exception as e:
        logging.error(f"An error occurred during backup to AWS S3: {e}")
        return False


def main():
    logging.info("Backup script started.")
    if USE_CLOUD_STORAGE:
        success = backup_to_s3()
    else:
        success = backup_to_remote()

    if success:
        logging.info("Backup operation completed successfully.")
    else:
        logging.error("Backup operation failed.")

    logging.info("Backup script finished.")


if __name__ == "__main__":
    main()


