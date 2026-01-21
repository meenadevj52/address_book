from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class AddressModel(SQLModel, table=True):
    __tablename__ = "addresses" 

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)

    name: str = Field(index=True, max_length=100)
    street: str = Field(max_length=255)
    city: str = Field(index=True, max_length=100)
    postal_code: str = Field(min_length=5, max_length=10)    
    country: str = Field(index=True, max_length=100)

    latitude: Optional[float] = Field(default=None, ge=-90, le=90) 
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
 
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)