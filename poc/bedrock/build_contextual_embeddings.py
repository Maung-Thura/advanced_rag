import os
import json
import glob

import pdfplumber
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_embeddings_dir():
	if not os.path.isdir('./embeddings'):
		os.mkdir('./embeddings')

	return


def extract_context(file_path):
    file = pdfplumber.open(file_path)
    context = {}

    for i, page in enumerate(file.pages):
        context[i] = {
            'page' : page.extract_text(),
            'images': None,
            'tables': None,
        }

    return context


def get_splitter_client():
    return RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ' '],
        chunk_size=1000,
        chunk_overlap=100
    )


def get_embeddings_client():
    return HuggingFaceEmbeddings()


def generate_context_embeddings(context):
    splitter_client = get_splitter_client()
    embeddings_client = get_embeddings_client()

    pages = [c['page'] for _, c in context.items()]
    documents = splitter_client.create_documents(pages)
    documents = [doc.page_content for doc in documents]
    embeddings = embeddings_client.embed_documents(documents)
    
    contextual_embeddings = []
    
    for i, document in enumerate(documents):
        contextual_embeddings.append({
            'context': document,
            'embedding': embeddings[i]
        })
    
    return contextual_embeddings


def build_embeddings():
    for file_path in glob.glob('./corpora/*'):
        context = extract_context(file_path)
        context_embeddings = generate_context_embeddings(context)
        
        file_name = file_path.split('/')[-1].split('.')[-2]
        
        open(f'./embeddings/{file_name}.json', 'w').write(json.dumps(context_embeddings, indent=4))
        print(f'Saved embeddings for ./embeddings/{file_name}.json...')


if __name__ == '__main__':
    create_embeddings_dir()
    build_embeddings()
