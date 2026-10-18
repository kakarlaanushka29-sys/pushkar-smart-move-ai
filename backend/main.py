from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

parking = [
    {"id": 1, "name": "Parking A", "capacity": 1000, "occupied": 980},
    {"id": 2, "name": "Parking B", "capacity": 800, "occupied": 500},
]

class OccupancyUpdate(BaseModel):
    occupied: int

def add_status(p):
    available = p["capacity"] - p["occupied"]
    percent = round(p["occupied"] * 100 / p["capacity"])
    if percent >= 90:
        status = "FULL_RISK"
    elif percent >= 70:
        status = "FILLING"
    else:
        status = "AVAILABLE"
    return {**p, "available": available, "percent": percent, "status": status}

@app.get("/parking")
def get_parking():
    return [add_status(p) for p in parking]

@app.put("/parking/{parking_id}")
def update_parking(parking_id: int, data: OccupancyUpdate):
    for p in parking:
        if p["id"] == parking_id:
            if data.occupied < 0 or data.occupied > p["capacity"]:
                raise HTTPException(status_code=400, detail="Invalid occupancy")
            p["occupied"] = data.occupied
            return add_status(p)
    raise HTTPException(status_code=404, detail="Parking not found")

@app.get("/parking/recommend")
def recommend():
    options = [add_status(p) for p in parking if add_status(p)["status"] != "FULL_RISK"]
    if not options:
        return {"message": "All parking nearly full"}
    return max(options, key=lambda x: x["available"])