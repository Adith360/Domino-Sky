import json

# Load dataset and India path
with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\flight_network.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

with open(r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\india_path.txt", "r", encoding="utf-8") as f:
    india_path_d = f.read().strip()

dataset_json = json.dumps(dataset)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Domino Sky | Flight Disruption Cascade & Recovery Simulator</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #060910;
      color: #e2e8f0;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0b1120;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }
    @keyframes pulse-ring {
      0% { transform: scale(0.9); opacity: 0.8; }
      50% { transform: scale(1.6); opacity: 0; }
      100% { transform: scale(0.9); opacity: 0; }
    }
    .pulse-ring-red {
      animation: pulse-ring 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
    }
    .glow-cyan {
      box-shadow: 0 0 15px rgba(56, 189, 248, 0.25);
    }
    .glow-emerald {
      box-shadow: 0 0 15px rgba(16, 185, 129, 0.25);
    }
    .time-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #38bdf8;
      cursor: pointer;
      box-shadow: 0 0 10px #38bdf8;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased">

  <!-- TOP APP BAR -->
  <header class="border-b border-slate-800 bg-[#090e1a]/95 backdrop-blur sticky top-0 z-50 px-4 lg:px-6 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-md">
    <div class="flex items-center space-x-3">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-sky-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-sky-500/20 text-white font-bold text-lg cursor-pointer" onclick="resetSimulation()">
        ✈
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-base font-bold tracking-tight text-white flex items-center gap-1.5">
            DOMINO SKY
            <span class="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-400 border border-sky-500/20 font-bold">AOC DISPATCHER</span>
          </h1>
          <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse mr-1"></span>
            100% Deterministic Engine
          </span>
        </div>
        <p class="text-xs text-slate-400">Flight Disruption Cascade & AI Recovery Simulator • 16 Airports • 70 Flights • 16 Aircraft • 2 Spares</p>
      </div>
    </div>

    <!-- PRESET DISRUPTION BUTTONS -->
    <div class="flex items-center flex-wrap gap-1.5">
      <span class="text-[11px] font-medium uppercase tracking-wider text-slate-500 mr-1 hidden sm:inline">Disruption Scenarios:</span>
      <button onclick="applyPreset('BOM_AFTERNOON')" class="text-xs font-mono px-2.5 py-1 rounded bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 transition flex items-center gap-1 shadow-sm" title="The Hackathon Prompt's Kolkata Cascade Story: BOM storm cascades to cancel Kolkata flight!">
        ⚡ BOM Storm (15:00)
      </button>
      <button onclick="applyPreset('BOM_MONSOON')" class="text-xs font-mono px-2.5 py-1 rounded bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 border border-rose-500/30 transition flex items-center gap-1 shadow-sm" title="16 flights delayed, 199 stranded passengers">
        ⛈️ BOM Flood (07:30)
      </button>
      <button onclick="applyPreset('DEL_FOG')" class="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 border border-slate-700 transition flex items-center gap-1 shadow-sm">
        🌫️ DEL Fog (08:00)
      </button>
      <button onclick="applyPreset('CCU_CYCLONE')" class="text-xs font-mono px-2.5 py-1 rounded bg-purple-500/10 hover:bg-purple-500/20 text-purple-300 border border-purple-500/30 transition flex items-center gap-1 shadow-sm" title="9 flights delayed, 2 crew violations!">
        🌀 CCU Alert (12:00)
      </button>
      <button onclick="applyPreset('BLR_HALT')" class="text-xs font-mono px-2.5 py-1 rounded bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 transition flex items-center gap-1 shadow-sm">
        🛡️ BLR Halt (09:00)
      </button>
      <button onclick="openBeforeAfterModal()" class="text-xs font-medium px-2.5 py-1 rounded bg-sky-950/80 hover:bg-sky-900 text-sky-300 border border-sky-600/50 transition flex items-center gap-1">
        ⚖️ Before vs After
      </button>
      <button onclick="resetSimulation()" class="text-xs font-medium px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition">
        ↺ Reset
      </button>
      <button onclick="exportSITREP()" class="text-xs font-medium px-2.5 py-1 rounded bg-sky-900/40 hover:bg-sky-800/60 text-sky-300 border border-sky-700/50 transition">
        📥 SITREP
      </button>
    </div>
  </header>

  <!-- TIME SCRUBBER: WATCH THE DELAY SPREAD IN REAL TIME -->
  <section class="bg-[#0c1220] border-b border-slate-800 px-4 lg:px-6 py-2.5 flex flex-wrap items-center justify-between gap-3">
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-1 bg-[#131b2e] px-2 py-1 rounded-lg border border-slate-700">
        <button id="play-pause-btn" onclick="togglePlayback()" class="w-7 h-7 rounded bg-sky-600 hover:bg-sky-500 text-white flex items-center justify-center font-bold text-xs transition">
          ▶
        </button>
        <button onclick="stepTime(-15)" class="w-7 h-7 rounded hover:bg-slate-800 text-slate-300 flex items-center justify-center font-mono text-xs transition" title="Step -15m">
          -15m
        </button>
        <button onclick="stepTime(15)" class="w-7 h-7 rounded hover:bg-slate-800 text-slate-300 flex items-center justify-center font-mono text-xs transition" title="Step +15m">
          +15m
        </button>
      </div>

      <div class="flex items-center gap-2">
        <span class="text-xs text-slate-400 font-medium">SIMULATION TIME:</span>
        <span id="current-clock-display" class="text-sm font-bold font-mono px-2.5 py-0.5 rounded bg-sky-950 text-sky-400 border border-sky-600/40">
          12:00 IST
        </span>
      </div>

      <div class="flex items-center gap-2 text-xs font-mono text-slate-400 border-l border-slate-800 pl-3">
        <span>Airborne Flights:</span>
        <span id="airborne-count-badge" class="font-bold text-white bg-slate-800 px-2 py-0.5 rounded">0 in air</span>
      </div>
    </div>

    <!-- Time Slider -->
    <div class="flex-1 max-w-xl mx-4 flex items-center gap-3">
      <span class="text-[10px] font-mono text-slate-500">05:00</span>
      <input id="time-scrubber" type="range" min="300" max="1380" step="5" value="720" oninput="handleTimeScrub(this.value)" class="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer time-slider" />
      <span class="text-[10px] font-mono text-slate-500">23:00</span>
    </div>

    <!-- Speed Selector -->
    <div class="flex items-center gap-1.5 text-xs font-mono text-slate-400">
      <span>Speed:</span>
      <button onclick="setPlaySpeed(1)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200">1x</button>
      <button onclick="setPlaySpeed(2)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200">2x</button>
      <button onclick="setPlaySpeed(5)" class="px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200">5x</button>
    </div>
  </section>

  <!-- MAIN DASHBOARD CONTENT -->
  <main class="flex-1 max-w-[1700px] w-full mx-auto p-3 lg:p-5 flex flex-col gap-4">

    <!-- KPI STATS SUMMARY CARDS -->
    <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
      <div class="bg-[#0c1220] border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between shadow">
        <span class="text-xs text-slate-400 font-medium">Scheduled Flights</span>
        <div class="flex items-baseline justify-between mt-1">
          <span id="kpi-total-flights" class="text-2xl font-bold font-mono text-white">70</span>
          <span class="text-[11px] text-emerald-400 font-mono" id="kpi-ontime-flights">70 on-time</span>
        </div>
        <div class="w-full bg-slate-800 h-1.5 rounded-full mt-2 overflow-hidden">
          <div id="kpi-ontime-bar" class="bg-emerald-500 h-full rounded-full transition-all duration-500" style="width: 100%"></div>
        </div>
      </div>

      <div class="bg-[#0c1220] border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between shadow">
        <span class="text-xs text-slate-400 font-medium">Delayed Flights</span>
        <div class="flex items-baseline justify-between mt-1">
          <span id="kpi-delayed-flights" class="text-2xl font-bold font-mono text-white">0</span>
          <span id="kpi-delayed-pct" class="text-[11px] font-mono text-slate-400">0% network</span>
        </div>
        <span id="kpi-severe-count" class="text-[11px] text-rose-400 font-mono mt-1">0 severely delayed</span>
      </div>

      <div class="bg-[#0c1220] border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between shadow">
        <span class="text-xs text-slate-400 font-medium">Total Delay Time</span>
        <div class="flex items-baseline justify-between mt-1">
          <span id="kpi-delay-minutes" class="text-2xl font-bold font-mono text-amber-400">0m</span>
          <span id="kpi-delay-hours" class="text-[11px] font-mono text-slate-400">0.0 hrs</span>
        </div>
        <span id="kpi-avg-delay" class="text-[11px] text-slate-400 font-mono mt-1">Avg 0m / delayed flight</span>
      </div>

      <div class="bg-[#0c1220] border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between shadow">
        <span class="text-xs text-slate-400 font-medium">Stranded Passengers</span>
        <div class="flex items-baseline justify-between mt-1">
          <span id="kpi-stranded-pax" class="text-2xl font-bold font-mono text-rose-400">0</span>
          <span id="kpi-broken-cx" class="text-[11px] font-mono text-rose-300">0 broken CX</span>
        </div>
        <span class="text-[11px] text-slate-400 mt-1">Out of 21 connections</span>
      </div>

      <div class="bg-[#0c1220] border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between shadow">
        <span class="text-xs text-slate-400 font-medium">Crew Violations</span>
        <div class="flex items-baseline justify-between mt-1">
          <span id="kpi-crew-violations" class="text-2xl font-bold font-mono text-white">0</span>
          <span class="text-[11px] font-mono text-slate-400">DGCA 600m</span>
        </div>
        <span id="kpi-crew-status" class="text-[11px] text-emerald-400 font-mono mt-1">100% Legal</span>
      </div>

      <div class="bg-[#0c1220] border border-slate-800/80 rounded-xl p-3 flex flex-col justify-between shadow">
        <span class="text-xs text-slate-400 font-medium">Est. Financial Cost</span>
        <div class="flex items-baseline justify-between mt-1">
          <span id="kpi-cost" class="text-2xl font-bold font-mono text-white">₹0</span>
          <span class="text-[11px] font-mono text-slate-400">INR</span>
        </div>
        <span class="text-[11px] text-slate-400 mt-1">Pax comp & delay penalties</span>
      </div>
    </div>

    <!-- WORKSPACE SPLIT: LEFT CONTROLS & MAP | RIGHT AI DISPATCHER & GANTT -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-4">

      <!-- LEFT COLUMN: CONTROLS & INTERACTIVE MAP (7 cols) -->
      <div class="lg:col-span-7 flex flex-col gap-4">
        
        <!-- DISRUPTION CONFIGURATION BAR -->
        <div class="bg-[#0c1220] border border-slate-800 rounded-xl p-4 flex flex-col gap-3 shadow">
          <div class="flex items-center justify-between">
            <h2 class="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              Airport Disruption & Ground Delay Program (GDP) Trigger
            </h2>
            <span id="active-disruption-badge" class="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
              Network Normal
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">Target Airport</label>
              <select id="input-airport" class="w-full bg-[#131b2e] border border-slate-700 rounded-lg px-3 py-1.5 text-sm font-mono text-slate-200 focus:outline-none focus:border-sky-500">
                <option value="BOM">BOM - Mumbai (CSMIA)</option>
                <option value="DEL">DEL - Delhi (IGIA)</option>
                <option value="BLR">BLR - Bengaluru (KIA)</option>
                <option value="HYD">HYD - Hyderabad (RGIA)</option>
                <option value="MAA">MAA - Chennai</option>
                <option value="CCU">CCU - Kolkata (NSCBIA)</option>
                <option value="AMD">AMD - Ahmedabad</option>
                <option value="COK">COK - Kochi</option>
                <option value="GOI">GOI - Goa</option>
                <option value="PNQ">PNQ - Pune</option>
                <option value="JAI">JAI - Jaipur</option>
                <option value="GAU">GAU - Guwahati</option>
                <option value="LKO">LKO - Lucknow</option>
                <option value="IXC">IXC - Chandigarh</option>
                <option value="BBI">BBI - Bhubaneswar</option>
                <option value="TRV">TRV - Thiruvananthapuram</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">Closure Start (IST)</label>
              <input id="input-start-time" type="time" value="15:00" class="w-full bg-[#131b2e] border border-slate-700 rounded-lg px-3 py-1.5 text-sm font-mono text-slate-200 focus:outline-none focus:border-sky-500" />
            </div>

            <div>
              <label class="block text-xs font-medium text-slate-400 mb-1">Closure End (IST)</label>
              <input id="input-end-time" type="time" value="16:30" class="w-full bg-[#131b2e] border border-slate-700 rounded-lg px-3 py-1.5 text-sm font-mono text-slate-200 focus:outline-none focus:border-sky-500" />
            </div>

            <button onclick="handleTriggerDisruption()" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-medium text-sm px-4 py-2 rounded-lg transition shadow-lg shadow-rose-600/20 flex items-center justify-center gap-1.5">
              <span>⚠️ Simulate Cascade</span>
            </button>
          </div>
        </div>

        <!-- INTERACTIVE INDIA FLIGHT MAP -->
        <div class="bg-[#0c1220] border border-slate-800 rounded-xl p-4 flex flex-col relative overflow-hidden shadow">
          <div class="flex items-center justify-between mb-2 z-10">
            <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <span>🇮🇳 Indian Airspace Live Telemetry</span>
            </h3>
            <div class="flex items-center gap-3 text-[11px] font-mono text-slate-400">
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-sky-400"></span> Normal</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-amber-400"></span> Delayed</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-rose-500"></span> Closed / GDP</span>
              <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-cyan-400"></span> Spare Hub</span>
            </div>
          </div>

          <div class="w-full h-[520px] bg-[#070b14] rounded-lg border border-slate-800/60 relative flex items-center justify-center">
            <svg id="network-map" class="w-full h-full" viewBox="0 0 900 950" preserveAspectRatio="xMidYMid meet">
              <defs>
                <radialGradient id="hub-glow-normal" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
                  <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>
                </radialGradient>
                <radialGradient id="hub-glow-closed" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#f43f5e" stop-opacity="0.9"/>
                  <stop offset="100%" stop-color="#f43f5e" stop-opacity="0"/>
                </radialGradient>
                <radialGradient id="hub-glow-spare" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.8"/>
                  <stop offset="100%" stop-color="#06b6d4" stop-opacity="0"/>
                </radialGradient>
              </defs>

              <g id="map-grid" opacity="0.15"></g>
              <!-- India Coastline / Border Silhouette -->
              <path id="india-boundary" d="__INDIA_PATH__" fill="#0d1424" fill-opacity="0.4" stroke="#1e2c48" stroke-width="1.5" />
              <g id="routes-layer"></g>
              <g id="particles-layer"></g>
              <g id="airports-layer"></g>
            </svg>

            <div id="map-tooltip" class="absolute pointer-events-none hidden bg-[#0f172a]/95 border border-slate-700 text-xs text-slate-200 p-2.5 rounded-lg shadow-xl z-30 font-mono min-w-[180px]"></div>
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN: AI DISPATCHER & TACTICAL RECOVERY (5 cols) -->
      <div class="lg:col-span-5 flex flex-col gap-4">
        
        <!-- AI DISPATCHER CONSOLE -->
        <div class="bg-[#0c1220] border border-slate-800 rounded-xl p-4 flex flex-col gap-3 shadow">
          <div class="flex items-center justify-between border-b border-slate-800 pb-3">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded-md bg-sky-500/10 text-sky-400 flex items-center justify-center font-bold text-xs border border-sky-500/20">
                AI
              </div>
              <h2 class="text-sm font-semibold text-slate-200">
                AI Flight Operations Dispatcher
              </h2>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
              Deterministic Grounded
            </span>
          </div>

          <div id="ai-briefing-box" class="bg-[#070b14] border border-slate-800/80 rounded-lg p-3 text-xs text-slate-300 leading-relaxed font-sans max-h-48 overflow-y-auto space-y-2">
            <p class="text-slate-400 italic">Select an airport closure scenario above to simulate the cascade and unlock AI recovery actions.</p>
          </div>

          <!-- INTERACTIVE AI COPILOT QUERY INPUT -->
          <div class="bg-[#070a13] border border-slate-800 rounded-lg p-2.5 flex flex-col gap-2">
            <div class="flex items-center justify-between text-[11px] font-medium text-slate-400">
              <span>Ask AI Dispatcher:</span>
              <span class="text-[10px] text-sky-400">Grounded Copilot</span>
            </div>
            <div class="flex flex-wrap gap-1">
              <button onclick="askCopilot('Why did crew CR03 exceed duty?')" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 transition">
                CR03 Timeout?
              </button>
              <button onclick="askCopilot('Explain the Kolkata cascade')" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 transition">
                Kolkata Cascade?
              </button>
              <button onclick="askCopilot('Which connection has the highest stranded passengers?')" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 transition">
                Top Stranded CX?
              </button>
              <button onclick="askCopilot('Compare spare swap vs flight cancellation')" class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-sky-300 transition">
                Swap vs Cancel?
              </button>
            </div>
            <div class="flex gap-1.5 mt-1">
              <input id="copilot-input" placeholder="Type custom operational question..." onkeydown="if(event.key==='Enter') sendCustomCopilotQuery()" class="flex-1 bg-[#101726] border border-slate-700 rounded px-2.5 py-1 text-xs font-mono text-slate-200 focus:outline-none focus:border-sky-500" />
              <button onclick="sendCustomCopilotQuery()" class="px-3 py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-medium transition">
                Ask
              </button>
            </div>
            <div id="copilot-answer-box" class="hidden p-2 rounded bg-slate-900 border border-slate-700 text-[11px] text-slate-200 leading-relaxed font-sans max-h-32 overflow-y-auto"></div>
          </div>

          <!-- RECOVERY ACTIONS CONTAINER -->
          <div class="flex flex-col gap-2 mt-1">
            <div class="flex items-center justify-between">
              <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400">
                Recommended Recovery Actions
              </h3>
              <span id="recovery-options-count" class="text-[11px] font-mono text-slate-500">0 options</span>
            </div>

            <div id="recovery-cards-container" class="flex flex-col gap-2.5 max-h-[340px] overflow-y-auto pr-1">
              <div class="p-4 border border-dashed border-slate-800 rounded-lg text-center text-xs text-slate-500">
                No active disruption. All flights operating smoothly.
              </div>
            </div>
          </div>
        </div>

        <!-- RECOVERY COMPARISON / DIFF BANNER -->
        <div id="recovery-diff-banner" class="hidden bg-gradient-to-r from-emerald-950/40 via-sky-950/30 to-indigo-950/40 border border-emerald-500/30 rounded-xl p-4 flex flex-col gap-2 shadow">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-emerald-400 flex items-center gap-1.5 uppercase tracking-wider">
              <span>✓</span> Recovery Plan Applied
            </span>
            <div class="flex items-center gap-2">
              <button onclick="openBeforeAfterModal()" class="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30 transition">
                View Full Diff
              </button>
              <button onclick="revertRecovery()" class="text-[11px] font-mono text-slate-400 hover:text-white underline">
                Revert
              </button>
            </div>
          </div>
          <div class="grid grid-cols-4 gap-2 text-center mt-1">
            <div class="bg-black/30 p-2 rounded border border-emerald-500/20">
              <span class="block text-[10px] text-slate-400 font-mono">Delay Saved</span>
              <span id="diff-delay" class="text-sm font-bold font-mono text-emerald-400">-0m</span>
            </div>
            <div class="bg-black/30 p-2 rounded border border-emerald-500/20">
              <span class="block text-[10px] text-slate-400 font-mono">Pax Saved</span>
              <span id="diff-pax" class="text-sm font-bold font-mono text-emerald-400">+0</span>
            </div>
            <div class="bg-black/30 p-2 rounded border border-emerald-500/20">
              <span class="block text-[10px] text-slate-400 font-mono">Crews Saved</span>
              <span id="diff-crews" class="text-sm font-bold font-mono text-emerald-400">0</span>
            </div>
            <div class="bg-black/30 p-2 rounded border border-emerald-500/20">
              <span class="block text-[10px] text-slate-400 font-mono">Cost Saved</span>
              <span id="diff-cost" class="text-sm font-bold font-mono text-emerald-400">₹0</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- AIRCRAFT ROTATION GANTT CHART (FULL WIDTH) -->
    <div class="bg-[#0c1220] border border-slate-800 rounded-xl p-4 flex flex-col gap-3 shadow">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 class="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <span>📊</span>
            Aircraft Rotation Gantt Timeline (16 Tails + 2 Spares)
          </h2>
          <p class="text-xs text-slate-400">Visualizing 30-minute turnaround propagation and delay absorption across 24 hours.</p>
        </div>
        <div class="flex items-center gap-3 text-[11px] font-mono text-slate-400">
          <span class="flex items-center gap-1"><span class="w-3 h-2 rounded bg-emerald-500"></span> On Time</span>
          <span class="flex items-center gap-1"><span class="w-3 h-2 rounded bg-amber-500"></span> Delayed (&lt;60m)</span>
          <span class="flex items-center gap-1"><span class="w-3 h-2 rounded bg-rose-500"></span> Severe Delay (&gt;60m)</span>
          <span class="flex items-center gap-1"><span class="w-3 h-2 rounded bg-cyan-400"></span> Spare Substituted</span>
          <span class="flex items-center gap-1"><span class="w-3 h-2 rounded bg-slate-600"></span> Cancelled</span>
        </div>
      </div>

      <div class="overflow-x-auto border border-slate-800/80 rounded-lg bg-[#070a13] p-2 relative">
        <div class="min-w-[1100px] flex border-b border-slate-800 pb-1.5 mb-1 text-[10px] font-mono text-slate-400">
          <div class="w-24 shrink-0 font-bold text-slate-300">TAIL / BASE</div>
          <div class="flex-1 grid grid-cols-19 text-center">
            <span>05:00</span><span>06:00</span><span>07:00</span><span>08:00</span>
            <span>09:00</span><span>10:00</span><span>11:00</span><span>12:00</span>
            <span>13:00</span><span>14:00</span><span>15:00</span><span>16:00</span>
            <span>17:00</span><span>18:00</span><span>19:00</span><span>20:00</span>
            <span>21:00</span><span>22:00</span><span>23:00</span>
          </div>
        </div>

        <div id="gantt-rows" class="min-w-[1100px] flex flex-col gap-1.5 py-1 relative"></div>

        <!-- Vertical Current Time Line on Gantt -->
        <div id="gantt-time-cursor" class="absolute top-0 bottom-0 w-[2px] bg-sky-400 pointer-events-none z-20 shadow-[0_0_8px_#38bdf8]" style="left: 110px;"></div>
      </div>
    </div>

    <!-- TABS: FLIGHT ROSTER | PASSENGER CONNECTIONS | CREW STATUS -->
    <div class="bg-[#0c1220] border border-slate-800 rounded-xl p-4 flex flex-col gap-3 shadow">
      <div class="flex flex-wrap items-center justify-between border-b border-slate-800 pb-2.5 gap-2">
        <div class="flex items-center gap-2">
          <button id="tab-btn-flights" onclick="switchTab('flights')" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20 transition">
            ✈ Flight Roster (70)
          </button>
          <button id="tab-btn-connections" onclick="switchTab('connections')" class="text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
            🧳 Connections & Stranded Pax (21)
          </button>
          <button id="tab-btn-crews" onclick="switchTab('crews')" class="text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition">
            👨‍✈️ Crew Duty Hours (16)
          </button>
        </div>

        <div class="flex items-center gap-2">
          <input id="table-search" oninput="renderActiveTab()" placeholder="Filter flights, tails, cities..." class="bg-[#131b2e] border border-slate-700 rounded-lg px-2.5 py-1 text-xs font-mono text-slate-200 focus:outline-none focus:border-sky-500 w-48" />
          <select id="status-filter" onchange="renderActiveTab()" class="bg-[#131b2e] border border-slate-700 rounded-lg px-2 py-1 text-xs font-mono text-slate-200 focus:outline-none">
            <option value="ALL">All Status</option>
            <option value="DELAYED">Delayed Only</option>
            <option value="ON_TIME">On Time Only</option>
            <option value="CANCELLED">Cancelled Only</option>
          </select>
        </div>
      </div>

      <div class="overflow-x-auto max-h-96 overflow-y-auto">
        <table class="w-full text-left text-xs font-mono">
          <thead id="table-head" class="text-slate-400 bg-slate-900/60 sticky top-0 border-b border-slate-800"></thead>
          <tbody id="table-body" class="divide-y divide-slate-800/60"></tbody>
        </table>
      </div>
    </div>

  </main>

  <!-- BEFORE VS AFTER RECOVERY COMPARISON MODAL -->
  <div id="before-after-modal" class="fixed inset-0 bg-black/85 backdrop-blur-md z-50 hidden flex items-center justify-center p-4">
    <div class="bg-[#0f172a] border border-slate-700 rounded-2xl max-w-5xl w-full p-6 flex flex-col gap-4 shadow-2xl max-h-[90vh] overflow-y-auto">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-xl">⚖️</span>
          <div>
            <h3 class="text-base font-bold text-white">Before vs After Recovery Analysis</h3>
            <p class="text-xs text-slate-400">Direct side-by-side comparison of cascade disruption vs tactical AI dispatch intervention.</p>
          </div>
        </div>
        <button onclick="closeBeforeAfterModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- Before Column -->
        <div class="bg-rose-950/20 border border-rose-500/30 rounded-xl p-4 flex flex-col gap-3">
          <div class="flex items-center justify-between border-b border-rose-500/20 pb-2">
            <h4 class="font-bold text-rose-300 text-sm flex items-center gap-1.5">
              <span>⚠️</span> Before Recovery (Cascade Active)
            </h4>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-400 font-bold">Unmitigated</span>
          </div>

          <div class="grid grid-cols-2 gap-2 text-center text-xs font-mono">
            <div class="bg-black/40 p-2.5 rounded border border-rose-500/20">
              <span class="text-slate-400 block text-[10px]">Delayed Flights</span>
              <strong id="modal-before-delayed" class="text-rose-400 text-base">0</strong>
            </div>
            <div class="bg-black/40 p-2.5 rounded border border-rose-500/20">
              <span class="text-slate-400 block text-[10px]">Total Delay Mins</span>
              <strong id="modal-before-delay-mins" class="text-rose-400 text-base">0m</strong>
            </div>
            <div class="bg-black/40 p-2.5 rounded border border-rose-500/20">
              <span class="text-slate-400 block text-[10px]">Stranded Pax</span>
              <strong id="modal-before-pax" class="text-rose-400 text-base">0</strong>
            </div>
            <div class="bg-black/40 p-2.5 rounded border border-rose-500/20">
              <span class="text-slate-400 block text-[10px]">Crew Violations</span>
              <strong id="modal-before-crews" class="text-rose-400 text-base">0</strong>
            </div>
          </div>

          <div id="modal-before-highlights" class="text-xs text-slate-300 space-y-1.5 bg-black/30 p-3 rounded border border-rose-500/20 font-sans"></div>
        </div>

        <!-- After Column -->
        <div class="bg-emerald-950/20 border border-emerald-500/30 rounded-xl p-4 flex flex-col gap-3">
          <div class="flex items-center justify-between border-b border-emerald-500/20 pb-2">
            <h4 class="font-bold text-emerald-300 text-sm flex items-center gap-1.5">
              <span>✓</span> After Recovery (Plan Deployed)
            </h4>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold">Optimized</span>
          </div>

          <div class="grid grid-cols-2 gap-2 text-center text-xs font-mono">
            <div class="bg-black/40 p-2.5 rounded border border-emerald-500/20">
              <span class="text-slate-400 block text-[10px]">Delayed Flights</span>
              <strong id="modal-after-delayed" class="text-emerald-400 text-base">0</strong>
            </div>
            <div class="bg-black/40 p-2.5 rounded border border-emerald-500/20">
              <span class="text-slate-400 block text-[10px]">Total Delay Mins</span>
              <strong id="modal-after-delay-mins" class="text-emerald-400 text-base">0m</strong>
            </div>
            <div class="bg-black/40 p-2.5 rounded border border-emerald-500/20">
              <span class="text-slate-400 block text-[10px]">Stranded Pax</span>
              <strong id="modal-after-pax" class="text-emerald-400 text-base">0</strong>
            </div>
            <div class="bg-black/40 p-2.5 rounded border border-emerald-500/20">
              <span class="text-slate-400 block text-[10px]">Crew Violations</span>
              <strong id="modal-after-crews" class="text-emerald-400 text-base">0</strong>
            </div>
          </div>

          <div id="modal-after-highlights" class="text-xs text-slate-300 space-y-1.5 bg-black/30 p-3 rounded border border-emerald-500/20 font-sans"></div>
        </div>
      </div>

      <!-- Net Improvements Delta Banner -->
      <div class="bg-gradient-to-r from-sky-950/60 to-emerald-950/60 border border-sky-500/40 rounded-xl p-4 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div>
          <span class="text-slate-400 block text-[11px]">NET QUANTIFIED BENEFIT:</span>
          <span id="modal-delta-summary" class="text-sm font-bold text-white">Deploying tactical intervention saves delay & protects passengers.</span>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <span class="text-slate-400 block text-[10px]">Est. Savings</span>
            <span id="modal-delta-cost" class="text-base font-bold text-emerald-400">₹0</span>
          </div>
          <button onclick="closeBeforeAfterModal()" class="px-4 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-medium text-xs transition">
            Close View
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- CASCADE ROOT CAUSE MODAL -->
  <div id="cascade-modal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-[#0f172a] border border-slate-700 rounded-2xl max-w-2xl w-full p-6 flex flex-col gap-4 shadow-2xl">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <span class="text-lg">🔍</span>
          <h3 id="modal-title" class="text-base font-bold text-white">Flight Cascade Lineage</h3>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-white text-lg font-bold">✕</button>
      </div>

      <div id="modal-content" class="flex flex-col gap-3 text-xs text-slate-300"></div>

      <div class="flex justify-end pt-2 border-t border-slate-800">
        <button onclick="closeModal()" class="px-4 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium">Close</button>
      </div>
    </div>
  </div>

  <!-- EMBEDDED DATASET & CLIENT SIMULATION ENGINE -->
  <script>
    const EMBEDDED_DATA = __DATASET_JSON__;

    // State
    let networkBaseline = null;
    let currentSimulation = null;
    let disruptedSimulation = null;
    let activeDisruption = { airport: null, start: null, end: null };
    let activeInterventions = { cancelled_flight_ids: [], spare_swaps: {} };
    let recoveryOptions = [];
    let currentTab = 'flights';
    
    // Playback state
    let simClockMinute = 720; // 12:00 default
    let isPlaying = false;
    let playTimer = null;
    let playSpeed = 1;

    function timeToMin(t) {
      if (!t) return 0;
      const [h, m] = t.split(':').map(Number);
      return h * 60 + m;
    }

    function minToTime(m) {
      const wrapped = ((m % 1440) + 1440) % 1440;
      const h = Math.floor(wrapped / 60);
      const min = wrapped % 60;
      return `${String(h).padStart(2, '0')}:${String(min).padStart(2, '0')}`;
    }

    // DETERMINISTIC SIMULATION ENGINE (CLIENT-SIDE WITH FLEET LOCATION BALANCE)
    function simulateEngine(closedApt, cStartStr, cEndStr, cancelledIds = [], spareSwaps = {}) {
      const cancellations = new Set(cancelledIds);
      const swaps = spareSwaps || {};
      const cStart = cStartStr ? timeToMin(cStartStr) : null;
      const cEnd = cEndStr ? timeToMin(cEndStr) : null;
      const minTurnaround = EMBEDDED_DATA.meta.min_turnaround_minutes || 30;

      const flightsByTail = {};
      EMBEDDED_DATA.flights.forEach(f => {
        if (!flightsByTail[f.tail_id]) flightsByTail[f.tail_id] = [];
        flightsByTail[f.tail_id].push(f);
      });
      Object.keys(flightsByTail).forEach(t => {
        flightsByTail[t].sort((a, b) => a.leg_order - b.leg_order);
      });

      const flightResults = {};
      const aircraftChains = {};

      Object.entries(flightsByTail).forEach(([origTail, flist]) => {
        let prevArrTime = null;
        let currentLocation = flist[0].origin;
        let activeTail = origTail;

        flist.forEach(f => {
          const fid = f.flight_id;
          const schedDep = timeToMin(f.dep);
          const schedArr = timeToMin(f.arr);
          const block = f.block_minutes;
          const pax = f.pax;
          const origin = f.origin;
          const dest = f.destination;
          const legOrder = f.leg_order;

          // Check Spare Aircraft Substitution
          if (swaps[fid]) {
            activeTail = swaps[fid];
            prevArrTime = null;
            currentLocation = origin;
          }

          // Cancellation check
          if (cancellations.has(fid)) {
            const fRes = {
              flight_id: fid,
              tail_id: activeTail,
              orig_tail_id: origTail,
              leg_order: legOrder,
              origin, destination: dest,
              sched_dep: f.dep, sched_arr: f.arr,
              actual_dep: null, actual_arr: null,
              dep_delay: 0, arr_delay: 0,
              status: 'CANCELLED',
              pax,
              reasons: ['Flight proactively cancelled by dispatcher intervention'],
              root_cause: 'Dispatcher Cancellation',
              is_cancelled: true,
              is_spare: false
            };
            flightResults[fid] = fRes;
            if (!aircraftChains[activeTail]) aircraftChains[activeTail] = [];
            aircraftChains[activeTail].push(fRes);
            currentLocation = origin;
            return;
          }

          // Aircraft location / fleet balance check
          if (currentLocation !== null && currentLocation !== origin) {
            const fRes = {
              flight_id: fid,
              tail_id: activeTail,
              orig_tail_id: origTail,
              leg_order: legOrder,
              origin, destination: dest,
              sched_dep: f.dep, sched_arr: f.arr,
              actual_dep: null, actual_arr: null,
              dep_delay: 0, arr_delay: 0,
              status: 'CANCELLED',
              pax,
              reasons: [`Aircraft ${activeTail} stranded at ${currentLocation} due to upstream flight cancellation`],
              root_cause: 'Aircraft Positioning Disruption',
              is_cancelled: true,
              is_spare: false
            };
            flightResults[fid] = fRes;
            if (!aircraftChains[activeTail]) aircraftChains[activeTail] = [];
            aircraftChains[activeTail].push(fRes);
            return;
          }

          let turnDelay = 0;
          const reasons = [];
          let rootCause = "On Time";

          let readyDep = schedDep;
          if (prevArrTime !== null) {
            const neededReady = prevArrTime + minTurnaround;
            if (neededReady > schedDep) {
              turnDelay = neededReady - schedDep;
              readyDep = neededReady;
              reasons.push(`Late inbound aircraft ${activeTail} (arr +${turnDelay}m buffer deficit)`);
              rootCause = "Inbound Turnaround Delay";
            }
          }

          let depTime = readyDep;

          // Closure at Origin
          if (closedApt && origin === closedApt && cStart !== null && cEnd !== null) {
            if ((depTime >= cStart && depTime < cEnd) || (depTime < cStart && schedDep >= cStart)) {
              reasons.push(`Origin ${origin} closed ${cStartStr}-${cEndStr} (held on ground)`);
              depTime = Math.max(depTime, cEnd);
              rootCause = `Airport Closure: ${origin}`;
            }
          }

          // Closure at Destination (Ground Delay Program)
          if (closedApt && dest === closedApt && cStart !== null && cEnd !== null) {
            const estArr = depTime + block;
            if (estArr >= cStart && estArr < cEnd) {
              reasons.push(`Destination ${dest} closed ${cStartStr}-${cEndStr} (held at ${origin} by GDP)`);
              depTime = cEnd - block;
              rootCause = `Airport Closure: ${dest} (GDP)`;
            }
          }

          const arrTime = depTime + block;
          const depDelay = depTime - schedDep;
          const arrDelay = arrTime - schedArr;
          prevArrTime = arrTime;
          currentLocation = dest;

          let status = 'ON_TIME';
          if (depDelay > 0) {
            status = depDelay >= 60 ? 'SEVERELY_DELAYED' : 'DELAYED';
          }

          const fRes = {
            flight_id: fid,
            tail_id: activeTail,
            orig_tail_id: origTail,
            leg_order: legOrder,
            origin, destination: dest,
            sched_dep: f.dep, sched_arr: f.arr,
            actual_dep: minToTime(depTime),
            actual_arr: minToTime(arrTime),
            dep_delay: depDelay,
            arr_delay: arrDelay,
            status, pax, reasons, root_cause: rootCause,
            is_cancelled: false,
            is_spare: (activeTail !== origTail)
          };

          flightResults[fid] = fRes;
          if (!aircraftChains[activeTail]) aircraftChains[activeTail] = [];
          aircraftChains[activeTail].push(fRes);
        });
      });

      // Connections
      const evaluatedConnections = [];
      let strandedPassengers = 0;
      let brokenConnectionsCount = 0;

      EMBEDDED_DATA.connections.forEach(cx => {
        const cid = cx.connection_id;
        const apt = cx.airport;
        const f1 = flightResults[cx.from_flight];
        const f2 = flightResults[cx.to_flight];
        const pax = cx.passengers;
        const minConnect = cx.min_connect_minutes;

        let status = 'MAINTAINED';
        let reason = 'Connection successful';
        let actualTransfer = null;

        if (!f1 || f1.is_cancelled) {
          status = 'BROKEN';
          reason = `Inbound flight ${cx.from_flight} cancelled`;
        } else if (!f2 || f2.is_cancelled) {
          status = 'BROKEN';
          reason = `Outbound flight ${cx.to_flight} cancelled`;
        } else {
          const f1Arr = timeToMin(f1.actual_arr);
          const f2Dep = timeToMin(f2.actual_dep);
          actualTransfer = f2Dep - f1Arr;
          if (actualTransfer < minConnect) {
            status = 'BROKEN';
            reason = `Transfer time ${actualTransfer}m below minimum required ${minConnect}m`;
          }
        }

        if (status === 'BROKEN') {
          strandedPassengers += pax;
          brokenConnectionsCount += 1;
        }

        evaluatedConnections.push({
          connection_id: cid,
          airport: apt,
          from_flight: cx.from_flight,
          to_flight: cx.to_flight,
          passengers: pax,
          min_connect_minutes: minConnect,
          actual_transfer_minutes: actualTransfer,
          status, reason,
          from_flight_arr: f1 && !f1.is_cancelled ? f1.actual_arr : 'CANCELLED',
          to_flight_dep: f2 && !f2.is_cancelled ? f2.actual_dep : 'CANCELLED'
        });
      });

      // Crews
      const evaluatedCrews = [];
      let crewViolationsCount = 0;

      EMBEDDED_DATA.crews.forEach(cr => {
        const cid = cr.crew_id;
        const dStart = timeToMin(cr.duty_start);
        const maxDuty = cr.max_duty_mins;
        const fids = cr.flight_ids;

        const completed = fids
          .map(id => flightResults[id])
          .filter(f => f && !f.is_cancelled);

        let actualDuty = 0;
        let overage = 0;
        let status = 'LEGAL';
        let lastArr = 'N/A';

        if (completed.length > 0) {
          const lastF = completed[completed.length - 1];
          lastArr = lastF.actual_arr;
          actualDuty = timeToMin(lastArr) - dStart;
          overage = Math.max(0, actualDuty - maxDuty);
          if (overage > 0) {
            status = 'DUTY_EXCEEDED';
            crewViolationsCount += 1;
          }
        } else {
          status = 'OFF_DUTY';
        }

        evaluatedCrews.push({
          crew_id: cid,
          tail_id: cr.tail_id,
          base: cr.base,
          duty_start: cr.duty_start,
          max_duty_mins: maxDuty,
          actual_duty_mins: actualDuty,
          overage_mins: overage,
          status,
          flights_count: fids.length,
          last_arrival: lastArr
        });
      });

      const allFlights = Object.values(flightResults);
      const delayedFlights = allFlights.filter(f => f.dep_delay > 0 && !f.is_cancelled);
      const totalDelayMinutes = delayedFlights.reduce((acc, f) => acc + f.dep_delay, 0);
      const cancelledFlights = allFlights.filter(f => f.is_cancelled);
      const cancelledPax = cancelledFlights.reduce((acc, f) => acc + f.pax, 0);

      const estDelayCost = delayedFlights.reduce((acc, f) => acc + f.pax * (f.dep_delay / 60) * 500, 0);
      const estCancelCost = cancelledPax * 5000;
      const estStrandedCost = strandedPassengers * 4000;
      const estCrewCost = crewViolationsCount * 50000;
      const totalEconomicCost = Math.round(estDelayCost + estCancelCost + estStrandedCost + estCrewCost);

      return {
        meta: {
          closed_airport: closedApt,
          closure_start: cStartStr,
          closure_end: cEndStr,
          cancelled_flights: Array.from(cancellations),
          spare_swaps: swaps
        },
        kpis: {
          total_flights: allFlights.length,
          on_time_flights: allFlights.filter(f => f.status === 'ON_TIME' && !f.is_cancelled).length,
          delayed_flights: delayedFlights.length,
          severely_delayed_flights: allFlights.filter(f => f.status === 'SEVERELY_DELAYED').length,
          cancelled_flights: cancelledFlights.length,
          total_delay_minutes: totalDelayMinutes,
          average_delay_minutes: delayedFlights.length > 0 ? Math.round((totalDelayMinutes / delayedFlights.length) * 10) / 10 : 0,
          broken_connections: brokenConnectionsCount,
          total_connections: EMBEDDED_DATA.connections.length,
          stranded_passengers: strandedPassengers,
          cancelled_passengers: cancelledPax,
          total_impacted_passengers: strandedPassengers + cancelledPax,
          crew_duty_violations: crewViolationsCount,
          total_economic_cost_inr: totalEconomicCost
        },
        flights: flightResults,
        connections: evaluatedConnections,
        crews: evaluatedCrews,
        aircraft_chains: aircraftChains
      };
    }

    // RECOVERY EVALUATOR WITH ROUND-TRIP OUT-AND-BACK PAIRS
    function evaluateRecoveryEngine(closedApt, cStart, cEnd) {
      const baseline = simulateEngine(closedApt, cStart, cEnd);
      const bK = baseline.kpis;
      const options = [];

      // 1. BLR Spare (VT-DS17)
      const blrDelayed = Object.values(baseline.flights).filter(f => f.origin === 'BLR' && f.dep_delay > 0 && !f.is_cancelled);
      if (blrDelayed.length > 0) {
        const target = blrDelayed.sort((a, b) => b.dep_delay - a.dep_delay)[0];
        const sim = simulateEngine(closedApt, cStart, cEnd, [], { [target.flight_id]: 'VT-DS17' });
        options.push({
          id: 'SWAP_SPARE_BLR',
          type: 'SPARE_SWAP',
          title: `Deploy Spare VT-DS17 at BLR for ${target.flight_id}`,
          description: `Substitute spare aircraft VT-DS17 stationed at Kempegowda (BLR) for flight ${target.flight_id} (${target.origin}➔${target.destination}), absorbing rotation delay and resetting downstream legs.`,
          target_flight: target.flight_id,
          target_tail: 'VT-DS17',
          swap_dict: { [target.flight_id]: 'VT-DS17' },
          cancel_list: [],
          delta: {
            delay_minutes_saved: bK.total_delay_minutes - sim.kpis.total_delay_minutes,
            stranded_pax_saved: bK.stranded_passengers - sim.kpis.stranded_passengers,
            crew_violations_saved: bK.crew_duty_violations - sim.kpis.crew_duty_violations,
            cost_saved_inr: bK.total_economic_cost_inr - sim.kpis.total_economic_cost_inr
          },
          result_kpis: sim.kpis
        });
      }

      // 2. DEL Spare (VT-DS18)
      const delDelayed = Object.values(baseline.flights).filter(f => f.origin === 'DEL' && f.dep_delay > 0 && !f.is_cancelled);
      if (delDelayed.length > 0) {
        const target = delDelayed.sort((a, b) => b.dep_delay - a.dep_delay)[0];
        const sim = simulateEngine(closedApt, cStart, cEnd, [], { [target.flight_id]: 'VT-DS18' });
        options.push({
          id: 'SWAP_SPARE_DEL',
          type: 'SPARE_SWAP',
          title: `Deploy Spare VT-DS18 at DEL for ${target.flight_id}`,
          description: `Substitute spare aircraft VT-DS18 stationed at Indira Gandhi (DEL) for flight ${target.flight_id} (${target.origin}➔${target.destination}), instantly resetting downstream punctuality and preventing crew timeout.`,
          target_flight: target.flight_id,
          target_tail: 'VT-DS18',
          swap_dict: { [target.flight_id]: 'VT-DS18' },
          cancel_list: [],
          delta: {
            delay_minutes_saved: bK.total_delay_minutes - sim.kpis.total_delay_minutes,
            stranded_pax_saved: bK.stranded_passengers - sim.kpis.stranded_passengers,
            crew_violations_saved: bK.crew_duty_violations - sim.kpis.crew_duty_violations,
            cost_saved_inr: bK.total_economic_cost_inr - sim.kpis.total_economic_cost_inr
          },
          result_kpis: sim.kpis
        });
      }

      // 3. Out-and-Back Round-Trip Cancellation Pairs
      // Group flights by tail to find spoke pairs
      const flightsByTail = {};
      EMBEDDED_DATA.flights.forEach(f => {
        if (!flightsByTail[f.tail_id]) flightsByTail[f.tail_id] = [];
        flightsByTail[f.tail_id].push(f);
      });

      Object.entries(flightsByTail).forEach(([tail, flist]) => {
        flist.sort((a, b) => a.leg_order - b.leg_order);
        for (let i = 0; i < flist.length - 1; i++) {
          const f1 = flist[i];
          const f2 = flist[i+1];
          if (f1.origin === f2.destination && f1.destination === f2.origin) {
            const f1Res = baseline.flights[f1.flight_id] || {};
            const f2Res = baseline.flights[f2.flight_id] || {};
            if ((f1.origin === closedApt || f1.destination === closedApt) && ((f1Res.dep_delay || 0) > 0 || (f2Res.dep_delay || 0) > 0)) {
              const pairIds = [f1.flight_id, f2.flight_id];
              const sim = simulateEngine(closedApt, cStart, cEnd, pairIds, {});
              options.push({
                id: `CANCEL_PAIR_${f1.flight_id}_${f2.flight_id}`,
                type: 'CANCELLATION',
                title: `Cancel Round-Trip Pair: ${f1.flight_id} & ${f2.flight_id} (${f1.origin}⇄${f1.destination})`,
                description: `Proactively cancel round-trip turn ${f1.flight_id}/${f2.flight_id} to keep aircraft ${tail} at ${f1.origin}, preserving fleet balance and eliminating downstream delays.`,
                target_flight: `${f1.flight_id}, ${f2.flight_id}`,
                target_tail: tail,
                swap_dict: {},
                cancel_list: pairIds,
                delta: {
                  delay_minutes_saved: bK.total_delay_minutes - sim.kpis.total_delay_minutes,
                  stranded_pax_saved: bK.stranded_passengers - sim.kpis.stranded_passengers,
                  crew_violations_saved: bK.crew_duty_violations - sim.kpis.crew_duty_violations,
                  cost_saved_inr: bK.total_economic_cost_inr - sim.kpis.total_economic_cost_inr
                },
                result_kpis: sim.kpis
              });
            }
          }
        }
      });

      // 4. Combined Multi-Hub Strategy
      const combinedSwaps = {};
      if (blrDelayed.length > 0) combinedSwaps[blrDelayed.sort((a,b)=>b.dep_delay-a.dep_delay)[0].flight_id] = 'VT-DS17';
      if (delDelayed.length > 0) combinedSwaps[delDelayed.sort((a,b)=>b.dep_delay-a.dep_delay)[0].flight_id] = 'VT-DS18';

      if (Object.keys(combinedSwaps).length > 0) {
        const sim = simulateEngine(closedApt, cStart, cEnd, [], combinedSwaps);
        options.push({
          id: 'COMBINED_MASTER_DISPATCH',
          type: 'OPTIMAL_MULTI_ACTION',
          title: 'Optimal Multi-Hub Fleet Recovery Plan',
          description: 'Simultaneously deploy available spare aircraft at both BLR and DEL hubs to insulate the national network and prevent cross-regional cascade.',
          target_flight: Object.keys(combinedSwaps).join(', '),
          target_tail: 'VT-DS17 & VT-DS18',
          swap_dict: combinedSwaps,
          cancel_list: [],
          delta: {
            delay_minutes_saved: bK.total_delay_minutes - sim.kpis.total_delay_minutes,
            stranded_pax_saved: bK.stranded_passengers - sim.kpis.stranded_passengers,
            crew_violations_saved: bK.crew_duty_violations - sim.kpis.crew_duty_violations,
            cost_saved_inr: bK.total_economic_cost_inr - sim.kpis.total_economic_cost_inr
          },
          result_kpis: sim.kpis
        });
      }

      options.sort((a, b) => b.delta.cost_saved_inr - a.delta.cost_saved_inr);
      return options;
    }

    function generateAIDispatcherBriefing(sim, options) {
      const k = sim.kpis;
      const meta = sim.meta;
      const apt = meta.closed_airport;

      if (!apt) {
        return {
          model: 'Deterministic Aviation Intelligence Engine',
          incident_summary: 'Network operating at normal baseline parameters. All 70 scheduled flights operating on time.',
          cascade_root_cause: 'No active airport closures or ground stops reported across the national airspace.',
          recommendations: []
        };
      }

      const delayed = Object.values(sim.flights).filter(f => f.dep_delay > 0 && !f.is_cancelled).sort((a,b)=>b.dep_delay-a.dep_delay);
      const brokenCx = sim.connections.filter(c => c.status === 'BROKEN');
      const crewViols = sim.crews.filter(c => c.status === 'DUTY_EXCEEDED');

      const primary = delayed.length > 0 ? delayed[0] : null;
      let rootCause = `Runway closure at ${apt} between ${meta.closure_start} and ${meta.closure_end} IST initiated Ground Delay Program. `;
      if (primary) {
        rootCause += `Flight ${primary.flight_id} (${primary.origin}➔${primary.destination}) sustained +${primary.dep_delay}m delay. With a strict 30-minute minimum turnaround, delays cascaded into downstream legs, breaking ${brokenCx.length} connection(s) and creating ${crewViols.length} regulatory crew violation(s).`;
      }

      const summary = `DISRUPTION NOTAM: Ground Stop & Runway Closure active at ${apt} (${meta.closure_start}-${meta.closure_end} IST). ${k.delayed_flights} flights delayed accumulating ${k.total_delay_minutes} minutes total delay. ${k.stranded_passengers} connecting passengers stranded.`;

      return {
        model: 'Deterministic Aviation Intelligence Engine',
        incident_summary: summary,
        cascade_root_cause: rootCause,
        recommendations: options
      };
    }

    // AI COPILOT GROUNDED QUERY SYSTEM
    function askCopilot(query) {
      const box = document.getElementById('copilot-answer-box');
      box.classList.remove('hidden');

      const k = currentSimulation.kpis;
      const delayed = Object.values(currentSimulation.flights).filter(f => f.dep_delay > 0).sort((a,b)=>b.dep_delay-a.dep_delay);
      const brokenCx = currentSimulation.connections.filter(c => c.status === 'BROKEN');
      const crewViols = currentSimulation.crews.filter(c => c.status === 'DUTY_EXCEEDED');

      let reply = '';
      const q = query.toLowerCase();

      if (q.includes('cr03') || q.includes('crew') || q.includes('timeout') || q.includes('legal')) {
        const cr = currentSimulation.crews.find(c => c.crew_id === 'CR03');
        if (cr && cr.status === 'DUTY_EXCEEDED') {
          reply = `<strong>Crew CR03 Analysis:</strong> Crew CR03 operates rotation VT-DS03 (Base DEL, duty start 11:30 IST). Scheduled duty was 590m (max allowed is 600m DGCA limit, leaving only a 10m buffer). Because inbound flight DS0303 arrived late from BOM into DEL at 19:10, final leg DS0304 to Kolkata pushed back to 19:40 and landed CCU at 22:05. Total actual duty reached <strong>${cr.actual_duty_mins} minutes (+${cr.overage_mins}m illegal overage)</strong>. By civil aviation law, this flight cannot depart without crew relief or spare aircraft substitution.`;
        } else {
          reply = `<strong>Crew Duty Status:</strong> Currently ${crewViols.length} crew rotation(s) exceed the statutory 600-minute DGCA limit. ` + (crewViols.length > 0 ? `Violating crews: ${crewViols.map(c=>c.crew_id + ' (+' + c.overage_mins + 'm)').join(', ')}.` : `All 16 flight crews are 100% legal.`);
        }
      } else if (q.includes('kolkata') || q.includes('cascade') || q.includes('mumbai')) {
        reply = `<strong>The Kolkata Domino Cascade:</strong> A 90-minute storm at Mumbai (15:00-16:30) initiates Ground Delay Program holding DS0302 at Ahmedabad. Aircraft VT-DS03 turns around at BOM and lands in Delhi at 19:10 (+50m delay). The 35m scheduled turnaround buffer at DEL is exhausted, pushing flight DS0304 to Kolkata to depart at 19:40 (+45m delay). This pushes crew CR03 past their legal 600m limit, forcing cancellation unless spare VT-DS18 at DEL is deployed.`;
      } else if (q.includes('connection') || q.includes('stranded') || q.includes('cx')) {
        if (brokenCx.length > 0) {
          const top = brokenCx.sort((a,b)=>b.passengers-a.passengers)[0];
          reply = `<strong>Passenger Connections:</strong> ${brokenCx.length} broken connection(s) stranding <strong>${k.stranded_passengers} total passengers</strong>. Highest volume broken connection is <strong>${top.connection_id} at ${top.airport}</strong> (${top.from_flight} ➔ ${top.to_flight}) with <strong>${top.passengers} stranded passengers</strong>: ${top.reason}.`;
        } else {
          reply = `<strong>Passenger Connections:</strong> All 21 passenger connections are currently maintained on schedule with zero stranded passengers.`;
        }
      } else if (q.includes('swap') || q.includes('cancel') || q.includes('compare')) {
        reply = `<strong>Swap vs. Cancel Strategy:</strong> Deploying spare aircraft (VT-DS17 at BLR or VT-DS18 at DEL) is almost always superior to flight cancellation. A spare swap absorbs the cascade with <strong>zero stranded passengers</strong> and preserves full revenue. In contrast, flight cancellation creates an immediate burden of stranded passengers (average 145 pax/flight) and hotel/rebooking compensation (~₹5,000/pax), but is useful as a round-trip circuit-breaker when spares are out of range.`;
      } else {
        reply = `<strong>AOC Operational Synthesis:</strong> Currently ${k.delayed_flights} of 70 flights are delayed (${k.total_delay_minutes}m total delay time). ${k.stranded_passengers} passengers stranded across ${k.broken_connections} missed connections. ${k.crew_duty_violations} crew legal duty violation(s). Top recovery recommendation: ${recoveryOptions.length > 0 ? recoveryOptions[0].title : 'None required'}.`;
      }

      box.innerHTML = `<span class="text-sky-400 font-bold block mb-1">DISPATCHER INTEL:</span>${reply}`;
    }

    function sendCustomCopilotQuery() {
      const input = document.getElementById('copilot-input');
      const val = input.value.trim();
      if (val) {
        askCopilot(val);
      }
    }

    // BEFORE VS AFTER MODAL
    function openBeforeAfterModal() {
      if (!disruptedSimulation) {
        disruptedSimulation = currentSimulation;
      }
      const bK = disruptedSimulation.kpis;
      const aK = currentSimulation.kpis;

      document.getElementById('modal-before-delayed').textContent = bK.delayed_flights;
      document.getElementById('modal-before-delay-mins').textContent = `${bK.total_delay_minutes}m`;
      document.getElementById('modal-before-pax').textContent = bK.stranded_passengers;
      document.getElementById('modal-before-crews').textContent = bK.crew_duty_violations;

      document.getElementById('modal-after-delayed').textContent = aK.delayed_flights;
      document.getElementById('modal-after-delay-mins').textContent = `${aK.total_delay_minutes}m`;
      document.getElementById('modal-after-pax').textContent = aK.stranded_passengers;
      document.getElementById('modal-after-crews').textContent = aK.crew_duty_violations;

      const delayDiff = bK.total_delay_minutes - aK.total_delay_minutes;
      const paxDiff = bK.stranded_passengers - aK.stranded_passengers;
      const crewDiff = bK.crew_duty_violations - aK.crew_duty_violations;
      const costDiff = bK.total_economic_cost_inr - aK.total_economic_cost_inr;

      document.getElementById('modal-delta-summary').innerHTML = `
        Delay reduced by <strong>${delayDiff}m</strong> • <strong>${paxDiff} passengers rescued</strong> • <strong>${crewDiff} crew violations eliminated</strong>.
      `;
      document.getElementById('modal-delta-cost').textContent = `₹${(costDiff/1000).toFixed(0)}k Saved`;

      const bDelayed = Object.values(disruptedSimulation.flights).filter(f=>f.dep_delay>0).sort((a,b)=>b.dep_delay-a.dep_delay);
      document.getElementById('modal-before-highlights').innerHTML = `
        <div class="font-bold text-rose-400 mb-1">Top Disruptions Unmitigated:</div>
        ${bDelayed.slice(0, 3).map(f=>`<div>• <strong>${f.flight_id}</strong> (${f.origin}➔${f.destination}): +${f.dep_delay}m delay</div>`).join('') || '<div>None</div>'}
        <div class="mt-1 text-rose-300">• ${bK.broken_connections} broken connections (${bK.stranded_passengers} pax stranded)</div>
      `;

      const aDelayed = Object.values(currentSimulation.flights).filter(f=>f.dep_delay>0).sort((a,b)=>b.dep_delay-a.dep_delay);
      document.getElementById('modal-after-highlights').innerHTML = `
        <div class="font-bold text-emerald-400 mb-1">Post-Intervention State:</div>
        ${aDelayed.slice(0, 3).map(f=>`<div>• <strong>${f.flight_id}</strong> (${f.origin}➔${f.destination}): +${f.dep_delay}m delay</div>`).join('') || '<div class="text-emerald-300">✓ All flights running on schedule!</div>'}
        <div class="mt-1 text-emerald-300">• Spare tails deployed, ${aK.broken_connections} broken CX</div>
      `;

      document.getElementById('before-after-modal').classList.remove('hidden');
    }

    function closeBeforeAfterModal() {
      document.getElementById('before-after-modal').classList.add('hidden');
    }

    // PLAYBACK & TIMELINE SCRUBBER
    function handleTimeScrub(val) {
      simClockMinute = parseInt(val, 10);
      updateClockDisplay();
      updateMapAndGanttAtTime();
    }

    function stepTime(delta) {
      simClockMinute = Math.max(300, Math.min(1380, simClockMinute + delta));
      document.getElementById('time-scrubber').value = simClockMinute;
      updateClockDisplay();
      updateMapAndGanttAtTime();
    }

    function updateClockDisplay() {
      const timeStr = minToTime(simClockMinute);
      document.getElementById('current-clock-display').textContent = `${timeStr} IST`;
      
      // Update cursor position on Gantt
      // Timeline goes from 300 (05:00) to 1380 (23:00) = 1080 min span
      const cursor = document.getElementById('gantt-time-cursor');
      if (cursor) {
        const leftOffset = 96; // 24rem width of header
        const timelineWidth = 1004; // approximate available width
        const pct = Math.max(0, Math.min(1, (simClockMinute - 300) / 1080));
        cursor.style.left = `${leftOffset + pct * timelineWidth}px`;
      }
    }

    function togglePlayback() {
      const btn = document.getElementById('play-pause-btn');
      if (isPlaying) {
        clearInterval(playTimer);
        isPlaying = false;
        btn.textContent = '▶';
      } else {
        isPlaying = true;
        btn.textContent = '⏸';
        playTimer = setInterval(() => {
          if (simClockMinute >= 1380) {
            simClockMinute = 300;
          } else {
            simClockMinute += 5;
          }
          document.getElementById('time-scrubber').value = simClockMinute;
          updateClockDisplay();
          updateMapAndGanttAtTime();
        }, 150 / playSpeed);
      }
    }

    function setPlaySpeed(speed) {
      playSpeed = speed;
      if (isPlaying) {
        togglePlayback();
        togglePlayback();
      }
    }

    function updateMapAndGanttAtTime() {
      if (!currentSimulation) return;
      // Count airborne flights at simClockMinute
      const airborne = Object.values(currentSimulation.flights).filter(f => {
        if (f.is_cancelled) return false;
        const dep = timeToMin(f.actual_dep);
        const arr = timeToMin(f.actual_arr);
        return simClockMinute >= dep && simClockMinute < arr;
      });

      document.getElementById('airborne-count-badge').textContent = `${airborne.length} airborne`;
    }

    function projectCoords(lat, lng) {
      const minLng = 68.0, maxLng = 95.0;
      const minLat = 7.5, maxLat = 33.5;
      const svgW = 900, svgH = 950;
      const padding = 70;
      const x = padding + ((lng - minLng) / (maxLng - minLng)) * (svgW - padding * 2);
      const y = (svgH - padding) - ((lat - minLat) / (maxLat - minLat)) * (svgH - padding * 2);
      return { x, y };
    }

    function playAlertPing() {
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.3);
      } catch (e) {}
    }

    function exportSITREP() {
      if (!currentSimulation) return;
      const k = currentSimulation.kpis;
      const meta = currentSimulation.meta;
      const text = [
        `DOMINO SKY | FLIGHT OPERATIONS DISPATCH SITREP REPORT`,
        `======================================================`,
        `Generated: ${new Date().toISOString()}`,
        `Disruption: ${meta.closed_airport ? meta.closed_airport + ' Closed (' + meta.closure_start + ' to ' + meta.closure_end + ' IST)' : 'Normal Operations Baseline'}`,
        ``,
        `KEY PERFORMANCE INDICATORS (KPIs):`,
        `----------------------------------`,
        `Total Flights: ${k.total_flights}`,
        `On-Time Flights: ${k.on_time_flights}`,
        `Delayed Flights: ${k.delayed_flights} (${k.severely_delayed_flights} severely delayed)`,
        `Total Delay Minutes: ${k.total_delay_minutes}m (${(k.total_delay_minutes/60).toFixed(1)} hours)`,
        `Average Delay / Delayed Flight: ${k.average_delay_minutes}m`,
        `Broken Connections: ${k.broken_connections} of ${k.total_connections}`,
        `Stranded Passengers: ${k.stranded_passengers}`,
        `Crew Legal Duty Violations: ${k.crew_duty_violations} (DGCA 600m statutory limit)`,
        `Estimated Financial Cost: INR ${k.total_economic_cost_inr.toLocaleString()}`,
        ``,
        `DELAYED FLIGHTS ROSTER:`,
        `----------------------`
      ];

      Object.values(currentSimulation.flights)
        .filter(f => f.dep_delay > 0)
        .forEach(f => {
          text.push(`* ${f.flight_id} (${f.tail_id}): ${f.origin} -> ${f.destination} | Sched: ${f.sched_dep} Actual: ${f.actual_dep} (+${f.dep_delay}m) | Reasons: ${f.reasons.join('; ')}`);
        });

      const blob = new Blob([text.join('\\n')], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `DominoSky_SITREP_${meta.closed_airport || 'NORMAL'}.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }

    async function init() {
      networkBaseline = {
        meta: EMBEDDED_DATA.meta,
        airports: EMBEDDED_DATA.airports,
        flights: EMBEDDED_DATA.flights,
        connections: EMBEDDED_DATA.connections,
        crews: EMBEDDED_DATA.crews,
        spare_aircraft: EMBEDDED_DATA.spare_aircraft,
        baseline_simulation: simulateEngine(null, null, null)
      };
      currentSimulation = networkBaseline.baseline_simulation;
      updateClockDisplay();
      renderAll();
    }

    function renderAll() {
      renderKPIs();
      renderMap();
      renderGantt();
      renderActiveTab();
      updateMapAndGanttAtTime();
    }

    function renderKPIs() {
      if (!currentSimulation) return;
      const k = currentSimulation.kpis;

      document.getElementById('kpi-total-flights').textContent = k.total_flights;
      document.getElementById('kpi-ontime-flights').textContent = `${k.on_time_flights} on-time`;
      const ontimePct = Math.round((k.on_time_flights / k.total_flights) * 100);
      document.getElementById('kpi-ontime-bar').style.width = `${ontimePct}%`;

      document.getElementById('kpi-delayed-flights').textContent = k.delayed_flights;
      const delayedPct = Math.round((k.delayed_flights / k.total_flights) * 100);
      document.getElementById('kpi-delayed-pct').textContent = `${delayedPct}% network`;
      document.getElementById('kpi-severe-count').textContent = `${k.severely_delayed_flights} severely delayed`;

      document.getElementById('kpi-delay-minutes').textContent = `${k.total_delay_minutes}m`;
      document.getElementById('kpi-delay-hours').textContent = `${(k.total_delay_minutes / 60).toFixed(1)} hrs`;
      document.getElementById('kpi-avg-delay').textContent = `Avg ${k.average_delay_minutes}m / delayed flight`;

      document.getElementById('kpi-stranded-pax').textContent = k.stranded_passengers;
      document.getElementById('kpi-broken-cx').textContent = `${k.broken_connections} broken CX`;

      document.getElementById('kpi-crew-violations').textContent = k.crew_duty_violations;
      const crewEl = document.getElementById('kpi-crew-status');
      if (k.crew_duty_violations > 0) {
        crewEl.textContent = `${k.crew_duty_violations} Over Limit!`;
        crewEl.className = "text-[11px] text-rose-400 font-mono mt-1 font-bold animate-pulse";
      } else {
        crewEl.textContent = "100% Legal";
        crewEl.className = "text-[11px] text-emerald-400 font-mono mt-1";
      }

      document.getElementById('kpi-cost').textContent = `₹${(k.total_economic_cost_inr / 100000).toFixed(1)}L`;
    }

    function renderMap() {
      if (!networkBaseline || !currentSimulation) return;

      const airportsLayer = document.getElementById('airports-layer');
      const routesLayer = document.getElementById('routes-layer');
      const particlesLayer = document.getElementById('particles-layer');

      airportsLayer.innerHTML = '';
      routesLayer.innerHTML = '';
      particlesLayer.innerHTML = '';

      const aptMap = {};
      networkBaseline.airports.forEach(a => {
        aptMap[a.id] = { ...a, ...projectCoords(a.lat, a.lng) };
      });

      const flightMap = currentSimulation.flights;
      const drawnRoutes = new Set();

      Object.values(flightMap).forEach(f => {
        const o = aptMap[f.origin];
        const d = aptMap[f.destination];
        if (!o || !d) return;

        const routeKey = [f.origin, f.destination].sort().join('-');
        if (!drawnRoutes.has(routeKey)) {
          drawnRoutes.add(routeKey);

          const dx = d.x - o.x;
          const dy = d.y - o.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          const cx = (o.x + d.x) / 2 - (dy / dist) * (dist * 0.15);
          const cy = (o.y + d.y) / 2 + (dx / dist) * (dist * 0.15);

          const pathD = `M ${o.x} ${o.y} Q ${cx} ${cy} ${d.x} ${d.y}`;

          const flightsOnRoute = Object.values(flightMap).filter(
            fl => (fl.origin === f.origin && fl.destination === f.destination) || (fl.origin === f.destination && fl.destination === f.origin)
          );
          const hasSevere = flightsOnRoute.some(fl => fl.dep_delay >= 60);
          const hasDelay = flightsOnRoute.some(fl => fl.dep_delay > 0);
          const strokeColor = hasSevere ? '#f43f5e' : (hasDelay ? '#f59e0b' : '#1e3a5f');
          const strokeWidth = hasSevere || hasDelay ? 2.5 : 1.2;
          const strokeOpacity = hasSevere || hasDelay ? 0.85 : 0.35;

          const pathEl = document.createElementNS('http://www.w3.org/2000/svg', 'path');
          pathEl.setAttribute('d', pathD);
          pathEl.setAttribute('fill', 'none');
          pathEl.setAttribute('stroke', strokeColor);
          pathEl.setAttribute('stroke-width', strokeWidth);
          pathEl.setAttribute('stroke-opacity', strokeOpacity);
          routesLayer.appendChild(pathEl);

          if (hasDelay || hasSevere || Math.random() < 0.35) {
            const particle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            particle.setAttribute('r', '2.5');
            particle.setAttribute('fill', hasSevere ? '#fb7185' : (hasDelay ? '#fbbf24' : '#38bdf8'));
            
            const animateMotion = document.createElementNS('http://www.w3.org/2000/svg', 'animateMotion');
            animateMotion.setAttribute('path', pathD);
            animateMotion.setAttribute('dur', `${4 + Math.random() * 4}s`);
            animateMotion.setAttribute('repeatCount', 'indefinite');
            particle.appendChild(animateMotion);
            particlesLayer.appendChild(particle);
          }
        }
      });

      networkBaseline.airports.forEach(apt => {
        const pt = aptMap[apt.id];
        const isClosed = activeDisruption.airport === apt.id;
        const isSpareBase = (apt.id === 'BLR' || apt.id === 'DEL');

        const aptFlights = Object.values(flightMap).filter(f => f.origin === apt.id || f.destination === apt.id);
        const delayedCount = aptFlights.filter(f => f.dep_delay > 0).length;

        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'cursor-pointer');
        g.onclick = () => selectAirportFromMap(apt.id);
        g.onmouseenter = (e) => showMapTooltip(e, apt, delayedCount, aptFlights.length);
        g.onmouseleave = hideMapTooltip;

        if (isClosed) {
          const pulse = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
          pulse.setAttribute('cx', pt.x);
          pulse.setAttribute('cy', pt.y);
          pulse.setAttribute('r', '18');
          pulse.setAttribute('fill', 'url(#hub-glow-closed)');
          pulse.setAttribute('class', 'pulse-ring-red');
          g.appendChild(pulse);
        }

        const node = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        node.setAttribute('cx', pt.x);
        node.setAttribute('cy', pt.y);
        const radius = apt.tier === 'mega_hub' ? 8 : (apt.tier === 'regional_hub' ? 6 : 4.5);
        node.setAttribute('r', radius);

        let nodeFill = '#38bdf8';
        if (isClosed) nodeFill = '#f43f5e';
        else if (delayedCount > 0) nodeFill = '#f59e0b';
        else if (isSpareBase) nodeFill = '#06b6d4';

        node.setAttribute('fill', nodeFill);
        node.setAttribute('stroke', '#090e1a');
        node.setAttribute('stroke-width', '2');
        g.appendChild(node);

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', pt.x + 10);
        text.setAttribute('y', pt.y + 4);
        text.setAttribute('fill', isClosed ? '#fda4af' : (delayedCount > 0 ? '#fde68a' : '#94a3b8'));
        text.setAttribute('font-size', '11');
        text.setAttribute('font-family', 'JetBrains Mono');
        text.setAttribute('font-weight', isClosed || apt.tier === 'mega_hub' ? 'bold' : 'normal');
        text.textContent = apt.id;
        g.appendChild(text);

        airportsLayer.appendChild(g);
      });
    }

    function showMapTooltip(e, apt, delayedCount, totalCount) {
      const tip = document.getElementById('map-tooltip');
      const isClosed = activeDisruption.airport === apt.id;
      tip.innerHTML = `
        <div class="font-bold text-white flex items-center justify-between gap-2 border-b border-slate-700 pb-1 mb-1">
          <span>${apt.id} • ${apt.name}</span>
          ${isClosed ? '<span class="text-rose-400 font-bold">CLOSED</span>' : '<span class="text-sky-400">ACTIVE</span>'}
        </div>
        <div class="text-[11px] text-slate-300">City: ${apt.city} • Tier: ${apt.tier.replace('_', ' ')}</div>
        <div class="text-[11px] text-slate-300">Capacity: ${apt.capacity_per_hour}/hr</div>
        <div class="text-[11px] mt-1 ${delayedCount > 0 ? 'text-amber-400 font-bold' : 'text-emerald-400'}">
          ${delayedCount > 0 ? `⚠️ ${delayedCount} of ${totalCount} flights delayed` : `✓ All ${totalCount} flights on schedule`}
        </div>
        ${apt.id === 'BLR' ? '<div class="text-[10px] text-cyan-400 mt-1 font-bold">★ Spare VT-DS17 Stationed Here</div>' : ''}
        ${apt.id === 'DEL' ? '<div class="text-[10px] text-cyan-400 mt-1 font-bold">★ Spare VT-DS18 Stationed Here</div>' : ''}
        <div class="text-[10px] text-slate-500 mt-1 italic">Click to target disruption</div>
      `;
      tip.style.left = `${e.clientX + 15}px`;
      tip.style.top = `${e.clientY - 40}px`;
      tip.classList.remove('hidden');
    }

    function hideMapTooltip() {
      document.getElementById('map-tooltip').classList.add('hidden');
    }

    function selectAirportFromMap(aptId) {
      document.getElementById('input-airport').value = aptId;
    }

    function renderGantt() {
      if (!currentSimulation) return;
      const rowsContainer = document.getElementById('gantt-rows');
      rowsContainer.innerHTML = '';

      const chains = currentSimulation.aircraft_chains;
      const tails = Object.keys(chains).sort();

      const dayStart = 5 * 60; // 05:00
      const dayDuration = 18 * 60; // 1080 min span (05:00 - 23:00)

      tails.forEach(tail => {
        const flights = chains[tail];
        const row = document.createElement('div');
        row.className = "flex items-center h-8 hover:bg-slate-900/50 rounded px-1 transition relative";

        const header = document.createElement('div');
        header.className = "w-24 shrink-0 font-mono text-[11px] font-semibold text-slate-300 flex items-center gap-1";
        const isSpare = tail === 'VT-DS17' || tail === 'VT-DS18';
        header.innerHTML = `${tail} ${isSpare ? '<span class="text-[9px] px-1 rounded bg-cyan-900/40 text-cyan-400 font-bold">SPARE</span>' : ''}`;
        row.appendChild(header);

        const timeline = document.createElement('div');
        timeline.className = "flex-1 h-6 relative bg-slate-900/40 rounded border border-slate-800/40 overflow-hidden";

        flights.forEach(f => {
          if (f.is_cancelled) {
            const schedM = timeToMin(f.sched_dep);
            const blockM = 60;
            const leftPct = Math.max(0, ((schedM - dayStart) / dayDuration) * 100);
            const widthPct = (blockM / dayDuration) * 100;

            const block = document.createElement('div');
            block.className = "absolute top-0.5 bottom-0.5 rounded text-[10px] font-mono px-1 flex items-center justify-center bg-slate-800/80 text-slate-500 border border-slate-700 line-through cursor-pointer";
            block.style.left = `${leftPct}%`;
            block.style.width = `${Math.max(widthPct, 2)}%`;
            block.title = `${f.flight_id} CANCELLED (${f.origin}->${f.destination})`;
            block.onclick = () => showCascadeModal(f.flight_id);
            block.textContent = f.flight_id;
            timeline.appendChild(block);
            return;
          }

          const depM = timeToMin(f.actual_dep);
          const arrM = timeToMin(f.actual_arr);
          const durM = arrM >= depM ? arrM - depM : (arrM + 1440) - depM;

          const leftPct = Math.max(0, ((depM - dayStart) / dayDuration) * 100);
          const widthPct = (durM / dayDuration) * 100;

          let bgClass = "bg-emerald-600/90 hover:bg-emerald-500 text-white border-emerald-400/40";
          if (f.is_spare) {
            bgClass = "bg-cyan-600 hover:bg-cyan-500 text-white border-cyan-400";
          } else if (f.dep_delay >= 60) {
            bgClass = "bg-rose-600 hover:bg-rose-500 text-white border-rose-400 animate-pulse";
          } else if (f.dep_delay > 0) {
            bgClass = "bg-amber-600 hover:bg-amber-500 text-white border-amber-400";
          }

          const block = document.createElement('div');
          block.className = `absolute top-0.5 bottom-0.5 rounded text-[10px] font-mono font-medium px-1 flex items-center justify-between border cursor-pointer shadow-sm truncate transition ${bgClass}`;
          block.style.left = `${leftPct}%`;
          block.style.width = `${Math.max(widthPct, 3)}%`;
          block.title = `${f.flight_id} (${f.origin}->${f.destination}) | Sched: ${f.sched_dep}-${f.sched_arr} | Actual: ${f.actual_dep}-${f.actual_arr} | Delay: +${f.dep_delay}m | Pax: ${f.pax}`;
          block.onclick = () => showCascadeModal(f.flight_id);

          block.innerHTML = `
            <span class="truncate font-bold">${f.flight_id}</span>
            <span class="text-[9px] opacity-80 hidden sm:inline">${f.origin}-${f.destination}</span>
            ${f.dep_delay > 0 ? `<span class="text-[9px] font-bold bg-black/40 px-1 rounded ml-0.5">+${f.dep_delay}m</span>` : ''}
          `;

          timeline.appendChild(block);
        });

        row.appendChild(timeline);
        rowsContainer.appendChild(row);
      });
    }

    function switchTab(tab) {
      currentTab = tab;
      document.getElementById('tab-btn-flights').className = tab === 'flights' 
        ? "text-xs font-semibold px-3 py-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20 transition"
        : "text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition";

      document.getElementById('tab-btn-connections').className = tab === 'connections'
        ? "text-xs font-semibold px-3 py-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20 transition"
        : "text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition";

      document.getElementById('tab-btn-crews').className = tab === 'crews'
        ? "text-xs font-semibold px-3 py-1.5 rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20 transition"
        : "text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-400 hover:text-white transition";

      renderActiveTab();
    }

    function renderActiveTab() {
      const thead = document.getElementById('table-head');
      const tbody = document.getElementById('table-body');
      const search = (document.getElementById('table-search').value || '').toLowerCase();
      const statusFilter = document.getElementById('status-filter').value;

      thead.innerHTML = '';
      tbody.innerHTML = '';

      if (currentTab === 'flights') {
        thead.innerHTML = `
          <tr>
            <th class="p-2.5">Flight ID</th>
            <th class="p-2.5">Tail</th>
            <th class="p-2.5">Route</th>
            <th class="p-2.5">Sched Times</th>
            <th class="p-2.5">Actual Times</th>
            <th class="p-2.5">Delay</th>
            <th class="p-2.5">Status</th>
            <th class="p-2.5">Pax</th>
            <th class="p-2.5">Root Cause / Lineage</th>
          </tr>
        `;

        const flights = Object.values(currentSimulation.flights);
        flights.forEach(f => {
          if (statusFilter !== 'ALL' && f.status !== statusFilter) return;
          const matchStr = `${f.flight_id} ${f.tail_id} ${f.origin} ${f.destination}`.toLowerCase();
          if (search && !matchStr.includes(search)) return;

          const tr = document.createElement('tr');
          tr.className = "hover:bg-slate-900/60 transition cursor-pointer";
          tr.onclick = () => showCascadeModal(f.flight_id);

          let statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">On Time</span>`;
          if (f.status === 'CANCELLED') {
            statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-slate-700 text-slate-300">Cancelled</span>`;
          } else if (f.status === 'SEVERELY_DELAYED') {
            statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 font-bold">Severe (+${f.dep_delay}m)</span>`;
          } else if (f.status === 'DELAYED') {
            statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-amber-500/10 text-amber-400 border border-amber-500/20">Delayed (+${f.dep_delay}m)</span>`;
          }

          tr.innerHTML = `
            <td class="p-2.5 font-bold text-white flex items-center gap-1.5">
              ${f.flight_id}
              ${f.is_spare ? '<span class="text-[9px] px-1 rounded bg-cyan-900/40 text-cyan-400 font-bold">SPARE</span>' : ''}
            </td>
            <td class="p-2.5 text-slate-300">${f.tail_id}</td>
            <td class="p-2.5 font-semibold text-slate-200">${f.origin} ➔ ${f.destination}</td>
            <td class="p-2.5 text-slate-400">${f.sched_dep} - ${f.sched_arr}</td>
            <td class="p-2.5 font-bold ${f.dep_delay > 0 ? 'text-amber-400' : 'text-slate-300'}">
              ${f.is_cancelled ? '---' : `${f.actual_dep} - ${f.actual_arr}`}
            </td>
            <td class="p-2.5 font-bold ${f.dep_delay > 0 ? 'text-rose-400' : 'text-emerald-400'}">
              ${f.is_cancelled ? 'N/A' : (f.dep_delay > 0 ? `+${f.dep_delay}m` : '0m')}
            </td>
            <td class="p-2.5">${statusBadge}</td>
            <td class="p-2.5 text-slate-300">${f.pax}</td>
            <td class="p-2.5 text-slate-400 truncate max-w-xs" title="${f.reasons.join('; ') || 'Operating normally'}">
              ${f.reasons.length > 0 ? f.reasons.join('; ') : '✓ Operating normally'}
            </td>
          `;
          tbody.appendChild(tr);
        });

      } else if (currentTab === 'connections') {
        thead.innerHTML = `
          <tr>
            <th class="p-2.5">Connection ID</th>
            <th class="p-2.5">Hub Airport</th>
            <th class="p-2.5">Inbound Flight</th>
            <th class="p-2.5">Outbound Flight</th>
            <th class="p-2.5">Min Transfer</th>
            <th class="p-2.5">Actual Transfer</th>
            <th class="p-2.5">Passengers</th>
            <th class="p-2.5">Status</th>
            <th class="p-2.5">Reason / Impact</th>
          </tr>
        `;

        const conns = currentSimulation.connections;
        conns.forEach(c => {
          const matchStr = `${c.connection_id} ${c.airport} ${c.from_flight} ${c.to_flight}`.toLowerCase();
          if (search && !matchStr.includes(search)) return;

          const isBroken = c.status === 'BROKEN';
          const tr = document.createElement('tr');
          tr.className = `hover:bg-slate-900/60 transition ${isBroken ? 'bg-rose-950/20' : ''}`;

          tr.innerHTML = `
            <td class="p-2.5 font-bold text-white">${c.connection_id}</td>
            <td class="p-2.5 font-bold text-sky-400">${c.airport}</td>
            <td class="p-2.5 text-slate-300 font-mono">${c.from_flight} (arr ${c.from_flight_arr})</td>
            <td class="p-2.5 text-slate-300 font-mono">${c.to_flight} (dep ${c.to_flight_dep})</td>
            <td class="p-2.5 text-slate-400">${c.min_connect_minutes}m</td>
            <td class="p-2.5 font-bold ${isBroken ? 'text-rose-400' : 'text-emerald-400'}">
              ${c.actual_transfer_minutes !== null ? `${c.actual_transfer_minutes}m` : 'N/A'}
            </td>
            <td class="p-2.5 font-bold text-white">${c.passengers} pax</td>
            <td class="p-2.5">
              ${isBroken 
                ? '<span class="px-2 py-0.5 rounded text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 font-bold">MISSED / STRANDED</span>' 
                : '<span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">MAINTAINED</span>'}
            </td>
            <td class="p-2.5 text-slate-400">${c.reason}</td>
          `;
          tbody.appendChild(tr);
        });

      } else if (currentTab === 'crews') {
        thead.innerHTML = `
          <tr>
            <th class="p-2.5">Crew ID</th>
            <th class="p-2.5">Assigned Tail</th>
            <th class="p-2.5">Home Base</th>
            <th class="p-2.5">Duty Start</th>
            <th class="p-2.5">Last Arrival</th>
            <th class="p-2.5">Total Duty</th>
            <th class="p-2.5">Legal Limit</th>
            <th class="p-2.5">Status</th>
            <th class="p-2.5">Overage</th>
          </tr>
        `;

        const crews = currentSimulation.crews;
        crews.forEach(cr => {
          const matchStr = `${cr.crew_id} ${cr.tail_id} ${cr.base}`.toLowerCase();
          if (search && !matchStr.includes(search)) return;

          const isIllegal = cr.status === 'DUTY_EXCEEDED';
          const tr = document.createElement('tr');
          tr.className = `hover:bg-slate-900/60 transition ${isIllegal ? 'bg-rose-950/20' : ''}`;

          tr.innerHTML = `
            <td class="p-2.5 font-bold text-white">${cr.crew_id}</td>
            <td class="p-2.5 text-slate-300 font-mono">${cr.tail_id}</td>
            <td class="p-2.5 text-sky-400 font-semibold">${cr.base}</td>
            <td class="p-2.5 text-slate-400">${cr.duty_start}</td>
            <td class="p-2.5 font-bold text-slate-200">${cr.last_arrival}</td>
            <td class="p-2.5 font-bold ${isIllegal ? 'text-rose-400' : 'text-slate-200'}">${cr.actual_duty_mins}m</td>
            <td class="p-2.5 text-slate-400">${cr.max_duty_mins}m (10h)</td>
            <td class="p-2.5">
              ${isIllegal 
                ? '<span class="px-2 py-0.5 rounded text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 font-bold animate-pulse">DUTY EXCEEDED</span>' 
                : '<span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">LEGAL</span>'}
            </td>
            <td class="p-2.5 font-bold ${isIllegal ? 'text-rose-400' : 'text-emerald-400'}">
              ${isIllegal ? `+${cr.overage_mins}m ILLEGAL` : `-${cr.max_duty_mins - cr.actual_duty_mins}m buffer`}
            </td>
          `;
          tbody.appendChild(tr);
        });
      }
    }

    function showCascadeModal(flightId) {
      const f = currentSimulation.flights[flightId];
      if (!f) return;

      document.getElementById('modal-title').textContent = `Cascade Root Cause: ${f.flight_id} (${f.origin} ➔ ${f.destination})`;
      const content = document.getElementById('modal-content');

      let html = `
        <div class="bg-slate-900 p-3 rounded-lg border border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono">
          <div><span class="text-slate-500">Aircraft Tail:</span> <strong class="text-white">${f.tail_id}</strong></div>
          <div><span class="text-slate-500">Leg Sequence:</span> <strong class="text-white">Leg ${f.leg_order}</strong></div>
          <div><span class="text-slate-500">Scheduled:</span> <strong class="text-white">${f.sched_dep} - ${f.sched_arr}</strong></div>
          <div><span class="text-slate-500">Actual:</span> <strong class="${f.dep_delay > 0 ? 'text-amber-400' : 'text-white'}">${f.actual_dep || 'N/A'} - ${f.actual_arr || 'N/A'}</strong></div>
          <div><span class="text-slate-500">Departure Delay:</span> <strong class="${f.dep_delay > 0 ? 'text-rose-400' : 'text-emerald-400'}">+${f.dep_delay} mins</strong></div>
          <div><span class="text-slate-500">Passengers:</span> <strong class="text-white">${f.pax} pax</strong></div>
          <div><span class="text-slate-500">Status:</span> <strong class="text-white">${f.status}</strong></div>
          <div><span class="text-slate-500">Aircraft Type:</span> <strong class="text-white">A320 (180 seats)</strong></div>
        </div>

        <div class="flex flex-col gap-2 mt-2">
          <h4 class="font-bold text-slate-200 uppercase tracking-wider text-[11px]">Chain of Causation (Domino Lineage):</h4>
          <div class="space-y-2">
      `;

      if (f.reasons.length === 0) {
        html += `
          <div class="p-3 bg-emerald-950/20 border border-emerald-500/20 rounded-lg text-emerald-300">
            ✓ <strong>No Cascade Disruption:</strong> Aircraft arrived on time, minimum 30-minute turnaround was preserved, and no airport closures affected this rotation.
          </div>
        `;
      } else {
        f.reasons.forEach((reason, i) => {
          html += `
            <div class="p-2.5 bg-slate-900 border-l-2 border-amber-500 rounded flex items-start gap-2">
              <span class="w-5 h-5 rounded-full bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-xs shrink-0">${i+1}</span>
              <div>
                <p class="font-medium text-slate-200">${reason}</p>
                <p class="text-[11px] text-slate-400 mt-0.5">Delay propagated through aircraft rotation chain without buffer absorption.</p>
              </div>
            </div>
          `;
        });
      }

      html += `
          </div>
        </div>
      `;

      content.innerHTML = html;
      document.getElementById('cascade-modal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('cascade-modal').classList.add('hidden');
    }

    async function handleTriggerDisruption() {
      const airport = document.getElementById('input-airport').value;
      const start = document.getElementById('input-start-time').value;
      const end = document.getElementById('input-end-time').value;

      activeDisruption = { airport, start, end };
      activeInterventions = { cancelled_flight_ids: [], spare_swaps: {} };

      document.getElementById('active-disruption-badge').textContent = `ACTIVE: ${airport} (${start}-${end})`;
      document.getElementById('active-disruption-badge').className = "text-xs font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30 font-bold animate-pulse";

      playAlertPing();

      currentSimulation = simulateEngine(
        activeDisruption.airport,
        activeDisruption.start,
        activeDisruption.end,
        activeInterventions.cancelled_flight_ids,
        activeInterventions.spare_swaps
      );
      disruptedSimulation = currentSimulation;

      recoveryOptions = evaluateRecoveryEngine(
        activeDisruption.airport,
        activeDisruption.start,
        activeDisruption.end
      );

      const aiData = generateAIDispatcherBriefing(currentSimulation, recoveryOptions);
      renderAIDispatcher(aiData, recoveryOptions);
      renderAll();
    }

    function applyPreset(presetKey) {
      if (presetKey === 'BOM_AFTERNOON') {
        document.getElementById('input-airport').value = 'BOM';
        document.getElementById('input-start-time').value = '15:00';
        document.getElementById('input-end-time').value = '16:30';
      } else if (presetKey === 'BOM_MONSOON') {
        document.getElementById('input-airport').value = 'BOM';
        document.getElementById('input-start-time').value = '07:30';
        document.getElementById('input-end-time').value = '09:00';
      } else if (presetKey === 'DEL_FOG') {
        document.getElementById('input-airport').value = 'DEL';
        document.getElementById('input-start-time').value = '08:00';
        document.getElementById('input-end-time').value = '10:00';
      } else if (presetKey === 'CCU_CYCLONE') {
        document.getElementById('input-airport').value = 'CCU';
        document.getElementById('input-start-time').value = '12:00';
        document.getElementById('input-end-time').value = '14:00';
      } else if (presetKey === 'BLR_HALT') {
        document.getElementById('input-airport').value = 'BLR';
        document.getElementById('input-start-time').value = '09:00';
        document.getElementById('input-end-time').value = '11:00';
      }
      handleTriggerDisruption();
    }

    function resetSimulation() {
      activeDisruption = { airport: null, start: null, end: null };
      activeInterventions = { cancelled_flight_ids: [], spare_swaps: {} };
      document.getElementById('active-disruption-badge').textContent = "Network Normal";
      document.getElementById('active-disruption-badge').className = "text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400";
      document.getElementById('recovery-diff-banner').classList.add('hidden');
      document.getElementById('ai-briefing-box').innerHTML = `<p class="text-slate-400 italic">Select an airport closure scenario above to simulate the cascade and unlock AI recovery actions.</p>`;
      document.getElementById('recovery-cards-container').innerHTML = `
        <div class="p-4 border border-dashed border-slate-800 rounded-lg text-center text-xs text-slate-500">
          No active disruption. All flights operating smoothly.
        </div>
      `;
      document.getElementById('recovery-options-count').textContent = '0 options';
      document.getElementById('copilot-answer-box').classList.add('hidden');
      
      currentSimulation = networkBaseline.baseline_simulation;
      disruptedSimulation = null;
      renderAll();
    }

    function renderAIDispatcher(aiData, options) {
      const briefingBox = document.getElementById('ai-briefing-box');
      briefingBox.innerHTML = `
        <div class="text-sky-400 font-bold mb-1 flex items-center justify-between">
          <span>OPERATIONAL SITREP</span>
          <span class="text-[10px] text-slate-500">${aiData.model}</span>
        </div>
        <p class="mb-1 text-slate-200 font-medium">${aiData.incident_summary}</p>
        <p class="text-slate-400 border-t border-slate-800 pt-1 mt-1"><strong>Root Cause Diagnosis:</strong> ${aiData.cascade_root_cause}</p>
      `;

      const container = document.getElementById('recovery-cards-container');
      container.innerHTML = '';
      document.getElementById('recovery-options-count').textContent = `${options.length} actionable plans`;

      if (options.length === 0) {
        container.innerHTML = `
          <div class="p-3 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-400">
            No recovery interventions required; rotation buffers absorbed the ground stop.
          </div>
        `;
        return;
      }

      options.forEach((opt, idx) => {
        const card = document.createElement('div');
        const isOptimal = idx === 0 || opt.type === 'OPTIMAL_MULTI_ACTION';
        card.className = `p-3 rounded-lg border transition flex flex-col gap-2 ${
          isOptimal 
            ? 'bg-gradient-to-r from-sky-950/40 to-indigo-950/40 border-sky-500/40 glow-cyan' 
            : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'
        }`;

        card.innerHTML = `
          <div class="flex items-start justify-between gap-2">
            <div>
              <div class="flex items-center gap-1.5">
                <span class="text-[10px] font-mono px-1.5 py-0.2 rounded ${opt.type === 'SPARE_SWAP' ? 'bg-cyan-900/40 text-cyan-400' : (opt.type === 'CANCELLATION' ? 'bg-rose-900/40 text-rose-400' : 'bg-purple-900/40 text-purple-400')}">
                  ${opt.type.replace('_', ' ')}
                </span>
                ${isOptimal ? '<span class="text-[10px] font-bold text-emerald-400">★ RECOMMENDED</span>' : ''}
              </div>
              <h4 class="font-bold text-xs text-white mt-1">${opt.title}</h4>
            </div>
            <button onclick="applyRecoveryPlan('${opt.id}')" class="shrink-0 text-xs font-semibold px-3 py-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-slate-950 transition shadow font-mono">
              Apply Plan
            </button>
          </div>

          <p class="text-[11px] text-slate-300 leading-normal">${opt.description}</p>

          <div class="grid grid-cols-4 gap-1.5 bg-black/40 p-2 rounded border border-slate-800/80 text-center text-[10px] font-mono">
            <div>
              <span class="text-slate-500 block">Delay Cut</span>
              <strong class="text-emerald-400">-${opt.delta.delay_minutes_saved}m</strong>
            </div>
            <div>
              <span class="text-slate-500 block">Pax Saved</span>
              <strong class="text-emerald-400">+${opt.delta.stranded_pax_saved}</strong>
            </div>
            <div>
              <span class="text-slate-500 block">Crews Saved</span>
              <strong class="${opt.delta.crew_violations_saved > 0 ? 'text-emerald-400' : 'text-slate-400'}">${opt.delta.crew_violations_saved}</strong>
            </div>
            <div>
              <span class="text-slate-500 block">Net Saved</span>
              <strong class="text-emerald-400">₹${(opt.delta.cost_saved_inr / 1000).toFixed(0)}k</strong>
            </div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    async function applyRecoveryPlan(planId) {
      const opt = recoveryOptions.find(o => o.id === planId);
      if (!opt) return;

      activeInterventions.cancelled_flight_ids = opt.cancel_list || [];
      activeInterventions.spare_swaps = opt.swap_dict || {};

      currentSimulation = simulateEngine(
        activeDisruption.airport,
        activeDisruption.start,
        activeDisruption.end,
        activeInterventions.cancelled_flight_ids,
        activeInterventions.spare_swaps
      );

      if (disruptedSimulation) {
        const dK = disruptedSimulation.kpis;
        const cK = currentSimulation.kpis;

        const delaySaved = dK.total_delay_minutes - cK.total_delay_minutes;
        const paxSaved = dK.stranded_passengers - cK.stranded_passengers;
        const crewsSaved = dK.crew_duty_violations - cK.crew_duty_violations;
        const costSaved = dK.total_economic_cost_inr - cK.total_economic_cost_inr;

        document.getElementById('diff-delay').textContent = `-${delaySaved}m`;
        document.getElementById('diff-pax').textContent = `+${paxSaved}`;
        document.getElementById('diff-crews').textContent = `${crewsSaved}`;
        document.getElementById('diff-cost').textContent = `₹${(costSaved / 1000).toFixed(0)}k`;

        document.getElementById('recovery-diff-banner').classList.remove('hidden');
      }

      renderAll();
    }

    async function revertRecovery() {
      activeInterventions = { cancelled_flight_ids: [], spare_swaps: {} };
      document.getElementById('recovery-diff-banner').classList.add('hidden');
      currentSimulation = simulateEngine(
        activeDisruption.airport,
        activeDisruption.start,
        activeDisruption.end,
        [], {}
      );
      renderAll();
    }

    window.onload = init;
  </script>
</body>
</html>
"""

final_html = html_template.replace("__DATASET_JSON__", dataset_json).replace("__INDIA_PATH__", india_path_d)

dest_path = r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\static\index.html"
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(final_html)

standalone_path = r"C:\Users\HP\.gemini\antigravity\scratch\domino-sky\standalone.html"
with open(standalone_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("SUCCESS: Upgraded static/index.html and standalone.html to V2 with Time Scrubber, Copilot Chat, India boundary, and Before vs After comparison!")
print(f"File size: {len(final_html)} bytes")
