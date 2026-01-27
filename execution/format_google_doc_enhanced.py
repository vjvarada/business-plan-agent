#!/usr/bin/env python3
"""Enhanced Google Doc Formatter"""
import json
import os
import re
import sys

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/documents"]


def get_creds():
    return Credentials.from_authorized_user_file("token.json", SCOPES)


def format_doc(doc_id, md_file):
    creds = get_creds()
    docs = build("docs", "v1", credentials=creds)

    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = docs.documents().get(documentId=doc_id).execute()
    end_idx = doc["body"]["content"][-1]["endIndex"] - 1

    reqs = [{"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_idx}}}]
    docs.documents().batchUpdate(documentId=doc_id, body={"requests": reqs}).execute()
    print("Cleared content")

    reqs = []
    idx = 1

    in_table = False
    table_rows = []

    for line in lines:
        line = line.rstrip()

        # Handle empty lines
        if not line.strip():
            if not in_table:
                continue
            else:
                # End of table
                if table_rows:
                    # Insert table content as text
                    for row in table_rows:
                        txt = row + "\n"
                        reqs.append(
                            {"insertText": {"location": {"index": idx}, "text": txt}}
                        )
                        idx += len(txt)
                    table_rows = []
                    in_table = False
                continue

        # Table detection
        if line.startswith("|"):
            in_table = True
            table_rows.append(line)
            continue
        elif line.startswith("---"):
            continue

        # Headers
        if line.startswith("# "):
            txt = line.lstrip("# ").strip() + "\n\n"
            reqs.append({"insertText": {"location": {"index": idx}, "text": txt}})
            reqs.append(
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": idx, "endIndex": idx + len(txt) - 1},
                        "paragraphStyle": {"namedStyleType": "HEADING_1"},
                        "fields": "namedStyleType",
                    }
                }
            )
            idx += len(txt)
        elif line.startswith("## "):
            txt = line.lstrip("#").strip() + "\n\n"
            reqs.append({"insertText": {"location": {"index": idx}, "text": txt}})
            reqs.append(
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": idx, "endIndex": idx + len(txt) - 1},
                        "paragraphStyle": {"namedStyleType": "HEADING_2"},
                        "fields": "namedStyleType",
                    }
                }
            )
            idx += len(txt)
        elif line.startswith("### "):
            txt = line.lstrip("#").strip() + "\n\n"
            reqs.append({"insertText": {"location": {"index": idx}, "text": txt}})
            reqs.append(
                {
                    "updateParagraphStyle": {
                        "range": {"startIndex": idx, "endIndex": idx + len(txt) - 1},
                        "paragraphStyle": {"namedStyleType": "HEADING_3"},
                        "fields": "namedStyleType",
                    }
                }
            )
            idx += len(txt)
        # Bullets
        elif line.startswith("- "):
            txt = line.lstrip("- ").strip() + "\n"
            start = idx
            reqs.append({"insertText": {"location": {"index": idx}, "text": txt}})
            reqs.append(
                {
                    "createParagraphBullets": {
                        "range": {"startIndex": start, "endIndex": idx + len(txt)},
                        "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE",
                    }
                }
            )
            idx += len(txt)
        # Quotes
        elif line.startswith("> "):
            txt = line.lstrip("> ").strip() + "\n"
            start = idx
            reqs.append({"insertText": {"location": {"index": idx}, "text": txt}})
            reqs.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": idx + len(txt) - 1},
                        "textStyle": {"italic": True},
                        "fields": "italic",
                    }
                }
            )
            idx += len(txt)
        # Normal text
        else:
            if line.strip():
                txt = line + "\n"
                reqs.append({"insertText": {"location": {"index": idx}, "text": txt}})
                idx += len(txt)

    for i in range(0, len(reqs), 50):
        batch = reqs[i : i + 50]
        docs.documents().batchUpdate(
            documentId=doc_id, body={"requests": batch}
        ).execute()
        print(f"Batch {i//50 + 1}/{(len(reqs)-1)//50 + 1}")

    print(f"\nFormatted: https://docs.google.com/document/d/{doc_id}/edit")


if __name__ == "__main__":
    format_doc(sys.argv[1], sys.argv[2])
