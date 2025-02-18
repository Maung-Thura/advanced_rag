FROM python:3.11-slim

LABEL maintainer="maungthura2024@u.northwestern.edu"

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN pip3 install --upgrade pip

COPY ./requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade -r /tmp/requirements.txt

RUN apt update

RUN apt install -y apache2

RUN apt install -y apache2-utils

RUN apt install curl

RUN apt install -y wget

RUN apt clean

COPY ./index.html /var/www/html/

# Apache HTTP port
EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]

RUN mkdir advancedrag

# Set the working directory
WORKDIR /advancedrag

RUN wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

COPY cronjob/upload_ml_research_papers_to_s3.py /home/ubuntu/advancedrag/

# Langflow server port
EXPOSE 7860

# DocumentDB port
EXPOSE 27017

RUN export LANGCHAIN_TRACING_V2=true

RUN export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"

RUN export LANGCHAIN_API_KEY="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"

RUN export LANGCHAIN_PROJECT="advancedrag"

COPY ./langflow/cache/langflow-pre.db /home/ubuntu/.cache/langflow/

COPY ./langflow/cache/monitor.duckdb /home/ubuntu/.cache/langflow/

CMD ["python", "-m", "langflow", "run", "--host", "0.0.0.0", "--port", "7860"]
