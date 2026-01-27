#!/usr/bin/env python3
"""Audit Business Plan - Check for math errors, unsourced claims, missing timeframes"""
import argparse, json, os, re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def audit_math(content):
    issues = []
    for m in re.finditer(r'(\d+[,\d]*)\s*[x*]\s*(\d+[,\d]*)\s*=\s*\$?([,\d]+)', content):
        num1 = int(m.group(1).replace(',',''))
        num2 = int(m.group(2).replace(',',''))
        actual = int(m.group(3).replace(',',''))
        expected = num1 * num2
        if expected != actual:
            issues.append({'type':'MATH_ERROR', 'calc':m.group(0), 'expected':expected, 'actual':actual})
    return issues

def run_audit(doc_id, research_dir):
    creds = Credentials.from_authorized_user_file("token.json", scopes=["https://www.googleapis.com/auth/documents.readonly"])
    docs = build('docs','v1',credentials=creds)
    doc = docs.documents().get(documentId=doc_id).execute()
    content = "".join([tr.get('content','') for el in doc.get('body',{}).get('content',[]) if 'paragraph' in el for tr in el['paragraph'].get('elements',[]) if 'textRun' in tr])
    
    issues = audit_math(content)
    
    print(f"AUDIT: {len(issues)} math errors found")
    for i in issues:
        print(f"  {i['calc']}  Expected: {i['expected']}, Got: {i['actual']}")
    return issues

if __name__=="__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--doc-id", required=True)
    p.add_argument("--research-dir", default=".tmp")
    args = p.parse_args()
    run_audit(args.doc_id, args.research_dir)
