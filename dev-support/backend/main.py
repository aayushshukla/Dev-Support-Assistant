from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def health_check():

    return {
        "status": "running"
    }


@app.post("/generate-code")
def generate_code(
    request: PromptRequest
):

    return {
        "agent": "Code Generator",
        "prompt": request.prompt,
        "generated_code": f"Code generated for: {request.prompt}"
    }