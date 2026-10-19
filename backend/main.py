from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware # type: ignore

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
from datetime import datetime
from typing import Optional

sos_reports = []

class SOSReport(BaseModel):
    category: str
    location: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    note: Optional[str] = ""

class StatusUpdate(BaseModel):
    status: str

STATUSES = ["Reported", "Acknowledged", "Team Assigned", "Help Arrived", "Resolved"]

@app.post("/sos")
def create_sos(r: SOSReport):
    report = {
        "id": len(sos_reports) + 1,
        "category": r.category,
        "location": r.location,
        "lat": r.lat,
        "lng": r.lng,
        "note": r.note,
        "status": "Reported",
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    sos_reports.append(report)
    return report

@app.get("/sos")
def list_sos():
    return list(reversed(sos_reports))

@app.get("/sos/{sos_id}")
def get_sos(sos_id: int):
    for s in sos_reports:
        if s["id"] == sos_id:
            return s
    raise HTTPException(status_code=404, detail="Not found")

@app.put("/sos/{sos_id}/status")
def update_sos(sos_id: int, data: StatusUpdate):
    if data.status not in STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")
    for s in sos_reports:
        if s["id"] == sos_id:
            s["status"] = data.status
            return s
    raise HTTPException(status_code=404, detail="Not found")
import math

shuttle_routes = [
    {"id": 1, "name": "Parking A → Ghat A", "capacity": 50, "running": 2, "interval_min": 10, "waiting": 30, "status": "Running"},
    {"id": 2, "name": "Parking B → Ghat A", "capacity": 50, "running": 2, "interval_min": 10, "waiting": 40, "status": "Running"},
]

class ShuttleUpdate(BaseModel):
    waiting: Optional[int] = None
    running: Optional[int] = None
    status: Optional[str] = None

SHUTTLE_STATUSES = ["Running", "Delayed", "Disrupted"]

def shuttle_view(r):
    load = r["waiting"] * 100 / (r["capacity"] * max(r["running"], 1))
    demand = "HIGH" if load >= 100 else "MEDIUM" if load >= 60 else "LOW"
    needed = math.ceil(r["waiting"] / r["capacity"])
    extra = max(0, needed - r["running"])
    if r["status"] == "Disrupted":
        suggestion = "Route disrupted. Use another route."
    elif extra > 0:
        suggestion = f"Suggest adding {extra} more shuttle(s). Admin to confirm."
    else:
        suggestion = "Enough shuttles for current demand."
    return {**r, "demand": demand, "extra_needed": extra, "suggestion": suggestion}

@app.get("/shuttle")
def list_shuttles():
    return [shuttle_view(r) for r in shuttle_routes]

@app.put("/shuttle/{route_id}")
def update_shuttle(route_id: int, data: ShuttleUpdate):
    for r in shuttle_routes:
        if r["id"] == route_id:
            if data.waiting is not None:
                if data.waiting < 0:
                    raise HTTPException(status_code=400, detail="Invalid waiting count")
                r["waiting"] = data.waiting
            if data.running is not None:
                if data.running < 0:
                    raise HTTPException(status_code=400, detail="Invalid shuttle count")
                r["running"] = data.running
            if data.status is not None:
                if data.status not in SHUTTLE_STATUSES:
                    raise HTTPException(status_code=400, detail="Invalid status")
                r["status"] = data.status
            return shuttle_view(r)
    raise HTTPException(status_code=404, detail="Route not found")