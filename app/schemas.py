from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ListingBase(BaseModel):
    listing_id: Optional[str] = None
    external_id: Optional[str] = None
    license_number: Optional[str] = None
    account_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    neighborhood: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    zip_code: Optional[str] = None
    zone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_type: Optional[str] = None
    listing_type: Optional[str] = None
    business_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    suites: Optional[int] = None
    parking_spaces: Optional[int] = None
    total_area: Optional[float] = None
    usable_area: Optional[float] = None
    unit_floor: Optional[int] = None
    price: Optional[float] = None
    rental_price: Optional[float] = None
    sale_price: Optional[float] = None
    condo_fee: Optional[float] = None
    iptu: Optional[float] = None
    amenities: Optional[str] = None
    furnished: Optional[bool] = False
    pool: Optional[bool] = False
    gym: Optional[bool] = False
    barbgrill: Optional[bool] = False
    title: Optional[str] = None
    description: Optional[str] = None
    publication_type: Optional[str] = None
    portal: Optional[str] = None
    is_inactive: Optional[bool] = False


class ListingCreate(ListingBase):
    pass


class ListingResponse(ListingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class BlockchainRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    block_index: int
    listing_id: Optional[str]
    action: str
    block_hash: str
    previous_hash: str
    contract_valid: bool
    contract_message: str
    timestamp: str
    created_at: Optional[datetime] = None


class BlockchainValidationResponse(BaseModel):
    is_valid: bool
    total_blocks: int
    invalid_blocks: list[int]
    message: str


class ImportResponse(BaseModel):
    total_imported: int
    total_skipped: int
    message: str
