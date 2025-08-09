
from fastapi import FastAPI
from .database import Base, engine
from . import models
from .routers import auth, animals, tasks, stocks, exports

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Refuge MVP+ API")

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth.router)
app.include_router(animals.router)
app.include_router(tasks.router)
app.include_router(stocks.router)
app.include_router(exports.router)
