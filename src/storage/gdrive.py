from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os
import pickle
from typing import List, Dict, Any
from .base import BaseStorage
import logging

SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveStorage(BaseStorage):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.folder_id = config["folder_id"]
        self.credentials_path = config["credentials_path"]
        self.service = self._get_drive_service()

    def _get_drive_service(self):
        creds = None
        token_path = os.path.join(os.path.dirname(self.credentials_path), "token.pickle")
        
        if os.path.exists(token_path):
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
                
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
                
        return build('drive', 'v3', credentials=creds)

    def upload_file(self, local_path: str, remote_name: str) -> str:
        try:
            file_metadata = {
                'name': remote_name,
                'parents': [self.folder_id]
            }
            
            media = MediaFileUpload(
                local_path,
                mimetype='application/pdf',
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            return file.get('id')
            
        except Exception as e:
            logging.error(f"Error uploading file to Google Drive: {str(e)}")
            return None

    def list_files(self) -> List[Dict[str, Any]]:
        try:
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents",
                fields="files(id, name, createdTime)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            logging.error(f"Error listing files from Google Drive: {str(e)}")
            return []
