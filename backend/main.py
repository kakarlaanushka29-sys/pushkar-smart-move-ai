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
roads = [
    {"id": 1, "name": "Main Road to Ghat A", "level": "HIGH", "closed": False, "time_min": 25},
    {"id": 2, "name": "Bypass Road via Parking B", "level": "MODERATE", "closed": False, "time_min": 18},
    {"id": 3, "name": "Riverside Road", "level": "LOW", "closed": False, "time_min": 22},
]

class RoadUpdate(BaseModel):
    level: Optional[str] = None
    closed: Optional[bool] = None
    time_min: Optional[int] = None

LEVELS = ["LOW", "MODERATE", "HIGH"]

@app.get("/traffic")
def get_traffic():
    return {"simulated": True, "roads": roads}

@app.put("/traffic/{road_id}")
def update_road(road_id: int, data: RoadUpdate):
    for r in roads:
        if r["id"] == road_id:
            if data.level is not None:
                if data.level not in LEVELS:
                    raise HTTPException(status_code=400, detail="Invalid level")
                r["level"] = data.level
            if data.closed is not None:
                r["closed"] = data.closed
            if data.time_min is not None:
                if data.time_min < 0:
                    raise HTTPException(status_code=400, detail="Invalid time")
                r["time_min"] = data.time_min
            return r
    raise HTTPException(status_code=404, detail="Road not found")

@app.get("/traffic/route")
def best_route():
    rank = {"LOW": 0, "MODERATE": 1, "HIGH": 2}
    open_roads = [r for r in roads if not r["closed"]]
    if not open_roads:
        return {"message": "All routes closed"}
    best = min(open_roads, key=lambda r: (r["time_min"] + rank[r["level"]] * 5))
    return {"simulated": True, "recommended": best}
@app.get("/journey")
def journey():
    # 1. Best parking (not nearly full)
    options = [add_status(p) for p in parking if add_status(p)["status"] != "FULL_RISK"]
    if not options:
        return {"message": "All parking nearly full. Please wait or ask staff."}
    best_parking = max(options, key=lambda x: x["available"])

    # 2. Shuttle from that parking
    shuttle = None
    for s in shuttle_routes:
        if s["name"].startswith(best_parking["name"]) and s["status"] != "Disrupted":
            shuttle = shuttle_view(s)
            break
    if shuttle is None:
        return {"message": "No shuttle available from recommended parking.",
                "parking": best_parking}

    # 3. Best road to parking area (simulated)
    rank = {"LOW": 0, "MODERATE": 1, "HIGH": 2}
    open_roads = [r for r in roads if not r["closed"]]
    road = min(open_roads, key=lambda r: r["time_min"] + rank[r["level"]] * 5) if open_roads else None

    wait_min = shuttle["interval_min"] // 2 if shuttle["demand"] != "HIGH" else shuttle["interval_min"]
    return {
        "simulated": True,
        "road": road,
        "parking": best_parking,
        "shuttle": shuttle,
        "est_wait_min": wait_min,
        "ghat": "Ghat A",
    }
crowd_zones = [
    {"id": 1, "name": "Ghat A", "level": "NORMAL", "alt": "Ghat B", "approved": False},
    {"id": 2, "name": "Ghat B", "level": "NORMAL", "alt": "Ghat A", "approved": False},
    {"id": 3, "name": "Entry Gate C", "level": "NORMAL", "alt": "Ghat B", "approved": False},
]

CROWD_LEVELS = ["NORMAL", "INCREASING", "CRITICAL"]

class CrowdUpdate(BaseModel):
    level: Optional[str] = None
    approved: Optional[bool] = None

def crowd_view(z):
    alt = next(x for x in crowd_zones if x["name"] == z["alt"])
    suggested = z["level"] == "CRITICAL" and alt["level"] != "CRITICAL"
    return {**z, "diversion_suggested": suggested, "alt_level": alt["level"]}

@app.get("/crowd")
def get_crowd():
    return {"manual_input": True, "zones": [crowd_view(z) for z in crowd_zones]}

@app.put("/crowd/{zone_id}")
def update_crowd(zone_id: int, data: CrowdUpdate):
    for z in crowd_zones:
        if z["id"] == zone_id:
            if data.level is not None:
                if data.level not in CROWD_LEVELS:
                    raise HTTPException(status_code=400, detail="Invalid level")
                if data.level != z["level"]:
                    z["approved"] = False  # old approval cancelled
                z["level"] = data.level
            if data.approved is not None:
                if data.approved and not crowd_view(z)["diversion_suggested"]:
                    raise HTTPException(status_code=400, detail="No valid diversion to approve")
                z["approved"] = data.approved
            return crowd_view(z)
    raise HTTPException(status_code=404, detail="Zone not found")
import copy

# Server start ayinappudu unna seed values ni save chesukuntundi
SEED = {
    "parking": copy.deepcopy(parking),
    "shuttle": copy.deepcopy(shuttle_routes),
    "roads": copy.deepcopy(roads),
    "crowd": copy.deepcopy(crowd_zones),
}

@app.post("/reset")
def reset_demo():
    parking[:] = copy.deepcopy(SEED["parking"])
    shuttle_routes[:] = copy.deepcopy(SEED["shuttle"])
    roads[:] = copy.deepcopy(SEED["roads"])
    crowd_zones[:] = copy.deepcopy(SEED["crowd"])
    sos_reports.clear()
    return {"message": "Demo data reset"}
import os
import hmac
from fastapi import Request # type: ignore
from fastapi.responses import JSONResponse # type: ignore

# Prototype PIN. Maarchali ante terminal lo: $env:ADMIN_PIN="1234" (server start mundu)
ADMIN_PIN = os.environ.get("ADMIN_PIN", "2027")

def needs_pin(method: str, path: str) -> bool:
    path = path.rstrip("/") or "/"
    if method == "PUT":
        return True
    if method == "GET" and path in ("/sos", "/admin/check"):
        return True
    if method == "POST" and path == "/reset":
        return True
    return False

@app.middleware("http")
async def admin_guard(request: Request, call_next):
    if needs_pin(request.method, request.url.path):
        sent = request.headers.get("x-admin-pin", "")
        if not hmac.compare_digest(sent.encode(), ADMIN_PIN.encode()):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing admin PIN"},
                headers={"Access-Control-Allow-Origin": request.headers.get("origin", "*")},
            )
    return await call_next(request)

@app.get("/admin/check")
def admin_check():
    return {"ok": True}