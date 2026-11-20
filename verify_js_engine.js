const fs = require('fs');

const html = fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/domino-sky/standalone.html', 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

// Evaluate the script in a mock window context
const ctx = {
  window: {},
  document: {
    getElementById: () => ({ textContent: '', style: {}, innerHTML: '', className: '', classList: { add: ()=>{}, remove: ()=>{} } })
  }
};

const fn = new Function('window', 'document', script + '; return { simulateEngine, evaluateRecoveryEngine, generateAIDispatcherBriefing };');
const { simulateEngine, evaluateRecoveryEngine } = fn(ctx.window, ctx.document);

const groundTruth = JSON.parse(fs.readFileSync('C:/Users/HP/.gemini/antigravity/scratch/domino-sky/ground_truth.json', 'utf8'));

console.log("Verifying JS simulation results against Python ground truth:");
let passed = 0;
for (const [key, truth] of Object.entries(groundTruth)) {
  const [apt, s, e] = key.split('_');
  const res = simulateEngine(apt, s, e);
  const k = res.kpis;
  const tk = truth.kpis;

  const match = (
    k.delayed_flights === tk.delayed_flights &&
    k.total_delay_minutes === tk.total_delay_minutes &&
    k.stranded_passengers === tk.stranded_passengers &&
    k.crew_duty_violations === tk.crew_duty_violations
  );

  console.log(`  ${key}:`);
  console.log(`    JS:     Delayed=${k.delayed_flights}, Mins=${k.total_delay_minutes}, Stranded=${k.stranded_passengers}, CrewViols=${k.crew_duty_violations}`);
  console.log(`    Python: Delayed=${tk.delayed_flights}, Mins=${tk.total_delay_minutes}, Stranded=${tk.stranded_passengers}, CrewViols=${tk.crew_duty_violations}`);
  console.log(`    Match:  ${match ? '✓ 100% IDENTICAL' : '❌ MISMATCH'}`);
  if (match) passed++;
}

console.log(`\nVerification Result: ${passed}/${Object.keys(groundTruth).length} scenarios 100% mathematically identical!`);
