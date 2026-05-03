from dotenv import load_dotenv
from fastapi import FastAPI
from app.factory.Factory import Factory
from app.exception.ExceptionManager import ExceptionManager

# Load environment variables first, before any imports that use them
load_dotenv()

# Initialize database on startup
factory = Factory()

app = FastAPI()

ExceptionManager.register_handlers(app)

app.include_router(factory.get_stock_router())