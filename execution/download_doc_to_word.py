#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download Google Docs business plan to local Word document (.docx).
"""

import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    return creds

def download_google_doc_to_docx(document_id, output_path):
    """Download Google Doc as Word document."""
    print(f"Connecting to Google Docs...")
    creds = get_credentials()
    
    # Get document title
    docs_service = build('docs', 'v1', credentials=creds)
    doc = docs_service.documents().get(documentId=document_id).execute()
    title = doc.get('title', 'Untitled')
    print(f"Found: {title}")
    
    # Download as .docx using Drive API
    drive_service = build('drive', 'v3', credentials=creds)
    
    request = drive_service.files().export_media(
        fileId=document_id,
        mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    
    done = False
    print("Downloading...")
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            print(f"  Download {int(status.progress() * 100)}%")
    
    # Save to file
    os.makedirs('.tmp', exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(file.getvalue())
    
    file_size_kb = len(file.getvalue()) / 1024
    
    print(f"\n Downloaded to local Word document!")
    print(f"   Title: {title}")
    print(f"   File: {output_path}")
    print(f"   Size: {file_size_kb:.1f} KB")
    print(f"\n Ready to open and edit in Word")
    
    return output_path

if __name__ == '__main__':
    document_id = "1ykrGQp-dnPtlOn9TtaYX8Bur-44s8gnrhSzV_01_lEw"
    output_path = ".tmp/RapidTools_Business_Plan_from_Cloud.docx"
    
    try:
        download_google_doc_to_docx(document_id, output_path)
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)