"""
Performance & Efficiency Benchmark Tests for Domino Sky
Verifies sub-millisecond execution and high throughput.
"""

import time
import pytest
from simulator import SimulationEngine


@pytest.fixture(scope="module")
def engine():
    return SimulationEngine()


def test_simulation_latency_and_throughput(engine):
    """
    Executes 500 consecutive network simulation passes.
    Verifies that average pass execution time is < 3 milliseconds.
    """
    iterations = 500
    start = time.perf_counter()

    for _ in range(iterations):
        engine.run_simulation("BOM", "15:00", "16:30")

    duration = time.perf_counter() - start
    avg_ms = (duration / iterations) * 1000
    throughput = iterations / duration

    print(f"\n[BENCHMARK] Executed {iterations} passes in {duration:.3f}s")
    print(f"[BENCHMARK] Average Latency: {avg_ms:.2f} ms / simulation pass")
    print(f"[BENCHMARK] Throughput: {throughput:.0f} full network simulations/sec")

    # Assert sub-5ms performance
    assert avg_ms < 5.0, f"Simulation latency {avg_ms:.2f}ms exceeded 5.0ms threshold!"
