from typing import List, Optional

from langflow.components.vectorstores.base.model import LCVectorStoreComponent
from langflow.field_typing import Text

from langflow.field_typing import Embeddings
from langflow.interface.custom.custom_component import CustomComponent
from langflow.schema.schema import Record
from langchain_community.vectorstores.documentdb import (
    DocumentDBSimilarityType,
    DocumentDBVectorSearch,
)


class DocumentDBSearchComponent(LCVectorStoreComponent):
    display_name = "DocumentDB Search"
    description = "Search a DocumentDB Vector Store for similar documents."

    def build_config(self):
        return {
            "search_type": {
                "display_name": "Search Type",
                "options": ["Similarity", "MMR"],
            },
            "input_value": {"display_name": "Input"},
            "embedding": {"display_name": "Embedding"},
            "collection_name": {"display_name": "Collection Name"},
            "db_name": {"display_name": "Database Name"},
            "index_name": {"display_name": "Index Name"},
            "documentdb_connection_url": {"display_name": "DocumentDB Connection URL"},
            "number_of_results": {
                "display_name": "Number of Results",
                "info": "Number of results to return.",
                "advanced": True,
            },
            "dimensions": {"display_name": "Dimension"},
            "similarity_algorithm": {
                "display_name": "Search Type",
                "options": ["COS", "EUC", "DOT"],
            },
        }

    def build(  # type: ignore[override]
            self,
            input_value: Text,
            search_type: str,
            embedding: Embeddings,
            number_of_results: int = 4,
            collection_name: str = "",
            db_name: str = "",
            index_name: str = "",
            documentdb_connection_url: str = "",
            dimensions: int = 1536,
            similarity_algorithm: str = "COS",
    ) -> List[Record]:

        vector_store = self.DocumentDBComponent().build(
            documentdb_connection_url=documentdb_connection_url,
            collection_name=collection_name,
            db_name=db_name,
            embedding=embedding,
            index_name=index_name,
            dimensions=dimensions,
        )
        if not vector_store:
            raise ValueError("Failed to create Document DB Vector Store")
        return self.search_with_vector_store(
            vector_store=vector_store, input_value=input_value, search_type=search_type, k=number_of_results
        )

    class DocumentDBComponent(CustomComponent):
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
