from simulator import SimulationEngine

engine = SimulationEngine()
print("=== Simulating 90-min thunderstorm in Mumbai 15:00-16:30 ===")
res = engine.run_simulation("BOM", "15:00", "16:30")
k = res["kpis"]
print(f"Delayed flights: {k['delayed_flights']}")
print(f"Total delay mins: {k['total_delay_minutes']}")
print(f"Broken connections: {k['broken_connections']}")
print(f"Stranded pax: {k['stranded_passengers']}")
print(f"Crew duty violations: {k['crew_duty_violations']}")

print("\nWhat happened to VT-DS03 and DS0304 (to Kolkata CCU)?")
for fid in ["DS0301", "DS0302", "DS0303", "DS0304"]:
    f = res["flights"][fid]
    print(f"  {fid} ({f['origin']}->{f['destination']}): sched {f['sched_dep']}-{f['sched_arr']}, actual {f['actual_dep']}-{f['actual_arr']}, delay +{f['dep_delay']}m, reasons: {f['reasons']}")

print("\nCrew CR03 status:")
for c in res["crews"]:
    if c["crew_id"] == "CR03":
        print(f"  CR03: duty {c['actual_duty_mins']}m / {c['max_duty_mins']}m, status: {c['status']}, overage: +{c['overage_mins']}m")

print("\nRecovery options for Mumbai afternoon storm:")
options = engine.evaluate_recovery_options("BOM", "15:00", "16:30")
for i, opt in enumerate(options):
    print(f"  [{i+1}] {opt['title']}")
    print(f"      Delta: {opt['delta']}")
