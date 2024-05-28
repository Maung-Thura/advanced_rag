import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote

import logging
import boto3
from botocore.exceptions import ClientError
import io
import argparse

"""
python3 upload_ml_research_papers_to_s3.py -research_papers_url https://proceedings.mlr.press/v222/ 
-aws_access_key_id ACCESS_KEY -aws_secret_access_key SECRET_ACCESS_KEY 
-aws_session_token SESSION_TOKEN -s3_bucket_name pvj8334-msai490-s3
"""


def download_pdfs_to_s3(url, s3_bucket_name, aws_access_key_id, aws_secret_access_key, aws_session_token):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        download_links = soup.find_all('a', string='Download PDF')

        count = 0
        for i, link in enumerate(download_links):
            pdf_url = link['href']
            pdf_response = requests.get(pdf_url)

            if pdf_response.status_code == 200:
                file_name = unquote(urlparse(pdf_url).path.split("/")[-1])
                upload_file_to_s3(pdf_response.content, s3_bucket_name, file_name, aws_access_key_id,
                                  aws_secret_access_key, aws_session_token)


def upload_file_to_s3(file_contents: bytes, bucket, file_name, aws_access_key_id, aws_secret_access_key,
                      aws_session_token):
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                             aws_session_token=aws_session_token)
    try:
        fo = io.BytesIO(file_contents)
        response = s3_client.upload_fileobj(fo, bucket, file_name)
        logging.debug(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    # Read in input parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-research_papers_url', type=str)
    parser.add_argument('-aws_access_key_id', type=str)
    parser.add_argument('-aws_secret_access_key', type=str)
    parser.add_argument('-aws_session_token', type=str)
    parser.add_argument('-s3_bucket_name', type=str)

    opt = parser.parse_args()

    download_pdfs_to_s3(opt.research_papers_url, opt.s3_bucket_name, opt.aws_access_key_id, opt.aws_secret_access_key,
                        opt.aws_session_token)


if __name__ == "__main__":
    main()
