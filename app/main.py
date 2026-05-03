from dotenv import load_dotenv

# Load environment variables first, before any imports that use them
load_dotenv()

from fastapi import FastAPI
from app.factory.Factory import Factory


# Initialize database on startup
factory = Factory()

app = FastAPI()
app.include_router(factory.get_stock_router())