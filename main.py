from fastapi import FastAPI
from database import engine, Base
from models import models
from routes import clientes, pos_venda, nps, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bom Controle NPS")

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(pos_venda.router)
app.include_router(nps.router)

@app.get("/")
def root():
    return {"message": "API Bom Controle NPS está funcionando!"}