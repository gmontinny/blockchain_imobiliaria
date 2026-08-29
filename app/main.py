from fastapi import FastAPI

from app.database import Base, engine
from app.routers import blockchain, importer, listings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blockchain Imobiliária",
    description="API imobiliária com blockchain e smart contracts usando dados do ZAP Imóveis.",
    version="1.0.0",
)

app.include_router(listings.router)
app.include_router(blockchain.router)
app.include_router(importer.router)


@app.get("/", tags=["Status"], summary="Verificar status da API", description="Retorna o status atual da API. Use para confirmar que o servidor está no ar.")
def health_check():
    return {"status": "ok", "message": "Blockchain Imobiliária API"}
