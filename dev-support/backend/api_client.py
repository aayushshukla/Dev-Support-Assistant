import requests

BASE_URL = "http://localhost:8000"


def start_workflow(
    prompt,
    agents,
    project_type
):

    payload = {
        "prompt": prompt,
        "agents": agents,
        "project_type": project_type
    }

    response = requests.post(
        f"{BASE_URL}/workflow/start",
        json=payload
    )

    return response.json()


def get_workflow_status(
    workflow_id
):

    response = requests.get(
        f"{BASE_URL}/workflow/{workflow_id}"
    )

    return response.json()