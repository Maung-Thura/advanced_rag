pip3 install --upgrade pip

pip3 install langflow --pre --force-reinstall

pip3 install pyopenssl --upgrade

pip3 install sentence-transformers

sudo apt update

sudo apt install apache2

sudo chown -R ubuntu:ubuntu /var/www

sudo chown -R ubuntu:ubuntu /etc/apache2/

pip3 install -U langsmith

mkdir advancedrag

cd advancedrag || exit

mkdir research_papers

wget https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

git clone https://github.com/Maung-Thura/langflow.git

cp langflow/cache/langflow-pre.db /home/ubuntu/.cache/langflow/

cp langflow/cache/monitor.duckdb /home/ubuntu/.cache/langflow/

cp langflow/httpd.conf /home/ubuntu/advancedrag/

cp langflow/index.html /home/ubuntu/advancedrag/

cp langflow/start.sh /home/ubuntu/advancedrag/

cp langflow/upload_ml_research_papers_to_s3.py /home/ubuntu/advancedrag/