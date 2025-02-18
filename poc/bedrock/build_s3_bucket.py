import os
import glob

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def create_bucket(bucket_name, region):
	try:
		s3_client = boto3.client('s3', region_name=region)

	except NoCredentialsError:
		print("Credentials not available")

	s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region})
	print(f"Bucket '{bucket_name}' created successfully.")


def upload_to_bucket(bucket_name, region=None):
	try:
		s3_client = boto3.client('s3', region_name=region)

	except NoCredentialsError:
		print("Credentials not available")

	for file_path in glob.glob('./corpora/*'):
		file_name = file_path.split('/')[-1]
		s3_client.upload_file(f'{file_path}', bucket_name, os.path.join('corpora', file_name))
		print(f'Uploaded {file_path}...')


	for file_path in glob.glob('./embeddings/*'):
		file_name = file_path.split('/')[-1]
		s3_client.upload_file(f'{file_path}', bucket_name, os.path.join('embeddings', file_name))
		print(f'Uploaded {file_path}...')
	

if __name__ == "__main__":
	bucket_name = 'jph6705-msai490-practicum'
	region = 'us-east-2'
	create_bucket(bucket_name, region)
	upload_to_bucket(bucket_name, region)
