from fastapi import FastAPI
from stats import get_current_stats, get_stats_by_id
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev purposes; restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/stats")
def stats_list():
    return get_current_stats()

@app.get("/stats/{user_id}")
def stats_detail(user_id: int):
    return get_stats_by_id(user_id)

