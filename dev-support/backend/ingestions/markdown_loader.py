from pathlib import Path

from backend.utils.tech_detector import (
    detect_technology
)


def load_markdown(file_path):

    content = Path(
        file_path
    ).read_text(
        encoding="utf-8"
    )

    title = (
        content.split("\n")[0]
        .replace("#", "")
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

            "category": "Markdown",

            "title": title,

            "content_text": content,

            "code_examples": None,

            "tags": None,

            "agent_role": "Knowledge Base"
        }

    ]