# FastAPI Introduction

FastAPI is a modern Python web framework used for building APIs.

## Features

- High Performance
- Automatic API Documentation
- Type Validation
- Async Support

## Dependency Injection

FastAPI provides dependency injection using the Depends function.

Example:

```python
from fastapi import Depends

def get_db():
    return "database"

@app.get("/users")
def get_users(db=Depends(get_db)):
    return {"db": db}
```

## Routing

FastAPI uses decorators for routing.

Example:

```python
@app.get("/users")
def get_users():
    return {"users": []}
```