from fastapi import FastAPI
from database import engine, Base
from models import models
from routes import clientes, pos_venda, nps, auth, relatorios
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bom Controle NPS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(pos_venda.router)
app.include_router(nps.router)
app.include_router(relatorios.router)

@app.get("/")
def root():
    return {"message": "API Bom Controle NPS está funcionando!"}