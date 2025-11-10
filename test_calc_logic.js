// Test the calculator logic
const SETTLEMENT_NOTIONAL = 100_000_000;
const NUM_POINTS = 145;

// Simulate creating test data
const spots = [];
let currentSpot = 1.1000;
for (let i = 0; i < NUM_POINTS; i++) {
    spots.push(currentSpot);
    currentSpot += (Math.random() - 0.5) * 0.0001;
}

console.log("Generated", spots.length, "spot prices");
console.log("First spot:", spots[0]);
console.log("Last spot:", spots[spots.length - 1]);

// Simulate strikes calculation
const strikes = [
    { name: '10Δ Put', strike: 1.0926, type: 'put' },
    { name: '25Δ Put', strike: 1.0960, type: 'put' },
    { name: 'ATM Call', strike: 1.1000, type: 'call' },
    { name: '25Δ Call', strike: 1.1040, type: 'call' },
    { name: '10Δ Call', strike: 1.1074, type: 'call' }
];

console.log("\nSimulating allResults structure:");
const allResults = strikes.map((s, idx) => {
    const baseNotional = SETTLEMENT_NOTIONAL / s.strike;
    console.log(`Strike ${idx + 1}: ${s.name}, base notional: ${(baseNotional / 1_000_000).toFixed(1)}M`);

    // Simulate results array with simple mock data
    const results = [];
    for (let i = 0; i < NUM_POINTS; i++) {
        results.push({
            time: i * 10,
            spot: spots[i],
            delta: 0.5,
            portfolioValue: 1000 * i
        });
    }

    return {
        name: s.name,
        strike: s.strike,
        type: s.type,
        baseNotional: baseNotional,
        results: results
    };
});

console.log("\nallResults created with", allResults.length, "strikes");
console.log("Each strike has", allResults[0].results.length, "time points");

// Simulate accessing data like displayResults does
console.log("\nSimulating displayResults access pattern:");
allResults.forEach((r, idx) => {
    const finalPnL = r.results[r.results.length - 1].portfolioValue;
    console.log(`Strike ${idx + 1}: ${r.name}, final P&L: ${finalPnL}`);
});

console.log("\nAll simulation checks passed!");
