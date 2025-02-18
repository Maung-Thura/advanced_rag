import boto3
import json
import numpy as np

from pymongo import MongoClient
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings



def instantiate_llm(region_name):
	try:
		bedrock_client = boto3.client(service_name='bedrock-runtime', region_name=region_name)

	except NoCredentialsError:
		print('Credentials not available')

	return bedrock_client


def query_llm(bedrock_client, model_id='amazon.titan-text-express-v1', query_text='', context=''):
	payload = {
		'prompt':  f'<|begin_of_text|>Here is a query - {query_text} and additional context to answer the query - {context}. Now, answer the query.<|eot_id|>',
		'max_gen_len': 250,
		'temperature': 0.5,
		'top_p': 0.7
	}
	response = bedrock_client.invoke_model(
		body = json.dumps(payload),
		modelId = model_id,
		accept = 'application/json',
		contentType = 'application/json',
	)

	response_body = json.loads(response.get('body').read())
	response_text = response_body['generation']
	
	return response_text


def get_embeddings_client():
	return HuggingFaceEmbeddings()


def generate_query_embeddings(query):
	embeddings_client = get_embeddings_client()
	return embeddings_client.embed_query(query)


def extract_context_from_db(db_name, collection_name, query_embedding):
	uri = 'mongodb://msaiadmin:msaipassword@jph6705-msai-rohan.cluster-coqnybpzsdbk.us-east-2.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false'
	client = MongoClient(uri)

	db = client[db_name]
	collection = db[collection_name]

	response = collection.aggregate([
		{
			'$search': {
				'vectorSearch': {
					'vector': query_embedding, 
					'path': 'embedding', 
					'similarity': 'cosine',
					'k': 3,
					'efSearch': 40
				}
			}
		},
		{
			'$project': {
				'_id': 0,
				'context': 1,
			}
		}
	])

	context = [c['context'] for c in list(response)]
	
	return context[0]

if __name__ == '__main__':
	bedrock_client = instantiate_llm('us-east-1')
	db_name = 'advanced-rag-embeddings'
	collection_name = 'embeddings'

	query_text = input('Enter your query here: ')
	query_embedding = generate_query_embeddings(query=query_text)
	context = extract_context_from_db(db_name, collection_name, query_embedding=query_embedding)
	response = query_llm(bedrock_client, model_id='meta.llama3-70b-instruct-v1:0', query_text=query_text, context=context)
	print(response)
