from fastapi import Depends, FastAPI
from pathlib import Path

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import agents, bikes

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(agents.app)
app.include_router(bikes.app)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
