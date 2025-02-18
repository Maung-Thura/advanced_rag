from typing import List, Optional

from langflow.field_typing import Embeddings
from langflow.interface.custom.custom_component import CustomComponent
from langflow.schema.schema import Record
from langchain_community.vectorstores.documentdb import (
    DocumentDBSimilarityType,
    DocumentDBVectorSearch,
)


# from sklearn.decomposition import PCA


class DocumentDBComponent(CustomComponent):
    display_name = "Document DB"
    description = "Construct a Document DB Vector Search` vector store from raw documents."
    icon = "MongoDB"

    def build_config(self):
        return {
            "inputs": {"display_name": "Input", "input_types": ["Document", "Record"]},
            "embedding": {"display_name": "Embedding"},
            "collection_name": {"display_name": "Collection Name"},
            "db_name": {"display_name": "Database Name"},
            "index_name": {"display_name": "Index Name"},
            "documentdb_connection_url": {"display_name": "DocumentDB Connection URL"},
            "dimensions": {"display_name": "Dimension"},
            "similarity_algorithm": {
                "display_name": "Search Type",
                "options": ["COS", "EUC", "DOT"],
            },
        }

    def build(
            self,
            embedding: Embeddings,
            inputs: Optional[List[Record]] = None,
            collection_name: str = "",
            db_name: str = "",
            index_name: str = "",
            documentdb_connection_url: str = "",
            dimensions: int = 1536,
            similarity_algorithm: str = "COS",
    ) -> DocumentDBVectorSearch:

        if similarity_algorithm == "COS":
            sim_algorithm = DocumentDBSimilarityType.COS
        elif similarity_algorithm == "EUC":
            sim_algorithm = DocumentDBSimilarityType.EUC
        elif similarity_algorithm == "DOT":
            sim_algorithm = DocumentDBSimilarityType.DOT
        else:
            raise ImportError("Invalid Similarity Algorithm. Only COS and EUC are allowed.")

        # Assuming 'embeddings' is your 4096-dimensional embeddings matrix
        # pca = PCA(n_components=1536)
        # reduced_embeddings = pca.fit_transform(embedding)

        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError("Please install pymongo to use MongoDB Atlas Vector Store")
        try:
            mongo_client: MongoClient = MongoClient(documentdb_connection_url)
            collection = mongo_client[db_name][collection_name]
        except Exception as e:
            raise ValueError(f"Failed to connect to MongoDB Atlas: {e}")

        documents = []
        for _input in inputs or []:
            if isinstance(_input, Record):
                documents.append(_input.to_lc_document())
            else:
                documents.append(_input)
        if documents:
            vector_store = DocumentDBVectorSearch.from_documents(
                documents=documents,
                embedding=embedding,
                collection=collection,
                index_name=index_name,
            )
        else:
            vector_store = DocumentDBVectorSearch(
                embedding=embedding,
                collection=collection,
                index_name=index_name,
            )

        # specify similarity algorithm, valid options are:
        #   cosine (COS), euclidean (EUC), dot product (DOT)
        if not vector_store.index_exists():
            vector_store.create_index(dimensions, sim_algorithm)
        return vector_store
