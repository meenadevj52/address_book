from datetime import datetime
from math import cos, radians
from typing import List, Tuple

from sqlmodel import Session, select

from src.models.address import AddressModel
from src.schemas.address import AddressCreate, AddressUpdate
from src.utils.geo import haversine_distance, geocode_address


class AddressService:
    """
    Service layer responsible for address-related business logic.
    """

    @staticmethod
    def create_address(session: Session, data: AddressCreate) -> AddressModel:
        """
        Create and persist a new address record.
        """
        if data.latitude is None or data.longitude is None:
            full_address = f"{data.street}, {data.city}, {data.country}"
            lat, lon = geocode_address(full_address)
            if lat is None or lon is None:
                raise ValueError("Unable to geocode address")
            data.latitude = lat
            data.longitude = lon
 
        address = AddressModel(**data.model_dump())
        session.add(address)
        session.commit()
        session.refresh(address)
        return address

    @staticmethod
    def get_address(session: Session, address_id: str) -> AddressModel:
        """
        Retrieve a single address by its unique identifier.
        """
        address = session.get(AddressModel, address_id)
        if not address:
            raise ValueError("Address not found")
        return address

    @staticmethod
    def update_address(
        session: Session,
        address_id: str,
        data: AddressUpdate,
    ) -> AddressModel:
        """
        Update an existing address record.
        """
        address = session.get(AddressModel, address_id)
        if not address:
            raise ValueError("Address not found")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(address, field, value)

        if address.latitude is None or address.longitude is None:
            full_address = f"{address.street}, {address.city}, {address.country}"
            lat, lon = geocode_address(full_address)
            address.latitude = lat
            address.longitude = lon
            
        address.updated_at = datetime.utcnow()
        session.add(address)
        session.commit()
        session.refresh(address)
        return address

    @staticmethod
    def delete_address(session: Session, address_id: str) -> None:
        """
        Delete an address record by its unique identifier.
        """
        address = session.get(AddressModel, address_id)
        if not address:
            raise ValueError("Address not found")

        session.delete(address)
        session.commit()

    @staticmethod
    def get_addresses_within_radius(
        session: Session,
        latitude: float,
        longitude: float,
        radius_km: float,
    ) -> List[AddressModel]:
        """
        Retrieve all addresses within a specified radius from a given location.
        """
        if radius_km <= 0:
            raise ValueError("Radius must be greater than zero")
        
        lat_delta = radius_km / 111
        lon_delta = radius_km / (111 * cos(radians(latitude)))

        stmt = select(AddressModel).where(
        AddressModel.latitude.between(latitude - lat_delta, latitude + lat_delta),
        AddressModel.longitude.between(longitude - lon_delta, longitude + lon_delta)
        )  
        addresses = session.exec(stmt).all()

        result = [
        addr for addr in addresses
        if haversine_distance(latitude, longitude, addr.latitude, addr.longitude) <= radius_km
    ]
        return result   
