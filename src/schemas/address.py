from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    """
    Base schema for address data shared across request and response models.
    """
    name: str = Field(..., max_length=100)
    street: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    postal_code: str = Field(..., max_length=10)
    country: str = Field(..., max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class AddressCreate(AddressBase):
    """
    Schema for creating a new address.
    """
    pass


class AddressUpdate(BaseModel):
    """
    Schema for updating an existing address with partial fields.
    """
    name: Optional[str] = Field(None, max_length=100)
    street: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(..., max_length=10)
    country: Optional[str] = Field(None, max_length=100)
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)


class AddressRead(AddressBase):
    """
    Schema for returning address data in API responses.
    """
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
