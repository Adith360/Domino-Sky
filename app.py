"""
Domino Sky: Flight Disruption Cascade & Recovery Simulator
FastAPI Backend Application
"""

import os
import json
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from simulator import SimulationEngine
from ai_dispatcher import AIDispatcher

app = FastAPI(
    title="Domino Sky: Flight Disruption & Recovery Simulator",
    version="1.0.0",
    description="Aviation disruption cascade simulation and AI dispatcher recovery platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SimulationEngine()
dispatcher = AIDispatcher()

@app.get("/api/network")
def get_network_baseline():
    """Returns baseline dataset: airports, flights, connections, crews, spares."""
    return {
        "meta": engine.meta,
        "airports": list(engine.airports.values()),
        "flights": list(engine.flights.values()),
        "connections": engine.connections,
        "crews": engine.crews,
        "spare_aircraft": engine.spare_aircraft,
        "baseline_simulation": engine.run_simulation()
    }

@app.post("/api/simulate")
def simulate(payload: Dict[str, Any] = Body(...)):
    """
    Runs deterministic simulation based on disruption and recovery inputs.
    """
    closed_airport = payload.get("closed_airport")
    closure_start = payload.get("closure_start")
    closure_end = payload.get("closure_end")
    cancelled_flight_ids = payload.get("cancelled_flight_ids", [])
    spare_swaps = payload.get("spare_swaps", {})

    result = engine.run_simulation(
        closed_airport=closed_airport,
        closure_start=closure_start,
        closure_end=closure_end,
        cancelled_flight_ids=cancelled_flight_ids,
        spare_swaps=spare_swaps
    )
    return result

@app.post("/api/evaluate_recovery")
def evaluate_recovery(payload: Dict[str, Any] = Body(...)):
    """
    Calculates quantified recovery recommendations for the active disruption.
    """
    closed_airport = payload.get("closed_airport")
    closure_start = payload.get("closure_start")
    closure_end = payload.get("closure_end")

    if not closed_airport or not closure_start or not closure_end:
        return {"options": []}

    options = engine.evaluate_recovery_options(closed_airport, closure_start, closure_end)
    return {"options": options}

@app.post("/api/ai_briefing")
def get_ai_briefing(payload: Dict[str, Any] = Body(...)):
    """
    Generates AI operations dispatcher briefing.
    """
    sim_data = payload.get("simulation_data")
    recovery_options = payload.get("recovery_options", [])
    api_key = payload.get("api_key")

    local_dispatcher = AIDispatcher(api_key=api_key) if api_key else dispatcher
    briefing = local_dispatcher.generate_briefing(sim_data, recovery_options)
    return briefing

# Serve static files and frontend
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(static_dir, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def serve_index():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Domino Sky - Building frontend...</h1>"

app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
