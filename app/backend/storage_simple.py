from azure.storage.blob import BlobServiceClient
import os

class SimpleStorageManager:
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service = BlobServiceClient.from_connection_string(connection_string)
        
    def upload_file(self, file, user_id):
        container_name = "user-documents"
        container_client = self.blob_service.get_container_client(container_name)
        
        # Create a unique blob name using user_id
        blob_name = f"{user_id}/{file.filename}"
        blob_client = container_client.get_blob_client(blob_name)
        
        # Upload the file
        blob_client.upload_blob(file)
        return blob_name 