
---

## File: `fastapi_routing.md`

```markdown
# FastAPI Routing

FastAPI uses decorators for routing.

## Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def get_users():
    return {"users": []}

Supported HTTP methods:

GET
POST
PUT
DELETE