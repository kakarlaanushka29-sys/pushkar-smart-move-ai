# PUSHKAR SMART MOVE AI

Smarter Mobility. Safer Pilgrimages.

Prototype for PS-05: Intelligent Traffic, Parking and Shuttle Management
(Godavari Pushkaralu 2027, Rajamahendravaram). Team: TRINETRA AI.

## Features
- Parking status and recommendation
- Shuttle demand and suggestions (admin confirms)
- Traffic and best route (simulated data)
- Journey planner
- Crowd alerts (manual input, diversion only after staff approval)
- SOS emergency reporting with live status
- English / Telugu / Hindi (Telugu and Hindi are drafts, need native-speaker review)

## Important
All traffic, shuttle, parking and crowd values are SIMULATED or manually entered.
No real sensors, CCTV or GPS fleet tracking. Data is in memory and resets on restart.
Admin page has no login yet (prototype only).
For emergencies, call 112.

## How to run
Terminal 1:
    cd backend
    python -m uvicorn main:app --reload

Terminal 2:
    cd web
    npm run dev

Open http://localhost:5173
API docs: http://127.0.0.1:8000/docs