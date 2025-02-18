from langsmith import Client

client = Client(api_key="changeme")
client.delete_project(project_name="changeme")