import json
import logging
from pathlib import Path
from typing import Generator, Optional

import pandas as pd
from sqlalchemy.orm import Session

from app.crud import register_on_blockchain
from app.models import Listing

CSV_PATH = Path(__file__).parent.parent.parent / "data" / "dataZAP.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def _safe_float(value) -> Optional[float]:
    if pd.isna(value) or str(value).strip().lower() in ("normal", "", "nan"):
        return None
    try:
        return float(str(value).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return None


def _safe_int(value) -> Optional[int]:
    if pd.isna(value) or str(value).strip().lower() in ("normal", "", "nan"):
        return None
    try:
        return int(float(str(value)))
    except (ValueError, TypeError):
        return None


def _safe_str(value) -> Optional[str]:
    if pd.isna(value) or str(value).strip().lower() in ("normal", "nan"):
        return None
    return str(value).strip()


def _safe_bool(value) -> bool:
    return str(value).strip().lower() == "true"


def _build_listing(row) -> Optional[Listing]:
    listing_id = _safe_str(row.get("listing.id"))
    if not listing_id:
        return None
    return Listing(
        listing_id=listing_id,
        external_id=_safe_str(row.get("listing.externalId")),
        license_number=_safe_str(row.get("account.licenseNumber")),
        account_name=_safe_str(row.get("account.name")),
        city=_safe_str(row.get("listing.address.city")),
        state=_safe_str(row.get("listing.address.state")),
        neighborhood=_safe_str(row.get("listing.address.neighborhood")),
        street=_safe_str(row.get("listing.address.street")),
        street_number=_safe_str(row.get("listing.address.streetNumber")),
        zip_code=_safe_str(row.get("listing.address.zipCode")),
        zone=_safe_str(row.get("listing.address.zone")),
        latitude=_safe_float(row.get("listing.address.point.lat")),
        longitude=_safe_float(row.get("listing.address.point.lon")),
        property_type=_safe_str(row.get("listing.propertyType")),
        listing_type=_safe_str(row.get("listing.listingType")),
        business_type=_safe_str(row.get("listing.pricingInfo.businessType")),
        bedrooms=_safe_int(row.get("listing.bedrooms")),
        bathrooms=_safe_int(row.get("listing.bathrooms")),
        suites=_safe_int(row.get("listing.suites")),
        parking_spaces=_safe_int(row.get("listing.parkingSpaces")),
        total_area=_safe_float(row.get("listing.totalAreas")),
        usable_area=_safe_float(row.get("listing.usableAreas")),
        unit_floor=_safe_int(row.get("listing.unitFloor")),
        price=_safe_float(row.get("listing.pricingInfo.price")),
        rental_price=_safe_float(row.get("listing.pricingInfo.rentalPrice")),
        sale_price=_safe_float(row.get("listing.pricingInfo.salePrice")),
        condo_fee=_safe_float(row.get("listing.pricingInfo.monthlyCondoFee")),
        iptu=_safe_float(row.get("listing.pricingInfo.yearlyIptu")),
        amenities=_safe_str(row.get("listing.amenities")),
        furnished=_safe_bool(row.get("listing.furnished")),
        pool=_safe_bool(row.get("listing.pool")),
        gym=_safe_bool(row.get("listing.gym")),
        barbgrill=_safe_bool(row.get("listing.barbgrill")),
        title=_safe_str(row.get("listing.title")),
        description=_safe_str(row.get("listing.description")),
        publication_type=_safe_str(row.get("listing.publicationType")),
        portal=_safe_str(row.get("listing.portal")),
        is_inactive=_safe_bool(row.get("listing.isInactive")),
    )


def import_csv(db: Session) -> dict:
    df = pd.read_csv(CSV_PATH, sep=";", dtype=str, on_bad_lines="skip")
    total = len(df)
    imported = 0
    skipped = 0

    logger.info("Iniciando importação: %d linhas encontradas no CSV.", total)

    for i, (_, row) in enumerate(df.iterrows(), start=1):
        listing = _build_listing(row)
        if not listing:
            skipped += 1
            logger.debug("[%d/%d] Ignorado: listing.id ausente.", i, total)
            continue

        exists = db.query(Listing).filter(Listing.listing_id == listing.listing_id).first()
        if exists:
            skipped += 1
            logger.debug("[%d/%d] Ignorado: '%s' já existe.", i, total, listing.listing_id)
            continue

        db.add(listing)
        db.flush()
        register_on_blockchain(db, listing, "REGISTER")
        imported += 1
        logger.info("[%d/%d] ✔ Importado: '%s' — %s, %s", i, total, listing.listing_id, listing.city, listing.neighborhood)

    db.commit()
    logger.info("Importação concluída: %d importados, %d ignorados.", imported, skipped)

    return {
        "total_imported": imported,
        "total_skipped": skipped,
        "message": f"{imported} imóveis importados, {skipped} ignorados.",
    }


def import_csv_stream(db: Session) -> Generator[str, None, None]:
    """Gerador SSE: emite eventos de progresso linha a linha."""
    df = pd.read_csv(CSV_PATH, sep=";", dtype=str, on_bad_lines="skip")
    total = len(df)
    imported = 0
    skipped = 0

    def _event(data: dict) -> str:
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    yield _event({"status": "started", "total": total, "message": f"{total} linhas encontradas no CSV."})
    logger.info("[SSE] Iniciando importação: %d linhas.", total)

    for i, (_, row) in enumerate(df.iterrows(), start=1):
        listing = _build_listing(row)
        if not listing:
            skipped += 1
            yield _event({"status": "skipped", "row": i, "total": total, "reason": "listing.id ausente"})
            continue

        exists = db.query(Listing).filter(Listing.listing_id == listing.listing_id).first()
        if exists:
            skipped += 1
            yield _event({"status": "skipped", "row": i, "total": total, "listing_id": listing.listing_id, "reason": "já existe"})
            continue

        db.add(listing)
        db.flush()
        register_on_blockchain(db, listing, "REGISTER")
        imported += 1
        logger.info("[SSE] [%d/%d] ✔ '%s' — %s", i, total, listing.listing_id, listing.city)
        yield _event({
            "status": "imported",
            "row": i,
            "total": total,
            "listing_id": listing.listing_id,
            "city": listing.city,
            "neighborhood": listing.neighborhood,
            "imported_so_far": imported,
            "skipped_so_far": skipped,
        })

    db.commit()
    logger.info("[SSE] Concluído: %d importados, %d ignorados.", imported, skipped)
    yield _event({
        "status": "done",
        "total_imported": imported,
        "total_skipped": skipped,
        "message": f"{imported} imóveis importados, {skipped} ignorados.",
    })
