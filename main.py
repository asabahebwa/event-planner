from fastapi import FastAPI
from database.connection import Settings
from routes.users import user_router
from routes.events import event_router
import uvicorn

app = FastAPI(title="Event Planner API", version="1.0.0")

settings = Settings()

# register routes

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.on_event("startup")
async def init_db():
    await settings.initialize_database()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
