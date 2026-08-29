from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ImportResponse
from app.services.importer import import_csv, import_csv_stream

router = APIRouter(prefix="/import", tags=["Importação"])


@router.post(
    "/csv",
    response_model=ImportResponse,
    summary="Importar imóveis do arquivo CSV",
    description=(
        "Lê o arquivo `data/dataZAP.csv` e importa os imóveis para o banco de dados. "
        "Registros já existentes (mesmo `listing_id`) são ignorados automaticamente, "
        "garantindo que reimportações não gerem duplicatas. "
        "Retorna o total de imóveis importados e ignorados ao final do processo. "
        "Para acompanhar o progresso linha a linha, use `GET /import/csv/stream`."
    ),
)
def importar_csv(db: Session = Depends(get_db)):
    return import_csv(db)


@router.get(
    "/csv/stream",
    summary="Importar CSV com progresso em tempo real (SSE)",
    description=(
        "Importa o arquivo `data/dataZAP.csv` transmitindo o progresso em tempo real "
        "via Server-Sent Events (SSE). Registros já existentes são ignorados. "
        "Cada evento é um JSON com os campos: "
        "`status` (started | imported | skipped | done), "
        "`row`, `total`, `listing_id`, `city`, `neighborhood`, "
        "`imported_so_far`, `skipped_so_far` e `message` (no evento final). "
        "**Não é possível testar streaming diretamente no Swagger.** "
        "Use: `curl -N http://localhost:8000/import/csv/stream`"
    ),
)
def importar_csv_stream(db: Session = Depends(get_db)):
    return StreamingResponse(
        import_csv_stream(db),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
