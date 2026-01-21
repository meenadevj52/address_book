# Address_Book
An address book application where API users can create, update and delete addresses.

---

## Features

- Create, read, update, and delete addresses.
- Store latitude and longitude coordinates for each address.
- Auto-fill coordinates if missing using **manual geocoding logic**.
- Search addresses **within a given radius** from a point.
- Flexible search:
  - Users can provide **latitude & longitude** directly.
  - Users can provide a **human-readable address**, which is automatically converted to coordinates.
- Built using **FastAPI**, **SQLModel**, and **SQLite**.
- Structured logging with console and rotating file handlers.

---

## Design Decisions

1. **Optional coordinates for addresses**  
   - When creating or updating an address, `latitude` and `longitude` are optional.  
   - If not provided, the application generates coordinates manually (for testing purposes).  
   - Users can still provide exact coordinates if they prefer.  

2. **Geocoding**
   - For simplicity and free testing, **Google Maps API is not used**.  
   - Manual coordinates or testing coordinates were used instead.  
   - In a production setup, you could integrate **Google Geocoding API** or another mapping API.

3. **Distance search**
   - Addresses can be searched **within a specified radius** using the Haversine formula.  
   - Users can search either by providing **coordinates** or a **human-readable address**.

---

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLModel
- **Validation:** Pydantic
- **Dependency Management:** uv
- **Geocoding:** OpenStreetMap Nominatim (for testing)
- **Distance Calculation:** Haversine formula
- **Logging:** Python logging module

 ---


### Setup Instructions

1. Clone the repository

    ```bash
    git clone <repo_url>
    cd address_book
    ```

2. Install uv
   ```
   pip install uv
   ```

2. Install project dependencies  
   ```bash
   uv sync
   ```

3. Run the API
   ```bash
   uv run uvicorn src.main:app --reload
   ```

4. Optional: Add GOOGLE_API_KEY if integrating Google API in production.

--- 


## **Performance & Scalability**
   - Currently, a **bounding box filter** is applied in SQL and addresses are filtered within a radius using the Haversine formula in Python.  
   - For small datasets (SQLite), this works fine, but it **loads all addresses into memory**.  
   - For production or larger datasets, a **spatial database** like **PostGIS (PostgreSQL)** or **Spatialite (SQLite extension)** can be used to store coordinates as spatial types and perform radius queries **directly in the database**, which is faster and more scalable.  
   
