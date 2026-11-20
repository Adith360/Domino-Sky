"""
Domino Sky Advanced Deterministic Simulation Engine
Includes:
- Aircraft physical location tracking & fleet balance
- Round-trip cancellation pair support
- Minimum 30m turnaround preservation
- Ground Delay Program (GDP) at destination & ground holds at origin
- DGCA statutory 600m flight crew duty limits
- Exact passenger connection preservation & stranded pax calculations
"""

from typing import Dict, List, Set, Any, Optional, Tuple
from collections import defaultdict
import json
import os

def time_to_min(t: str) -> int:
    if not t:
        return 0
    h, m = map(int, t.split(':'))
    return h * 60 + m

def min_to_time(m: int) -> str:
    m = ((m % 1440) + 1440) % 1440
    return f"{m // 60:02d}:{m % 60:02d}"

class SimulationEngine:
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(cur_dir, "flight_network.json")
            if not os.path.exists(data_path):
                data_path = r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\flight_network.json"
        
        with open(data_path, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)
            
        self.meta = self.raw_data.get("meta", {})
        self.airports = {a["id"]: a for a in self.raw_data.get("airports", [])}
        self.flights = {f["flight_id"]: f for f in self.raw_data.get("flights", [])}
        self.connections = self.raw_data.get("connections", [])
        self.crews = self.raw_data.get("crews", [])
        self.spare_aircraft = self.raw_data.get("spare_aircraft", [])
        self.min_turnaround = self.meta.get("min_turnaround_minutes", 30)

        self.flights_by_tail = defaultdict(list)
        for f in self.raw_data.get("flights", []):
            self.flights_by_tail[f["tail_id"]].append(f)
        for tail in self.flights_by_tail:
            self.flights_by_tail[tail].sort(key=lambda x: x["leg_order"])

    def run_simulation(
        self,
        closed_airport: Optional[str] = None,
        closure_start: Optional[str] = None,
        closure_end: Optional[str] = None,
        cancelled_flight_ids: Optional[List[str]] = None,
        spare_swaps: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        cancellations = set(cancelled_flight_ids or [])
        swaps = spare_swaps or {}

        c_start = time_to_min(closure_start) if closure_start else None
        c_end = time_to_min(closure_end) if closure_end else None

        flight_results: Dict[str, Dict[str, Any]] = {}
        aircraft_chains: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        for orig_tail, flist in self.flights_by_tail.items():
            prev_arr_time: Optional[int] = None
            current_location: Optional[str] = flist[0]["origin"]
            active_tail = orig_tail

            for f in flist:
                fid = f["flight_id"]
                sched_dep = time_to_min(f["dep"])
                sched_arr = time_to_min(f["arr"])
                block = f["block_minutes"]
                pax = f["pax"]
                origin = f["origin"]
                dest = f["destination"]
                leg_order = f["leg_order"]

                # Check if swapped with a spare aircraft
                if fid in swaps:
                    active_tail = swaps[fid]
                    prev_arr_time = None
                    current_location = origin

                # Explicit Cancellation
                if fid in cancellations:
                    flight_results[fid] = {
                        "flight_id": fid,
                        "tail_id": active_tail,
                        "orig_tail_id": orig_tail,
                        "leg_order": leg_order,
                        "origin": origin,
                        "destination": dest,
                        "sched_dep": f["dep"],
                        "sched_arr": f["arr"],
                        "actual_dep": None,
                        "actual_arr": None,
                        "dep_delay": 0,
                        "arr_delay": 0,
                        "status": "CANCELLED",
                        "pax": pax,
                        "reasons": ["Flight proactively cancelled by dispatcher intervention"],
                        "root_cause": "Dispatcher Cancellation",
                        "is_cancelled": True,
                        "is_spare": False
                    }
                    aircraft_chains[active_tail].append(flight_results[fid])
                    # Note: Aircraft did not fly, so its location remains at origin
                    current_location = origin
                    continue

                # Aircraft Location Check (Fleet Balance)
                if current_location is not None and current_location != origin:
                    # Aircraft is physically stranded at another airport!
                    flight_results[fid] = {
                        "flight_id": fid,
                        "tail_id": active_tail,
                        "orig_tail_id": orig_tail,
                        "leg_order": leg_order,
                        "origin": origin,
                        "destination": dest,
                        "sched_dep": f["dep"],
                        "sched_arr": f["arr"],
                        "actual_dep": None,
                        "actual_arr": None,
                        "dep_delay": 0,
                        "arr_delay": 0,
                        "status": "CANCELLED",
                        "pax": pax,
                        "reasons": [f"Aircraft {active_tail} stranded at {current_location} due to upstream flight cancellation"],
                        "root_cause": "Aircraft Positioning Disruption",
                        "is_cancelled": True,
                        "is_spare": False
                    }
                    aircraft_chains[active_tail].append(flight_results[fid])
                    continue

                # Turnaround calculation
                reasons = []
                root_cause = "On Time"

                if prev_arr_time is None:
                    ready_dep = sched_dep
                else:
                    needed_ready = prev_arr_time + self.min_turnaround
                    if needed_ready > sched_dep:
                        turn_delay = needed_ready - sched_dep
                        ready_dep = needed_ready
                        reasons.append(f"Late inbound aircraft {active_tail} (arr +{turn_delay}m buffer deficit)")
                        root_cause = "Inbound Turnaround Delay"
                    else:
                        ready_dep = sched_dep

                dep_time = ready_dep

                # Origin Airport Closure
                if closed_airport and origin == closed_airport and c_start is not None and c_end is not None:
                    if (c_start <= dep_time < c_end) or (dep_time < c_start and sched_dep >= c_start):
                        reasons.append(f"Origin {origin} closed {closure_start}-{closure_end} (held on ground)")
                        dep_time = max(dep_time, c_end)
                        root_cause = f"Airport Closure: {origin}"

                # Destination Airport Closure (Ground Delay Program)
                if closed_airport and dest == closed_airport and c_start is not None and c_end is not None:
                    est_arr = dep_time + block
                    if c_start <= est_arr < c_end:
                        reasons.append(f"Destination {dest} closed {closure_start}-{closure_end} (held at {origin} by GDP)")
                        dep_time = c_end - block
                        root_cause = f"Airport Closure: {dest} (GDP)"

                arr_time = dep_time + block
                dep_delay = dep_time - sched_dep
                arr_delay = arr_time - sched_arr
                prev_arr_time = arr_time
                current_location = dest

                if dep_delay <= 0:
                    status = "ON_TIME"
                elif dep_delay < 60:
                    status = "DELAYED"
                else:
                    status = "SEVERELY_DELAYED"

                f_res = {
                    "flight_id": fid,
                    "tail_id": active_tail,
                    "orig_tail_id": orig_tail,
                    "leg_order": leg_order,
                    "origin": origin,
                    "destination": dest,
                    "sched_dep": f["dep"],
                    "sched_arr": f["arr"],
                    "actual_dep": min_to_time(dep_time),
                    "actual_arr": min_to_time(arr_time),
                    "dep_delay": dep_delay,
                    "arr_delay": arr_delay,
                    "status": status,
                    "pax": pax,
                    "reasons": reasons,
                    "root_cause": root_cause,
                    "is_cancelled": False,
                    "is_spare": (active_tail != orig_tail)
                }
                flight_results[fid] = f_res
                aircraft_chains[active_tail].append(f_res)

        # Evaluate Connections
        evaluated_connections = []
        stranded_passengers = 0
        broken_connections_count = 0

        for cx in self.connections:
            cid = cx["connection_id"]
            apt = cx["airport"]
            f1 = flight_results.get(cx["from_flight"])
            f2 = flight_results.get(cx["to_flight"])
            pax = cx["passengers"]
            min_connect = cx["min_connect_minutes"]

            status = "MAINTAINED"
            reason = "Connection successful"
            actual_transfer_time = None

            if not f1 or f1.get("is_cancelled"):
                status = "BROKEN"
                reason = f"Inbound flight {cx['from_flight']} was cancelled"
            elif not f2 or f2.get("is_cancelled"):
                status = "BROKEN"
                reason = f"Outbound flight {cx['to_flight']} was cancelled"
            else:
                f1_arr = time_to_min(f1["actual_arr"])
                f2_dep = time_to_min(f2["actual_dep"])
                actual_transfer_time = f2_dep - f1_arr
                if actual_transfer_time < min_connect:
                    status = "BROKEN"
                    reason = f"Transfer time {actual_transfer_time}m below minimum required {min_connect}m"

            if status == "BROKEN":
                stranded_passengers += pax
                broken_connections_count += 1

            evaluated_connections.append({
                "connection_id": cid,
                "airport": apt,
                "from_flight": cx["from_flight"],
                "to_flight": cx["to_flight"],
                "passengers": pax,
                "min_connect_minutes": min_connect,
                "actual_transfer_minutes": actual_transfer_time,
                "status": status,
                "reason": reason,
                "from_flight_arr": f1["actual_arr"] if f1 and not f1.get("is_cancelled") else "CANCELLED",
                "to_flight_dep": f2["actual_dep"] if f2 and not f2.get("is_cancelled") else "CANCELLED"
            })

        # Evaluate Crews
        evaluated_crews = []
        crew_violations_count = 0

        for cr in self.crews:
            cid = cr["crew_id"]
            tail = cr["tail_id"]
            base = cr["base"]
            d_start = time_to_min(cr["duty_start"])
            max_duty = cr["max_duty_mins"]
            fids = cr["flight_ids"]
            
            completed_flights = [flight_results[fid] for fid in fids if fid in flight_results and not flight_results[fid].get("is_cancelled")]
            
            if not completed_flights:
                actual_duty = 0
                status = "OFF_DUTY"
                overage = 0
                last_arrival = "N/A"
            else:
                last_f = completed_flights[-1]
                last_arrival = last_f["actual_arr"]
                actual_duty = time_to_min(last_arrival) - d_start
                overage = max(0, actual_duty - max_duty)
                status = "LEGAL" if overage == 0 else "DUTY_EXCEEDED"

            if status == "DUTY_EXCEEDED":
                crew_violations_count += 1

            evaluated_crews.append({
                "crew_id": cid,
                "tail_id": tail,
                "base": base,
                "duty_start": cr["duty_start"],
                "max_duty_mins": max_duty,
                "actual_duty_mins": actual_duty,
                "overage_mins": overage,
                "status": status,
                "flights_count": len(fids),
                "last_arrival": last_arrival
            })

        all_flights = list(flight_results.values())
        delayed_flights = [f for f in all_flights if f["dep_delay"] > 0 and not f.get("is_cancelled")]
        total_delay_minutes = sum(f["dep_delay"] for f in delayed_flights)
        cancelled_flights = [f for f in all_flights if f.get("is_cancelled")]
        cancelled_pax = sum(f["pax"] for f in cancelled_flights)
        
        est_delay_cost = sum(f["pax"] * (f["dep_delay"] / 60.0) * 500 for f in delayed_flights)
        est_cancellation_cost = cancelled_pax * 5000
        est_stranded_cost = stranded_passengers * 4000
        est_crew_penalty = crew_violations_count * 50000
        total_economic_cost = int(est_delay_cost + est_cancellation_cost + est_stranded_cost + est_crew_penalty)

        return {
            "meta": {
                "closed_airport": closed_airport,
                "closure_start": closure_start,
                "closure_end": closure_end,
                "cancelled_flights": list(cancellations),
                "spare_swaps": swaps
            },
            "kpis": {
                "total_flights": len(all_flights),
                "on_time_flights": len([f for f in all_flights if f["status"] == "ON_TIME" and not f.get("is_cancelled")]),
                "delayed_flights": len(delayed_flights),
                "severely_delayed_flights": len([f for f in all_flights if f["status"] == "SEVERELY_DELAYED"]),
                "cancelled_flights": len(cancelled_flights),
                "total_delay_minutes": total_delay_minutes,
                "average_delay_minutes": round(total_delay_minutes / len(delayed_flights), 1) if delayed_flights else 0,
                "broken_connections": broken_connections_count,
                "total_connections": len(self.connections),
                "stranded_passengers": stranded_passengers,
                "cancelled_passengers": cancelled_pax,
                "total_impacted_passengers": stranded_passengers + cancelled_pax,
                "crew_duty_violations": crew_violations_count,
                "total_economic_cost_inr": total_economic_cost
            },
            "flights": flight_results,
            "connections": evaluated_connections,
            "crews": evaluated_crews,
            "aircraft_chains": dict(aircraft_chains)
        }

    def evaluate_recovery_options(
        self,
        closed_airport: str,
        closure_start: str,
        closure_end: str
    ) -> List[Dict[str, Any]]:
        baseline = self.run_simulation(closed_airport, closure_start, closure_end)
        b_kpis = baseline["kpis"]
        options = []

        # 1. BLR Spare Aircraft (VT-DS17)
        blr_delayed_flights = [
            f for f in baseline["flights"].values()
            if f["origin"] == "BLR" and f["dep_delay"] > 0 and not f.get("is_cancelled")
        ]
        if blr_delayed_flights:
            target = max(blr_delayed_flights, key=lambda x: x["dep_delay"])
            sim_swap_blr = self.run_simulation(
                closed_airport, closure_start, closure_end,
                spare_swaps={target["flight_id"]: "VT-DS17"}
            )
            s_kpis = sim_swap_blr["kpis"]
            options.append({
                "id": "SWAP_SPARE_BLR",
                "type": "SPARE_SWAP",
                "title": f"Deploy Spare VT-DS17 at BLR for {target['flight_id']}",
                "description": f"Substitute spare aircraft VT-DS17 stationed at Kempegowda (BLR) for flight {target['flight_id']} ({target['origin']}➔{target['destination']}), absorbing rotation delay and resetting downstream legs.",
                "target_flight": target["flight_id"],
                "target_tail": "VT-DS17",
                "swap_dict": {target["flight_id"]: "VT-DS17"},
                "cancel_list": [],
                "delta": {
                    "delay_minutes_saved": b_kpis["total_delay_minutes"] - s_kpis["total_delay_minutes"],
                    "stranded_pax_saved": b_kpis["stranded_passengers"] - s_kpis["stranded_passengers"],
                    "crew_violations_saved": b_kpis["crew_duty_violations"] - s_kpis["crew_duty_violations"],
                    "cost_saved_inr": b_kpis["total_economic_cost_inr"] - s_kpis["total_economic_cost_inr"]
                },
                "result_kpis": s_kpis
            })

        # 2. DEL Spare Aircraft (VT-DS18)
        del_delayed_flights = [
            f for f in baseline["flights"].values()
            if f["origin"] == "DEL" and f["dep_delay"] > 0 and not f.get("is_cancelled")
        ]
        if del_delayed_flights:
            target = max(del_delayed_flights, key=lambda x: x["dep_delay"])
            sim_swap_del = self.run_simulation(
                closed_airport, closure_start, closure_end,
                spare_swaps={target["flight_id"]: "VT-DS18"}
            )
            s_kpis = sim_swap_del["kpis"]
            options.append({
                "id": "SWAP_SPARE_DEL",
                "type": "SPARE_SWAP",
                "title": f"Deploy Spare VT-DS18 at DEL for {target['flight_id']}",
                "description": f"Substitute spare aircraft VT-DS18 stationed at Indira Gandhi (DEL) for flight {target['flight_id']} ({target['origin']}➔{target['destination']}), instantly resetting downstream punctuality and preventing crew timeout.",
                "target_flight": target["flight_id"],
                "target_tail": "VT-DS18",
                "swap_dict": {target["flight_id"]: "VT-DS18"},
                "cancel_list": [],
                "delta": {
                    "delay_minutes_saved": b_kpis["total_delay_minutes"] - s_kpis["total_delay_minutes"],
                    "stranded_pax_saved": b_kpis["stranded_passengers"] - s_kpis["stranded_passengers"],
                    "crew_violations_saved": b_kpis["crew_duty_violations"] - s_kpis["crew_duty_violations"],
                    "cost_saved_inr": b_kpis["total_economic_cost_inr"] - s_kpis["total_economic_cost_inr"]
                },
                "result_kpis": s_kpis
            })

        # 3. Round-Trip Out-and-Back Cancellation Pairs
        # Find tails with out-and-back pairs touching closed airport
        for tail, flist in self.flights_by_tail.items():
            for i in range(len(flist) - 1):
                f1 = flist[i]
                f2 = flist[i+1]
                # Is it an out-and-back round trip? e.g. BOM->PNQ and PNQ->BOM
                if f1["origin"] == f2["destination"] and f1["destination"] == f2["origin"]:
                    # If this pair touches closed airport and was delayed
                    f1_res = baseline["flights"].get(f1["flight_id"], {})
                    f2_res = baseline["flights"].get(f2["flight_id"], {})
                    if (f1["origin"] == closed_airport or f1["destination"] == closed_airport) and (f1_res.get("dep_delay", 0) > 0 or f2_res.get("dep_delay", 0) > 0):
                        pair_ids = [f1["flight_id"], f2["flight_id"]]
                        sim_pair = self.run_simulation(
                            closed_airport, closure_start, closure_end,
                            cancelled_flight_ids=pair_ids
                        )
                        p_kpis = sim_pair["kpis"]
                        options.append({
                            "id": f"CANCEL_PAIR_{f1['flight_id']}_{f2['flight_id']}",
                            "type": "CANCELLATION",
                            "title": f"Cancel Round-Trip Pair: {f1['flight_id']} & {f2['flight_id']} ({f1['origin']}<->{f1['destination']})",
                            "description": f"Proactively cancel round-trip turn {f1['flight_id']}/{f2['flight_id']} to keep aircraft {tail} at {f1['origin']}, completely eliminating downstream delays on subsequent legs.",
                            "target_flight": f"{f1['flight_id']}, {f2['flight_id']}",
                            "target_tail": tail,
                            "swap_dict": {},
                            "cancel_list": pair_ids,
                            "delta": {
                                "delay_minutes_saved": b_kpis["total_delay_minutes"] - p_kpis["total_delay_minutes"],
                                "stranded_pax_saved": b_kpis["stranded_passengers"] - p_kpis["stranded_passengers"],
                                "crew_violations_saved": b_kpis["crew_duty_violations"] - p_kpis["crew_duty_violations"],
                                "cost_saved_inr": b_kpis["total_economic_cost_inr"] - p_kpis["total_economic_cost_inr"]
                            },
                            "result_kpis": p_kpis
                        })

        # 4. Combined Multi-Hub Fleet Recovery
        combined_swaps = {}
        if blr_delayed_flights:
            target_blr = max(blr_delayed_flights, key=lambda x: x["dep_delay"])
            combined_swaps[target_blr["flight_id"]] = "VT-DS17"
        if del_delayed_flights:
            target_del = max(del_delayed_flights, key=lambda x: x["dep_delay"])
            combined_swaps[target_del["flight_id"]] = "VT-DS18"

        if combined_swaps:
            sim_comb = self.run_simulation(
                closed_airport, closure_start, closure_end,
                spare_swaps=combined_swaps
            )
            comb_kpis = sim_comb["kpis"]
            options.append({
                "id": "COMBINED_MASTER_DISPATCH",
                "type": "OPTIMAL_MULTI_ACTION",
                "title": "Optimal Multi-Hub Fleet Recovery Plan",
                "description": "Simultaneously deploy available spare aircraft at both BLR and DEL hubs to insulate the national network and prevent cross-regional cascade.",
                "target_flight": ", ".join(combined_swaps.keys()),
                "target_tail": "VT-DS17 & VT-DS18",
                "swap_dict": combined_swaps,
                "cancel_list": [],
                "delta": {
                    "delay_minutes_saved": b_kpis["total_delay_minutes"] - comb_kpis["total_delay_minutes"],
                    "stranded_pax_saved": b_kpis["stranded_passengers"] - comb_kpis["stranded_passengers"],
                    "crew_violations_saved": b_kpis["crew_duty_violations"] - comb_kpis["crew_duty_violations"],
                    "cost_saved_inr": b_kpis["total_economic_cost_inr"] - comb_kpis["total_economic_cost_inr"]
                },
                "result_kpis": comb_kpis
            })

        options.sort(key=lambda x: x["delta"]["cost_saved_inr"], reverse=True)
        return options
