from fastapi import FastAPI

from app.routers import auth, tasks

app = FastAPI(title="Task Tracker")
app.include_router(auth.router)
app.include_router(tasks.router)
