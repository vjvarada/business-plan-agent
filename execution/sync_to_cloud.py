#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync local files (.xlsx, .docx) to Google Drive.
Uploads and converts to Google Sheets/Docs format.

Usage:
    python sync_to_cloud.py --file .tmp/RapidTools_financial_model.xlsx
    python sync_to_cloud.py --file .tmp/business_plan.docx --folder-id FOLDER_ID
"""

import os
import sys
import argparse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def sync_to_cloud(filepath, folder_id=None):
    """Upload local file to Google Drive and convert to native format."""
    if not os.path.exists(filepath):
        print(f" File not found: {filepath}")
        sys.exit(1)
    
    creds = get_credentials()
    drive_service = build('drive', 'v3', credentials=creds)
    
    filename = os.path.basename(filepath)
    file_ext = os.path.splitext(filename)[1].lower()
    
    # Determine MIME types
    if file_ext == '.xlsx':
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        google_mime_type = 'application/vnd.google-apps.spreadsheet'
        doc_type = 'Google Sheets'
    elif file_ext == '.docx':
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        google_mime_type = 'application/vnd.google-apps.document'
        doc_type = 'Google Docs'
    else:
        print(f" Unsupported file type: {file_ext}")
        print("   Supported: .xlsx, .docx")
        sys.exit(1)
    
    print(f"Uploading {filename} to Google Drive...")
    
    # Upload and convert
    file_metadata = {
        'name': filename.replace(file_ext, ''),
        'mimeType': google_mime_type
    }
    
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(filepath, mimetype=mime_type, resumable=True)
    
    try:
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink'
        ).execute()
        
        file_id = file.get('id')
        url = file.get('webViewLink')
        
        print(f"\n Successfully uploaded to {doc_type}!")
        print(f"   Name: {file['name']}")
        print(f"   ID: {file_id}")
        print(f"   URL: {url}")
        
        return {
            'id': file_id,
            'name': file['name'],
            'url': url,
            'type': doc_type
        }
    
    except Exception as e:
        print(f"\n Error uploading file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Sync local files to Google Drive')
    parser.add_argument('--file', required=True, help='Path to local file (.xlsx or .docx)')
    parser.add_argument('--folder-id', help='Google Drive folder ID (optional)')
    
    args = parser.parse_args()
    
    result = sync_to_cloud(args.file, args.folder_id)
    print(f"\n File Type: {result['type']}")
    print(f" Share this URL with stakeholders")
    
    return result

if __name__ == '__main__':
    main()