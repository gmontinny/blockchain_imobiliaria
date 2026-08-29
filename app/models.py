from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    String,
    Text,
    DateTime,
    func,
)

from app.database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(String, unique=True, index=True)
    external_id = Column(String, index=True)

    # Agência
    license_number = Column(String)
    account_name = Column(String)

    # Endereço
    city = Column(String, index=True)
    state = Column(String, index=True)
    neighborhood = Column(String, index=True)
    street = Column(String)
    street_number = Column(String)
    zip_code = Column(String)
    zone = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    # Características
    property_type = Column(String)
    listing_type = Column(String)
    business_type = Column(String)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    suites = Column(Integer)
    parking_spaces = Column(Integer)
    total_area = Column(Float)
    usable_area = Column(Float)
    unit_floor = Column(Integer)

    # Preços
    price = Column(Float)
    rental_price = Column(Float)
    sale_price = Column(Float)
    condo_fee = Column(Float)
    iptu = Column(Float)

    # Comodidades
    amenities = Column(Text)
    furnished = Column(Boolean, default=False)
    pool = Column(Boolean, default=False)
    gym = Column(Boolean, default=False)
    barbgrill = Column(Boolean, default=False)

    # Publicação
    title = Column(String)
    description = Column(Text)
    publication_type = Column(String)
    portal = Column(String)
    is_inactive = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BlockchainRecord(Base):
    __tablename__ = "blockchain_records"

    id = Column(Integer, primary_key=True, index=True)
    block_index = Column(Integer, unique=True, index=True)
    listing_id = Column(String, index=True)
    action = Column(String)  # REGISTER, UPDATE, DEACTIVATE
    block_hash = Column(String, unique=True)
    previous_hash = Column(String)
    block_data = Column(Text)  # JSON serializado
    contract_valid = Column(Boolean)
    contract_message = Column(String)
    timestamp = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
