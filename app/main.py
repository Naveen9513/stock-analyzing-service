from fastapi import FastAPI
from app.api.StockRouter import router  

app = FastAPI()

# include routers
app.include_router(router)