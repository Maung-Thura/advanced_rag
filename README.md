# Advanced RAG

### Technical Stack
* Ubuntu Linux
* Python 3.10 and above
* Langflow
* OpenAI LLM
* Hugging Face Embeddings
* AWS DocumentDB
* AWS EC2
* Apache HTTP Server
* LangSmith
* Docker
* Unix Shell
* Open SSL

### Langflow Custom Components
* S3DirectoryComponent.py - AWS S3 Directory
* DocumentDBComponent.py - Document DB Vector Store
* DocumentDBSearchComponent.py - Document DB Vector Search

### Ubuntu CRON Entry
* upload_ml_research_papers_to_s3.py - Upload Machine Learning (ML) research papers to AWS S3

### Apache HTTP Server
* index.html - landing page
* httpd.conf - inbound traffic routing configuration file 

### S3 File poller
* /cronjob/upload_ml_research_papers_to_s3.py - polls the pdf files from the given URL
```
python3 upload_ml_research_papers_to_s3.py -research_papers_url URL
-aws_access_key_id ACCESS_KEY -aws_secret_access_key SECRET_ACCESS_KEY 
-aws_session_token SESSION_TOKEN -s3_bucket_name BUCKET_NAME
```

### Setup Files
* Download Amazon DocumentDB Certificate Authority (CA) certificate 
```
wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
```
* install.sh - install the system via EC2 console
* start.sh - start the system via EC2 console 
* Dockerfile - build the system in docker container
* requirements.txt - required python libraries

### Langflow Model
* /langflow - model in SQLite
* advanced_rag_model.json - JSON representation of the model

### Miscellaneous
* Utilities tools are in - /poc/util
* findings.txt - manual testing observations

### LangSmithEvaluation
* LangSmithEvaluation.py - evaluates OpenAI LLM relevance, conciseness, coherence and detail

### DeepEval
* deepeval.py - evaluation metric for our RAG system based on faithfulness and answer relevancy

### Deployment
#### Option 1
* Spin up DocumentDB database version 5 with db.r6g.xlarge compute power
* Spin up Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.2.0 (Ubuntu 20.04) 20240507 AMI with g5.2xlarge GPU and 32GB RAM compute power, 120GB storage AWS AMI EC2
* Set up networking by following [this YouTube link](https://www.youtube.com/watch?v=S4fBuj1HeAg&list=PLVHXCmfgqDrHKFqkBYaYmml0UofMu23j7&index=31)
* Download [install.sh](https://github.com/NU-MSAI-Practicum/advanced_rag_team_triad/blob/main/install.sh) into EC2
* Run install.sh as ubuntu user
```
sh install.sh
```
* Go into advancedrag directory
Run start.sh as ubuntu user
```
sh start.sh
```
#### Option 2
* Spin up DocumentDB database version 5 with db.r6g.xlarge compute power
* Download [Dockerfile](https://github.com/NU-MSAI-Practicum/advanced_rag_team_triad/blob/main/Dockerfile)
* Build docker image
```
docker build -t advanced_rag_team_triad:01 .
```
* Run docker image
```
docker run --name advanced_rag_team_triad_container -d -p 80:80 -p 7860:7860 -p 27017:27017 advanced_rag_team_triad:01
```
#### Option 3
* Spin up [Advanced_RAG_AWS_AMI](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#ImageDetails:imageId=ami-01b13bc920f0f19af)
* SSH pem files will be provided via separate channel 
* Setup S3 File Poller CRON job in EC2
* Connect to EC2 console and open crontab
```
Crontab -e
```
* Add a new CRON entry for 12:00 AM everyday, pleases replace credentials
```
0 0 * * * python3 /home/ubuntu/advancedrag/upload_ml_research_papers_to_s3.py upload_ml_research_papers_to_s3.py -research_papers_url https://proceedings.mlr.press/v222/ -aws_access_key_id ACCESS_KEY -aws_secret_access_key SECRET_ACCESS_KEY -aws_session_token SESSION_TOKEN -s3_bucket_name pvj8334-msai490-s3
```
