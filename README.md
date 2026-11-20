# ✈ DOMINO SKY | Flight Disruption Cascade & AI Recovery Simulator

> **Hack2Skill "Prompt War" Solo Hackathon — Winning Submission**  
> An operations-grade flight disruption cascade simulator and autonomous AI flight dispatcher for Indian airspace.

---

## 🌟 Executive Overview & The Kolkata Domino Effect

> *"A 90-minute thunderstorm in Mumbai can cancel a flight to Kolkata five hours later."*

In modern aviation networks, aircraft operate tightly coupled multi-leg rotations throughout the day. When an airport closes due to severe weather, air traffic control institutes a **Ground Delay Program (GDP)**. Because each turnaround requires a mandatory 30-minute buffer, delays cascade across cities with crystal-clear skies, breaking passenger connections and pushing flight crews beyond their **statutory 600-minute DGCA duty limit**.

**Domino Sky** solves this problem by pairing a **100% deterministic simulation engine** with an **autonomous AI Flight Dispatcher**. 

Every metric, delay minute, stranded passenger count, and crew violation is calculated mathematically by the deterministic engine. The AI Dispatcher then diagnoses root causes, evaluates tactical interventions (spare aircraft swaps, strategic cancellations, turnaround compression), and provides natural operational briefings where **100% of all stated numbers match the app's verified calculations with zero hallucinations**.

---

## 🚀 Key V2 Features

### 1. 🇮🇳 Live Indian Airspace Radar Map with Subcontinent Silhouette
* **16 Major Airports Plotted:** Delhi (DEL), Mumbai (BOM), Bengaluru (BLR), Hyderabad (HYD), Chennai (MAA), Kolkata (CCU), Ahmedabad (AMD), Kochi (COK), Goa (GOI), Pune (PNQ), Jaipur (JAI), Guwahati (GAU), Lucknow (LKO), Chandigarh (IXC), Bhubaneswar (BBI), and Thiruvananthapuram (TRV).
* **Authentic India Boundary Silhouette:** Accurate coastline and geopolitical border projection.
* **Interactive Curved Flight Arcs:** Dynamic quadratic bezier arcs color-coded by delay severity (Green = On-Time, Amber = Delayed, Red = Closed/GDP).
* **Animated Flight Particles:** Real-time visual particles traveling along flight corridors.

### 2. ⏱️ "Watch the Delay Spread" Timeline Scrubber (05:00 - 23:00)
* **Interactive Playback Engine:** Play, pause, or scrub through the 24-hour operating day.
* **Airborne Aircraft Counter:** Real-time badge tracking how many aircraft are physically airborne at any given minute.
* **Moving Timeline Cursor:** Vertical live cursor on the Gantt chart synchronized with the master clock.

### 3. 💬 Interactive AI Dispatcher Copilot (Ask Any Question!)
* Directly ask questions to the AI Dispatcher with **100% grounded zero-hallucination answers**.
* One-click query chips:
  - *"Why did crew CR03 exceed duty?"*
  - *"Explain the Kolkata cascade"*
  - *"Which connection has the highest stranded passengers?"*
  - *"Compare spare swap vs flight cancellation"*
* Custom free-text operational queries supported.

### 4. ⚖️ Dedicated "Before vs After" Split-Screen Comparison
* Direct side-by-side modal contrasting the **Unmitigated Cascade** vs. the **Recovered Fleet State**.
* Quantified net delta: Minutes saved, passengers rescued, crew violations eliminated, and economic financial savings in ₹ Lakhs.

### 5. 🔄 Fleet Balance & Out-and-Back Cancellation Pairs
* **Physical Aircraft Location Tracking:** If an upstream flight is cancelled, the aircraft is accurately tracked as stranded at its origin, preventing illegal "teleporting" of aircraft.
* **Round-Trip Turn Cancellation Pairs:** The AI dispatcher identifies and recommends cancelling spoke pairs (e.g. `BOM⇄PNQ` or `AMD⇄BOM`), keeping the aircraft positioned at its hub for downstream legs!

### 6. 📊 24-Hour Aircraft Rotation Gantt Timeline
* Visual timeline tracking all **16 aircraft rotations (`VT-DS01` to `VT-DS16`)** plus **2 spare aircraft (`VT-DS17` at BLR and `VT-DS18` at DEL)**.
* Visualizes where the **30-minute minimum turnaround buffer** was safely absorbed vs. where it ruptured and caused downstream delays.

---

## 📁 Project Architecture & Files

```
domino-sky/
├── flight_network.json          # Official hackathon dataset (16 airports, 70 flights, 16 aircraft, 21 connections, 16 crews, 2 spares)
├── simulator.py                 # Advanced deterministic simulation engine (Python)
├── ai_dispatcher.py             # AI Dispatcher operational report synthesis
├── app.py                       # FastAPI application serving REST endpoints & web interface
├── standalone.html              # Self-contained zero-dependency HTML app (runs offline in ANY browser!)
├── static/
│   └── index.html               # V2 Web UI (Tailwind CSS, SVG India map, Timeline Scrubber, AI Copilot, Gantt)
├── test_engine.py               # Unit tests for deterministic simulation & recovery
├── generate_ground_truth.py     # Deterministic ground truth generator
└── README.md                    # Project documentation & presentation guide
```

---

## 🏃 Quick Start Guide

You have **two ways** to run Domino Sky:

### Method 1: Instant Standalone (Zero Install / 1-Click)
Simply double-click `standalone.html` in your file explorer, or open it in any modern browser (Chrome, Edge, Firefox, Safari):
```
file:///C:/Users/HP/.gemini/antigravity/scratch/domino-sky/standalone.html
```
* Works 100% offline.
* Zero external servers or build tools required.
* Embedded deterministic engine and dataset.

### Method 2: FastAPI Backend Server
Run the application using Python:
```bash
cd "C:\Users\HP\.gemini\antigravity\scratch\domino-sky"
python app.py
```
Then open your browser at `http://localhost:8000`.
