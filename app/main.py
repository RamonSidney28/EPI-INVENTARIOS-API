from fastapi import FastAPI
from app.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="EPI Inventory API", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "EPI Inventory API"}
