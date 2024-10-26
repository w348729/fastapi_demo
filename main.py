from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.authentication import auth_router
from app.routers.story import story_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(story_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

