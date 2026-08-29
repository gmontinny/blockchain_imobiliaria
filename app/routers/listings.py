from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud import create_listing, get_listing_by_id, get_listings
from app.database import get_db
from app.schemas import ListingCreate, ListingResponse

router = APIRouter(prefix="/listings", tags=["Imóveis"])


@router.post(
    "/",
    response_model=ListingResponse,
    status_code=201,
    summary="Cadastrar novo imóvel",
    description="Cadastra um imóvel e registra a transação na blockchain. Se o `listing_id` já existir, registra um evento de atualização na cadeia sem duplicar o imóvel.",
)
def cadastrar_imovel(data: ListingCreate, db: Session = Depends(get_db)):
    listing, _ = create_listing(db, data)
    return listing


@router.get(
    "/",
    response_model=list[ListingResponse],
    summary="Listar imóveis com filtros",
    description="Retorna a lista de imóveis cadastrados. Permite filtrar por cidade, tipo de negócio (RENTAL, SALE, RENTAL_SALE) e faixa de preço.",
)
def listar_imoveis(
    skip: int = Query(0, ge=0, description="Número de registros a pular (paginação)"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de registros retornados"),
    city: str | None = Query(None, description="Filtrar por cidade (busca parcial)"),
    business_type: str | None = Query(None, description="Tipo de negócio: RENTAL, SALE ou RENTAL_SALE"),
    min_price: float | None = Query(None, description="Preço mínimo"),
    max_price: float | None = Query(None, description="Preço máximo"),
    db: Session = Depends(get_db),
):
    return get_listings(db, skip, limit, city, business_type, min_price, max_price)


@router.get(
    "/{listing_id}",
    response_model=ListingResponse,
    summary="Buscar imóvel por ID",
    description="Retorna todos os dados de um imóvel específico pelo seu ID interno.",
)
def buscar_imovel_por_id(listing_id: int, db: Session = Depends(get_db)):
    listing = get_listing_by_id(db, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado.")
    return listing
