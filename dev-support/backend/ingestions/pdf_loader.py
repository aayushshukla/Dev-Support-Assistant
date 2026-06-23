"""
PDF Loader

Extracts text from PDF files and converts
it into the standard document format.
"""

from pypdf import PdfReader

from backend.utils.tech_detector import (
    detect_technology
)


def load_pdf(file_path):

    reader = PdfReader(
        file_path
    )

    content = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:

            content += text + "\n"

    title = (
        content.split("\n")[0]
        .strip()
    )

    domain = detect_technology(
        title,
        content
    )

    return [

        {

            "source_url": file_path,

            "domain": domain,

            "domain_group": "Uploaded Documents",

            "category": "PDF",

            "title": title,

            "content_text": content,

            "code_examples": None,

            "tags": None,

            "agent_role": "Knowledge Base"
        }

    ]