from dotenv import load_dotenv

# Load environment variables first, before any imports that use them
load_dotenv()

from fastapi import FastAPI
from app.api.StockRouter import router
from app.repository.DatabaseManager import DatabaseManager

app = FastAPI()

# Initialize database on startup
db = DatabaseManager()
db.init_db()

# include routers
app.include_router(router)