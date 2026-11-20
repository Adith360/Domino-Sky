"""
Domino Sky - Unit Tests & Verification Suite
============================================
Comprehensive test suite validating deterministic simulation,
passenger cascade logic, crew duty limits, and AI dispatcher grounding.
"""

import pytest
from simulator import SimulationEngine, time_to_min, min_to_time
from ai_dispatcher import AIDispatcher


@pytest.fixture(scope="module")
def engine():
    return SimulationEngine()


@pytest.fixture(scope="module")
def dispatcher():
    return AIDispatcher()


def test_time_conversions():
    """Verify bidirectional minute-to-HH:MM conversion logic."""
    assert time_to_min("00:00") == 0
    assert time_to_min("01:30") == 90
    assert time_to_min("12:00") == 720
    assert time_to_min("23:59") == 1439
    assert min_to_time(0) == "00:00"
    assert min_to_time(90) == "01:30"
    assert min_to_time(720) == "12:00"


def test_baseline_network(engine):
    """Verify undisturbed baseline network conditions."""
    res = engine.run_simulation()
    k = res["kpis"]
    assert k["total_flights"] == 70
    assert k["on_time_flights"] == 70
    assert k["delayed_flights"] == 0
    assert k["total_delay_minutes"] == 0
    assert k["broken_connections"] == 0
    assert k["stranded_passengers"] == 0
    assert k["crew_duty_violations"] == 0


def test_mumbai_prompt_story(engine):
    """
    Verifies the hackathon prompt's exact scenario:
    A 90-minute storm at Mumbai (15:00-16:30) cascades to Kolkata flight DS0304
    and pushes crew CR03 into statutory duty violation (+35m overage).
    """
    res = engine.run_simulation("BOM", "15:00", "16:30")
    k = res["kpis"]
    assert k["delayed_flights"] == 3
    assert k["total_delay_minutes"] == 150
    assert k["crew_duty_violations"] == 1

    # Check Kolkata leg
    kolkata_flight = res["flights"]["DS0304"]
    assert kolkata_flight["dep_delay"] == 45
    assert kolkata_flight["destination"] == "CCU"

    # Check crew CR03 violation
    cr03 = next(c for c in res["crews"] if c["crew_id"] == "CR03")
    assert cr03["status"] == "DUTY_EXCEEDED"
    assert cr03["overage_mins"] == 35


def test_mumbai_monsoon_cascade(engine):
    """
    Verifies morning monsoon storm at BOM (07:30-09:00):
    Causes 16 delayed flights, 755 delay mins, and 199 stranded passengers.
    """
    res = engine.run_simulation("BOM", "07:30", "09:00")
    k = res["kpis"]
    assert k["delayed_flights"] == 16
    assert k["total_delay_minutes"] == 755
    assert k["stranded_passengers"] == 199
    assert k["broken_connections"] == 6


def test_spare_aircraft_recovery(engine):
    """
    Tests that deploying spare VT-DS18 at DEL resolves the Kolkata cascade.
    """
    options = engine.evaluate_recovery_options("BOM", "15:00", "16:30")
    assert len(options) > 0
    top = options[0]
    assert "VT-DS18" in top["target_tail"] or "VT-DS18" in str(top.get("swap_dict", {}))
    assert top["delta"]["crew_violations_saved"] == 1


def test_fleet_balance_round_trip_cancellation(engine):
    """
    Tests that round-trip spoke pairs can be cancelled to preserve hub positioning.
    """
    options = engine.evaluate_recovery_options("BOM", "07:30", "09:00")
    pair_cancellations = [o for o in options if "CANCEL_PAIR" in o["id"]]
    assert len(pair_cancellations) > 0


def test_ai_dispatcher_grounding(engine, dispatcher):
    """
    Verifies zero-hallucination constraint: AI Dispatcher numbers must
    exactly match deterministic simulation KPIs.
    """
    res = engine.run_simulation("BOM", "15:00", "16:30")
    options = engine.evaluate_recovery_options("BOM", "15:00", "16:30")
    briefing = dispatcher.generate_briefing(res, options)

    impact = briefing["operational_impact"]
    assert impact["delayed_flights_count"] == res["kpis"]["delayed_flights"]
    assert impact["total_delay_minutes"] == res["kpis"]["total_delay_minutes"]
    assert impact["stranded_passengers"] == res["kpis"]["stranded_passengers"]
    assert impact["crew_violations_count"] == res["kpis"]["crew_duty_violations"]
    assert "BOM" in briefing["incident_summary"]


def test_delhi_fog_scenario(engine):
    """Verifies morning low-visibility disruption at DEL."""
    res = engine.run_simulation("DEL", "08:00", "10:00")
    k = res["kpis"]
    assert k["delayed_flights"] > 0
    assert k["total_delay_minutes"] > 0
