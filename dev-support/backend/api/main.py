from fastapi import FastAPI

from backend.api.routes.query import (
    router as query_router
)

from backend.api.routes.upload import (
    router as upload_router
)

from backend.api.routes.index import (
    router as index_router
)

from backend.api.routes.stats import (
    router as stats_router
)

from backend.api.dashboard import (
    router as dashboard_router
)
from backend.api.routes.feedback import (
    router as feedback_router
)

app = FastAPI(

    title="Developer Support Assistant",

    version="1.0.0"
)


@app.get("/")
def health_check():

    return {

        "status": "running"
    }



app.include_router(
    query_router
)

app.include_router(
    upload_router
)

app.include_router(
    index_router
)

app.include_router(
    stats_router
)


app.include_router(
    dashboard_router
)

app.include_router(
    feedback_router
)