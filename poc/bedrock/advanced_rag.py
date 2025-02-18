import boto3
import streamlit as st


from langchain_community.embeddings import BedrockEmbeddings
#from langchain.llms.bedrock import Bedrock
from langchain_community.llms import Bedrock

# ## Data Ingestion

# # Vector Embedding And Vector Store

import os
from astrapy import DataAPIClient

os.environ["ASTRA_DB_API_ENDPOINT"] ="https://4c5ec6df-6240-4e0e-a17c-ea5acc0a7531-us-east-2.apps.astra.datastax.com"
os.environ["ASTRA_DB_APPLICATION_TOKEN"] = "AstraCS:ysImOkpETfJsAebhQPmFNoLB:7f6f14e98c3c03758881fc1704c066a7c5dfe9334a9f432b047d601d6fc5385d"
os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjEEIaCXVzLWVhc3QtMiJIMEYCIQDbBlAHyzbcea95QpaogFzPZ3KimTtd/xL5thoinsvQcQIhAOM+IOrtPt2/Xvr4PZUa24YjDSVsLc8NWlsZMUO6zR+gKvQCCKv//////////wEQABoMOTQ5NjcyNzIzMTUwIgwnDGprKDZAU0BCt/4qyAI1dp5cZzvKVfMfmISuiVJfoWIR/3yK8ES2rzWi0ueBdjNrPpObQ/GPcdFlogeRFldSGGsaD5vmacuapu7hXgTb55AAU/GhWIX1NgNnHsoOG2NcvstoVIFpKTXQK0MOtWIcNvw7z1K8FoD1xQZdIwiBIIQuZXYjMmyDGsRj7/kVAevXuFHSMd/Z71IcxAf8YsXYMHF1nc5ObTLTvqnCtBOtw+8xOSEH0XZld4bOFvpYqNO2r4aWf7xCiJ6EIyq5kxM+Xvg1niukQdyzZJkfjQedvyCX8eq9uN80t91I1w0xE5PawzGVI3vkbiJtS1CU/vw/BysMCFNvqVeEipcJ7wOoWHxRAn7tyT7RbUWlSOtuFWYoSC/3sG/FF/4lTK9X16KPD4T9/ky2f+d8mbKVIPBOFS3rOZ9AEpAEOoPcYu1hRJbV/w+kGQhOMPzlk7IGOqYB+dZ12iXfr9tF8+BDHghkHBaJd1dMbjQpWWockGYZrdjiP2S4J41EX+soxcxvw/QIcuHSLg24uK5+0oohqBbmtrJl2hSz8szowrMT0+TUGrFOz4qjx+b6hqiIYiozXsew1V76wPiw841utPI7wG33UGofTy0E+JakJ93VRL2CC8nRJiH/2J0rZFVfdf9Qu4OktqMcVsC26bLJnIGE5ihI2lWqysyimQ=="
client = DataAPIClient("AstraCS:NuOPNaPZoxjUTeOBZanBukps:13d0c0c42cb255108c4ff848b4b41c5b0ba9a5721edd63619a1755cb9ca992f5")
db = client.get_database_by_api_endpoint("https://4c5ec6df-6240-4e0e-a17c-ea5acc0a7531-us-east-2.apps.astra.datastax.com")
#print(f"Connected to Astra DB: {db.list_collection_names()}")
print(f"Connected to Astra DB: {db.name()}")

# ## LLm Models
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS

# ## Bedrock Clients
session = boto3.Session(
    aws_access_key_id='ASIA52HHHYLHGFJDD2GY',
    aws_secret_access_key='cXJ7AVarcdXOv24VdWp/RXQOlmtpreNIAggBddv2',
    aws_session_token= 'IQoJb3JpZ2luX2VjEEIaCXVzLWVhc3QtMiJIMEYCIQDbBlAHyzbcea95QpaogFzPZ3KimTtd/xL5thoinsvQcQIhAOM+IOrtPt2/Xvr4PZUa24YjDSVsLc8NWlsZMUO6zR+gKvQCCKv//////////wEQABoMOTQ5NjcyNzIzMTUwIgwnDGprKDZAU0BCt/4qyAI1dp5cZzvKVfMfmISuiVJfoWIR/3yK8ES2rzWi0ueBdjNrPpObQ/GPcdFlogeRFldSGGsaD5vmacuapu7hXgTb55AAU/GhWIX1NgNnHsoOG2NcvstoVIFpKTXQK0MOtWIcNvw7z1K8FoD1xQZdIwiBIIQuZXYjMmyDGsRj7/kVAevXuFHSMd/Z71IcxAf8YsXYMHF1nc5ObTLTvqnCtBOtw+8xOSEH0XZld4bOFvpYqNO2r4aWf7xCiJ6EIyq5kxM+Xvg1niukQdyzZJkfjQedvyCX8eq9uN80t91I1w0xE5PawzGVI3vkbiJtS1CU/vw/BysMCFNvqVeEipcJ7wOoWHxRAn7tyT7RbUWlSOtuFWYoSC/3sG/FF/4lTK9X16KPD4T9/ky2f+d8mbKVIPBOFS3rOZ9AEpAEOoPcYu1hRJbV/w+kGQhOMPzlk7IGOqYB+dZ12iXfr9tF8+BDHghkHBaJd1dMbjQpWWockGYZrdjiP2S4J41EX+soxcxvw/QIcuHSLg24uK5+0oohqBbmtrJl2hSz8szowrMT0+TUGrFOz4qjx+b6hqiIYiozXsew1V76wPiw841utPI7wG33UGofTy0E+JakJ93VRL2CC8nRJiH/2J0rZFVfdf9Qu4OktqMcVsC26bLJnIGE5ihI2lWqysyimQ=='
)
#bedrock = session.client('bedrock-runtime', region_name='us-east-1')
bedrock=boto3.client(service_name="bedrock-runtime", region_name="us-east-1")
bedrock_embeddings=BedrockEmbeddings(model_id="amazon.titan-embed-text-v1",client=bedrock)

# ## Data ingestion
from poc.util.parser import count_paper_titles_and_extract_text
def data_ingestion():
    # loader=PyPDFDirectoryLoader("/Users/chethana/Downloads/advanced_rag_chethana/pdfs")
    # documents=loader.load()
    # text_splitter=RecursiveCharacterTextSplitter(chunk_size=10000,chunk_overlap=1000)
    # docs=text_splitter.split_documents(documents)
    extracted_text = count_paper_titles_and_extract_text("https://proceedings.mlr.press/v222/")
    combined_text = "\n".join(extracted_text)
    documents = []
    for text in extracted_text:
        # Create a dictionary representing a document with a single attribute 'content'
        document = {"content": text}
        documents.append(document)

    return documents
    #return docs

# ## Vector Embedding and vector store
token="AstraCS:ysImOkpETfJsAebhQPmFNoLB:7f6f14e98c3c03758881fc1704c066a7c5dfe9334a9f432b047d601d6fc5385d",
api_endpoint="https://4c5ec6df-6240-4e0e-a17c-ea5acc0a7531-us-east-2.apps.astra.datastax.com"
ASTRA_DB_KEYSPACE = None
# cassio.init(
#     token=token,
#     database_id=api_endpoint,
#     keyspace=ASTRA_DB_KEYSPACE if ASTRA_DB_KEYSPACE else None,
# )
# #def get_vector_store(docs):
#     embedding = bedrock_embeddings
#     token=os.getenv("AstraCS:NuOPNaPZoxjUTeOBZanBukps:13d0c0c42cb255108c4ff848b4b41c5b0ba9a5721edd63619a1755cb9ca992f5"),
#     api_endpoint="https://4c5ec6df-6240-4e0e-a17c-ea5acc0a7531-us-east-2.apps.astra.datastax.com"
#     keyspace = None 
#     if not token or not api_endpoint:
#         st.error("Astra DB environment variables not set. Please ensure ASTRA_DB_APPLICATION_TOKEN and ASTRA_DB_API_ENDPOINT are correctly configured.")
#         return None
#     try:
#         # vectorstore = Cassandra(
#         #     #collection_name="test",
#         #     embedding=embedding,
#         #     token=token,
#         #     api_endpoint=api_endpoint
#         # )
#         vector_store = Cassandra(
#             embedding=bedrock_embeddings,
#             table_name="rag",
#             session=None,  # <-- meaning: use the global defaults from cassio.init()
#             keyspace=None,  # <-- meaning: use the global defaults from cassio.init()
#         )
#     except Exception as e:
#         st.error(f"Error creating AstraDBVectorStore: {e}")
#         return None
#     vectorstore.save_local("astra_index")
#     return vectorstore
def get_vector_store(docs):
    vectorstore=FAISS.from_documents(
        docs,
        bedrock_embeddings
    )
    vectorstore.save_local("faiss_index")
    return vectorstore
def get_claude_llm():
    llm=Bedrock(model_id="ai21.j2-mid-v1",client=bedrock,model_kwargs={'maxTokens':512})
    return llm

def get_llama2_llm():
    llm=Bedrock(model_id="meta.llama2-70b-chat-v1",client=bedrock,model_kwargs={'max_gen_len':512})
    
    return llm

prompt_template = """

Human: Use the following pieces of context to provide a 
concise answer to the question at the end but usse atleast summarize with 
250 words with detailed explaantions. If you don't know the answer, 
just say that you don't know, don't try to make up an answer.
<context>
{context}
</context

Question: {question}

Assistant:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

def get_response_llm(llm,vectorstore,query):
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(
        search_type="similarity", search_kwargs={"k": 3}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT})
    answer=qa({"query":query})
    return answer['result']


def main():
    st.set_page_config("Chat PDF")
    
    st.header("ML Proceedings Advanced RAG Model")

    user_question = st.text_input("Ask a Question from the PDF Files")

    with st.sidebar:
        st.title("Update Or Create Vector Store:")
        
        if st.button("Vectors Update"):
            with st.spinner("Processing..."):
                docs = data_ingestion()
                get_vector_store(docs)
                st.success("Done")

    if st.button("Claude Output"):
        with st.spinner("Processing..."):
            llm=get_claude_llm()          
            astra_index = get_vector_store(docs)
            st.write(get_response_llm(llm,astra_index,user_question))
            st.success("Done")

    if st.button("Llama2 Output"):
        with st.spinner("Processing..."):
            astra_index = get_vector_store(docs)
            llm=get_llama2_llm()
            st.write(get_response_llm(llm,astra_index,user_question))
            st.success("Done")

if __name__ == "__main__":
    main()













