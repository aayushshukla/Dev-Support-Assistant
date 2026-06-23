"""
CSV Loader

Loads CSV records and converts them into
a standard document structure.
"""

import pandas as pd


def load_csv(file_path):

    df = pd.read_csv(file_path)

    documents = []

    for _, row in df.iterrows():

        documents.append({

            "source_url":
            str(row["source_url"])
            if pd.notna(row["source_url"])
            else None,

            "domain":
            str(row["domain"])
            if pd.notna(row["domain"])
            else None,

            "domain_group":
            str(row["domain_group"])
            if pd.notna(row["domain_group"])
            else None,

            "category":
            str(row["category"])
            if pd.notna(row["category"])
            else None,

            "title":
            str(row["title"])
            if pd.notna(row["title"])
            else None,

            "content_text":
            str(row["content_text"])
            if pd.notna(row["content_text"])
            else None,

            "code_examples":
            str(row["code_examples"])
            if pd.notna(row["code_examples"])
            else None,

            "tags":
            str(row["tags"])
            if pd.notna(row["tags"])
            else None,

            "agent_role":
            str(row["agent_role"])
            if pd.notna(row["agent_role"])
            else "upload"
        })

    return documents