"""
Application definition
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from unittest.mock import MagicMock

# FastAPI app initialization
app = FastAPI()

# Allow CORS for your localhost (or any other domain you trust)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "https://hahehackathon.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mocked Pydantic model for validating incoming request data
class ItemUpdate(BaseModel):
    name: str
    description: str

# Mocked database interaction function (for testing purposes)
def mock_get_db():
    db = MagicMock()
    
    # Mock an existing item in the "database"
    db_item = MagicMock()
    db_item.id = 1
    db_item.name = "Mock Item"
    db_item.description = "Mock Description"
    
    # Mock the query filter method
    db.query().filter().first.return_value = db_item  # Simulating fetching the item from the "database"
    
    # Mock commit and refresh methods (they will do nothing)
    db.commit = MagicMock()
    db.refresh = MagicMock()

    yield db

# Endpoint to update an item (mocked database version)
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(mock_get_db)):
    # Fetch the existing item (using mock database)
    db_item = db.query().filter().first()
    
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    # Mock updating the item’s data
    db_item.name = item.name
    db_item.description = item.description

    # Simulate committing the transaction
    db.commit()
    db.refresh(db_item)

    return JSONResponse(content={"message": "Item updated successfully", "item": {"id": db_item.id, "name": db_item.name, "description": db_item.description}})


@app.get("/")
async def home():
    return JSONResponse({
  "busLine": "Bus 5",
  "route": "Hauptbahnhof - Altona",
  "totalStations": 5,
  "stations": [
    {
      "stationName": "Hauptbahnhof",
      "estimatedArrival": "12:05",
      "checkedPassengers": {
        "normal": 10,
        "wheelchair": 1,
        "elderly": 2
      }
    },
    {
      "stationName": "Jungfernstieg",
      "estimatedArrival": "12:12",
      "checkedPassengers": {
        "normal": 8,
        "wheelchair": 0,
        "elderly": 1
      }
    },
    {
      "stationName": "Sternschanze",
      "estimatedArrival": "12:20",
      "checkedPassengers": {
        "normal": 15,
        "wheelchair": 2,
        "elderly": 3
      }
    },
    {
      "stationName": "Holstenstraße",
      "estimatedArrival": "12:27",
      "checkedPassengers": {
        "normal": 7,
        "wheelchair": 0,
        "elderly": 4
      }
    },
    {
      "stationName": "Altona",
      "estimatedArrival": "12:35",
      "checkedPassengers": {
        "normal": 5,
        "wheelchair": 1,
        "elderly": 2
      }
    }
  ]
}
)


@app.get("/404")
async def missing():
    return JSONResponse({"error": "That's gonna be a 'no' from me."}, status_code=404)
