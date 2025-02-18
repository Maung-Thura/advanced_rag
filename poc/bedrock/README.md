# Advanced RAG using Bedrock and DocumentDB


## Links
- [Corpora](https://us-east-2.console.aws.amazon.com/s3/buckets/jph6705-msai490-practicum?region=us-east-2&bucketType=general&tab=objects)
- [Embeddings](https://us-east-2.console.aws.amazon.com/s3/buckets/jph6705-msai490-practicum?region=us-east-2&bucketType=general&tab=objects)


## Flow of Control
- **build_corpora.py** (download research papers)
- **build_contextual_embeddings.py** (generate embeddings)
- **build_s3_bucket.py** (save both to s3 bucket)
- **build_document_db.py** (store vectors to document db for quick search)
- **invoke_llm.py** (invoke llm with query + additional context)


## Key Decisions
- LLM - Llama, freely available through bedrock
- Embeddings - Hugging face, freely usable through hugging face sdk
- Embeddings input - Text, we are using text to generate embeddings for now, however we will extend the input to images and tables (code added to **build_context_embeddings.py**)

## To Do
- To tie up of fetching context and llm invoker
- To add a simple UI