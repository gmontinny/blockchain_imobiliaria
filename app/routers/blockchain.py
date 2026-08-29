from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud import get_blockchain_records, validate_blockchain_integrity
from app.database import get_db
from app.schemas import BlockchainRecordResponse, BlockchainValidationResponse

router = APIRouter(prefix="/blockchain", tags=["Blockchain"])


@router.get(
    "/records",
    response_model=list[BlockchainRecordResponse],
    summary="Listar blocos da blockchain",
    description="Retorna todos os blocos registrados na cadeia, em ordem cronológica. Cada bloco contém o hash SHA-256, o hash do bloco anterior e o resultado da validação do smart contract.",
)
def listar_blocos(
    skip: int = Query(0, ge=0, description="Número de registros a pular (paginação)"),
    limit: int = Query(100, ge=1, le=500, description="Máximo de blocos retornados"),
    db: Session = Depends(get_db),
):
    return get_blockchain_records(db, skip, limit)


@router.get(
    "/validate",
    response_model=BlockchainValidationResponse,
    summary="Validar integridade da blockchain",
    description="Percorre todos os blocos em ordem e verifica se o `previous_hash` de cada bloco corresponde ao `block_hash` do bloco anterior. Qualquer adulteração é detectada e os índices dos blocos inválidos são retornados.",
)
def validar_blockchain(db: Session = Depends(get_db)):
    return validate_blockchain_integrity(db)
