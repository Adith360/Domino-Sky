import subprocess
import time
import urllib.request
import sys

# Start uvicorn server in background process
proc = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", "8000"
], cwd=r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky")

try:
    print("Waiting for server to spin up...")
    time.sleep(3)
    resp = urllib.request.urlopen("http://127.0.0.1:8000/")
    content = resp.read().decode('utf-8')
    print(f"Server replied! Status: {resp.status}, HTML size: {len(content)} bytes")
    assert "DOMINO SKY" in content
    
    # Test simulate endpoint via HTTP
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/simulate",
        data=b'{"closed_airport": "BOM", "closure_start": "15:00", "closure_end": "16:30"}',
        headers={"Content-Type": "application/json"}
    )
    resp_sim = urllib.request.urlopen(req)
    print("API /api/simulate replied! Status:", resp_sim.status)
    print("ALL SERVER TESTS PASSED PERFECTLY!")
finally:
    proc.terminate()
    proc.wait()
    print("Server cleanly stopped.")
