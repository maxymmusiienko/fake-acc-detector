from fastapi import FastAPI, HTTPException
from stats import get_current_stats

app = FastAPI()

@app.get("/stats")
def get_all_stats():
    stats = get_current_stats()
    return stats

@app.get("/stats/{user_id}")
def get_stats_by_user(user_id: int):
    stats = get_current_stats()
    if user_id in stats:
        return {user_id: stats[user_id]}
    else:
        raise HTTPException(status_code=404, detail="User not found")
