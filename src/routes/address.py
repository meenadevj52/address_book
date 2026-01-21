from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from src.core.database import get_session
from src.schemas.address import AddressCreate, AddressRead, AddressUpdate
from src.services.address_service import AddressService
from src.utils.geo import geocode_address

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(
    data: AddressCreate,
    session: Session = Depends(get_session),
):
    """
    Create a new address record.
    """
    try:
        return AddressService.create_address(session, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{address_id}", response_model=AddressRead)
def get_address(
    address_id: str,
    session: Session = Depends(get_session),
):
    """
    Retrieve an address by its unique identifier.
    """
    try:
        return AddressService.get_address(session, address_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )


@router.put("/{address_id}", response_model=AddressRead)
def update_address(
    address_id: str,
    data: AddressUpdate,
    session: Session = Depends(get_session),
):
    """
    Update an existing address by its unique identifier.
    """
    try:
        return AddressService.update_address(session, address_id, data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: str,
    session: Session = Depends(get_session),
):
    """
    Delete an address by its unique identifier.
    """
    try:
        AddressService.delete_address(session, address_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )


@router.get("/search/", response_model=List[AddressRead])
def search_addresses(
    lat: Optional[float] = Query(None, ge=-90, le=90, description="Latitude of center point"),
    lon: Optional[float] = Query(None, ge=-180, le=180, description="Longitude of center point"),
    address: Optional[str] = Query(None, description="Optional human-readable address to geocode"),
    radius_km: float = Query(..., gt=0, description="Radius in kilometers"),
    session: Session = Depends(get_session),
):
    """
    Retrieve all addresses within a given radius from a location.
    - If `lat` and `lon` are provided, they are used as the center point.
    - If `address` is provided, it will be geocoded to get the center coordinates.
    """
    if address:
        coords = geocode_address(address)
        if not coords:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to geocode the provided address",
            )
        lat, lon = coords

    if lat is None or lon is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either coordinates or address must be provided",
        )

    return AddressService.get_addresses_within_radius(
        session=session, latitude=lat, longitude=lon, radius_km=radius_km
    )
