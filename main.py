from fastapi import APIRouter, FastAPI
from src.route import user_route, payment_route
import uvicorn


app = FastAPI()

app.include_router(user_route)
app.include_router(payment_route)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True
    )