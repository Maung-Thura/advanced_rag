from typing import Optional

import langchain_cohere
from langchain_community.embeddings.cohere import CohereEmbeddings

from langchain_cohere import CohereEmbeddings

from langflow.custom import CustomComponent

# from cohere.types import ToolResult


class CohereEmbeddingsComponent(CustomComponent):
    display_name = "Cohere Embeddings"
    description = "Generate embeddings using Cohere models."

    def build_config(self):
        return {
            "cohere_api_key": {"display_name": "Cohere API Key", "password": True},
            "model": {"display_name": "Model", "default": "embed-english-light-v3.0", "advanced": True},
            "truncate": {"display_name": "Truncate", "advanced": True},
            "max_retries": {"display_name": "Max Retries", "advanced": True},
            "user_agent": {"display_name": "User Agent", "advanced": True},
            "request_timeout": {"display_name": "Request Timeout", "advanced": True},
        }

    def build(
        self,
        request_timeout: Optional[float] = None,
        cohere_api_key: str = "NFly8sZI4vSVY139kzn5hkwBiZhVDUONg3km1yiP",
        max_retries: int = 3,
        model: str = "embed-english-light-v3.0",
        truncate: Optional[str] = None,
        user_agent: str = "langchain",
    ) -> langchain_cohere.CohereEmbeddings:
        return langchain_cohere.CohereEmbeddings(  # type: ignore
            max_retries=max_retries,
            user_agent=user_agent,
            request_timeout=request_timeout,
            cohere_api_key=cohere_api_key,
            model=model,
            truncate=truncate,
        )

cc = CohereEmbeddingsComponent
cc.build(cc)
