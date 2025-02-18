from typing import Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError
from langflow.base.data.utils import parallel_load_records, parse_text_file_to_record, retrieve_file_paths
from langflow.interface.custom.custom_component import CustomComponent
from langflow.schema import Record

import logging
from pathlib import Path
import os, shutil


class S3DirectoryComponent(CustomComponent):
    display_name = "Directory"
    description = "Recursively load files from a directory."
    icon = "folder"

    def build_config(self) -> Dict[str, Any]:
        return {
            "aws_access_key_id": {"display_name": "AWS Access Key ID"},
            "aws_secret_access_key": {"display_name": "AWS Secret Access Key"},
            "aws_session_token": {"display_name": "AWS Session Token"},
            "s3_bucket_name": {"display_name": "s3 Bucket Name"},
            "local_directory": {"display_name": "Local Directory"},
            "total_files_limit": {"display_name": "Total Files Limit"},
            "skip_file_download": {"display_name": "Skip File Download"},
            "types": {
                "display_name": "Types",
                "info": "File types to load. Leave empty to load all types.",
            },
            "depth": {"display_name": "Depth", "info": "Depth to search for files."},
            "max_concurrency": {"display_name": "Max Concurrency", "advanced": True},
            "load_hidden": {
                "display_name": "Load Hidden",
                "advanced": True,
                "info": "If true, hidden files will be loaded.",
            },
            "recursive": {
                "display_name": "Recursive",
                "advanced": True,
                "info": "If true, the search will be recursive.",
            },
            "silent_errors": {
                "display_name": "Silent Errors",
                "advanced": True,
                "info": "If true, errors will not raise an exception.",
            },
            "use_multithreading": {
                "display_name": "Use Multithreading",
                "advanced": True,
            },
        }

    def build(
            self,
            aws_access_key_id: str,
            aws_secret_access_key: str,
            aws_session_token: str,
            s3_bucket_name: str,
            local_directory: str,
            total_files_limit: int = 30,
            skip_file_download: bool = False,
            depth: int = 0,
            max_concurrency: int = 2,
            load_hidden: bool = False,
            recursive: bool = True,
            silent_errors: bool = False,
            use_multithreading: bool = True,
    ) -> List[Optional[Record]]:
        resolved_path = self.resolve_path(local_directory)
        if not skip_file_download:
            success = self.download_files_from_s3(local_directory, total_files_limit, s3_bucket_name, aws_access_key_id,
                                                  aws_secret_access_key,
                                                  aws_session_token)
            if not success:
                raise Exception("Failed to download research papers from s3.")

        file_paths = retrieve_file_paths(resolved_path, load_hidden, recursive, depth)
        loaded_records = []

        if use_multithreading:
            loaded_records = parallel_load_records(file_paths, silent_errors, max_concurrency)
        else:
            loaded_records = [parse_text_file_to_record(file_path, silent_errors) for file_path in file_paths]
        loaded_records = list(filter(None, loaded_records))
        self.status = loaded_records
        return loaded_records

    def download_files_from_s3(self, local_directory, total_files_limit, bucket, aws_access_key_id,
                               aws_secret_access_key,
                               aws_session_token):
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                                 aws_session_token=aws_session_token)
        try:
            if not local_directory.endswith("/"):
                local_directory += "/"
            file_list = s3_client.list_objects(Bucket=bucket)['Contents']
            Path(local_directory).mkdir(parents=True, exist_ok=True)
            file_count = 0

            for filename in os.listdir(local_directory):
                file_path = os.path.join(local_directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

            for key in file_list:
                local_file = local_directory + key['Key']
                if file_count < total_files_limit:
                    # print(key['Key'] + 'file downloaded')
                    s3_client.download_file(bucket, key['Key'], local_file)
                    file_count += 1
                else:
                    logging.warning('Total files limit has been reached. ' + key['Key'] + ' will not be processed.')
        except ClientError as e:
            logging.error(e)
            return False
        return True
