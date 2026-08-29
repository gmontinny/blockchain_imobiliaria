import json
from typing import Optional

from sqlalchemy.orm import Session

from app.blockchain import SmartContract, create_block_from_record
from app.models import BlockchainRecord, Listing
from app.schemas import ListingCreate


def _parse_float(value) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(str(value).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return None


def _parse_int(value) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def get_last_block_hash(db: Session) -> str:
    last = db.query(BlockchainRecord).order_by(BlockchainRecord.block_index.desc()).first()
    return last.block_hash if last else "0" * 64


def get_next_block_index(db: Session) -> int:
    last = db.query(BlockchainRecord).order_by(BlockchainRecord.block_index.desc()).first()
    return (last.block_index + 1) if last else 1


def register_on_blockchain(db: Session, listing: Listing, action: str) -> BlockchainRecord:
    contract = SmartContract()
    valid, message = contract.validate_transaction(listing.id, action)

    block_data = {
        "listing_id": listing.listing_id,
        "city": listing.city,
        "neighborhood": listing.neighborhood,
        "price": listing.price,
        "usable_area": listing.usable_area,
        "business_type": listing.business_type,
        "action": action,
    }

    block = create_block_from_record(
        index=get_next_block_index(db),
        data=block_data,
        previous_hash=get_last_block_hash(db),
    )

    record = BlockchainRecord(
        block_index=block.index,
        listing_id=listing.listing_id,
        action=action,
        block_hash=block.hash,
        previous_hash=block.previous_hash,
        block_data=json.dumps(block.data, ensure_ascii=False),
        contract_valid=block.data.get("contract_valid", valid),
        contract_message=block.data.get("contract_validation", message),
        timestamp=block.timestamp,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def create_listing(db: Session, data: ListingCreate) -> tuple[Listing, BlockchainRecord]:
    if data.listing_id:
        existing = db.query(Listing).filter(Listing.listing_id == data.listing_id).first()
        if existing:
            block_record = register_on_blockchain(db, existing, "UPDATE")
            return existing, block_record

    listing = Listing(**data.model_dump())
    db.add(listing)
    db.commit()
    db.refresh(listing)
    block_record = register_on_blockchain(db, listing, "REGISTER")
    return listing, block_record


def get_listings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    city: Optional[str] = None,
    business_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> list[Listing]:
    query = db.query(Listing)
    if city:
        query = query.filter(Listing.city.ilike(f"%{city}%"))
    if business_type:
        query = query.filter(Listing.business_type == business_type)
    if min_price is not None:
        query = query.filter(Listing.price >= min_price)
    if max_price is not None:
        query = query.filter(Listing.price <= max_price)
    return query.offset(skip).limit(limit).all()


def get_listing_by_id(db: Session, listing_id: int) -> Optional[Listing]:
    return db.query(Listing).filter(Listing.id == listing_id).first()


def get_blockchain_records(db: Session, skip: int = 0, limit: int = 100) -> list[BlockchainRecord]:
    return db.query(BlockchainRecord).order_by(BlockchainRecord.block_index).offset(skip).limit(limit).all()


def validate_blockchain_integrity(db: Session) -> dict:
    records = db.query(BlockchainRecord).order_by(BlockchainRecord.block_index).all()
    invalid_blocks = []

    for i, record in enumerate(records):
        if i > 0:
            expected_previous = records[i - 1].block_hash
            if record.previous_hash != expected_previous:
                invalid_blocks.append(record.block_index)

    return {
        "is_valid": len(invalid_blocks) == 0,
        "total_blocks": len(records),
        "invalid_blocks": invalid_blocks,
        "message": "Blockchain íntegra." if not invalid_blocks else f"{len(invalid_blocks)} bloco(s) inválido(s) detectado(s).",
    }
