import glob
import json

import boto3
from botocore.exceptions import NoCredentialsError
from pymongo import MongoClient


def create_doc_db(cluster_name, region_name, instance_class):
	try:
		client = boto3.client('docdb', region_name=region_name)
	
	except NoCredentialsError:
		print('Credentials not available')

	client.create_db_cluster(
		DBClusterIdentifier=cluster_name,
		Engine='docdb',
		MasterUsername='msaiadmin',
		MasterUserPassword='msaipassword',
	)

	client.create_db_instance(
		DBInstanceIdentifier=cluster_name + '-instance',
		DBInstanceClass=instance_class,
		Engine='docdb',
		DBClusterIdentifier=cluster_name,
		AutoMinorVersionUpgrade=True
	)


def get_s3_contents(bucket_name, region=None, prefix='embeddings'):
	try:
		s3_client = boto3.client('s3', region_name=region)
		
	except NoCredentialsError:
		print("Credentials not available")
		
	file_paths = [c['Key'] for c in s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)['Contents']]
	return file_paths


def save_embeddings_to_db(bucket_name, region, db_name, collection_name):
	uri = 'mongodb://msaiadmin:msaipassword@jph6705-msai-rohan.cluster-coqnybpzsdbk.us-east-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
	client = MongoClient(uri)

	try:
		s3_client = boto3.client('s3', region_name=region)
		
	except NoCredentialsError:
		print("Credentials not available")

	db = client[db_name]
	collection = db[collection_name]

	file_paths = get_s3_contents(bucket_name, region)
	
	for file_path in file_paths:
		response = s3_client.get_object(Bucket=bucket_name, Key=file_path)
		embeddings = json.loads(response['Body'].read().decode('utf-8'))
		collection.insert_many(embeddings)
		print(f'Saved embeddings for {file_path}...')


def set_db_vector_search_index(db_name, collection_name):
	uri = 'mongodb://msaiadmin:msaipassword@jph6705-msai-rohan.cluster-coqnybpzsdbk.us-east-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
	client = MongoClient(uri)

	db = client[db_name]
	collection = db[collection_name]

	collection.create_index(
		[('embedding', 'vector')],
		vectorOptions= {
			'type': 'hnsw', 
			'similarity': 'cosine',
			'dimensions': 768,
			'm': 16,
			'efConstruction': 64
		},
		name='embeddings-index'
	)


if __name__ == '__main__':
	cluster_name = 'jph6705-msai-rohan'
	db_name = 'advanced-rag-embeddings'
	collection_name = 'embeddings'
	region = 'us-east-2'
	bucket_name = 'jph6705-msai490-practicum'
	region = 'us-east-2'

	# create_doc_db(cluster_name, region, 'db.r5.large')
	# save_embeddings_to_db(bucket_name, region, db_name, collection_name)
	set_db_vector_search_index(db_name, collection_name)