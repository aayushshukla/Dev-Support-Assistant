import requests

BASE_URL = "http://127.0.0.1:8000"


def generate_code(
    prompt
):

    response = requests.post(
        f"{BASE_URL}/generate-code",
        json={
            "prompt": prompt
        }
    )

    return response.json()