from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from routes.reviews import router as review_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Tables created successfully.")
    yield
    #shutdown code can be added here if needed
    print("Application shutdown.")

app = FastAPI(
    lifespan=lifespan,
    title="Rangmanch Review App",
    description="An API for managing reviews of plays.",
    )

app.include_router(review_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Rangmanch Review App!"}