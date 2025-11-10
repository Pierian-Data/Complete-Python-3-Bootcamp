// Test variable base data frequency and hedging frequency

function calculateHedgeTimes(totalMinutes, hedgeFrequency) {
    const hedgeTimes = [];
    let hedgeTime = 0;
    while (hedgeTime <= totalMinutes) {
        hedgeTimes.push(hedgeTime);
        hedgeTime += hedgeFrequency;
    }
    return hedgeTimes;
}

console.log("=== Test 1: Base=10, Hedge=10, 145 points (original config) ===");
{
    const baseFreq = 10;
    const hedgeFreq = 10;
    const numPoints = 145;
    const totalMinutes = (numPoints - 1) * baseFreq;
    const hedgeTimes = calculateHedgeTimes(totalMinutes, hedgeFreq);

    console.log("Base frequency:", baseFreq, "min");
    console.log("Hedge frequency:", hedgeFreq, "min");
    console.log("Number of data points:", numPoints);
    console.log("Total time:", totalMinutes, "minutes =", (totalMinutes / 60), "hours");
    console.log("Hedge times:", hedgeTimes.length, "points");
    console.log("Expected hedge times: 145 (every data point)");
    console.log("Match:", hedgeTimes.length === 145 ? "✓" : "✗");
    console.log("Last hedge time:", hedgeTimes[hedgeTimes.length - 1]);
    console.log("Aligned (last hedge = total):", hedgeTimes[hedgeTimes.length - 1] === totalMinutes ? "✓" : "✗");
}

console.log("\n=== Test 2: Base=10, Hedge=60, 145 points ===");
{
    const baseFreq = 10;
    const hedgeFreq = 60;
    const numPoints = 145;
    const totalMinutes = (numPoints - 1) * baseFreq;
    const hedgeTimes = calculateHedgeTimes(totalMinutes, hedgeFreq);

    console.log("Base frequency:", baseFreq, "min");
    console.log("Hedge frequency:", hedgeFreq, "min");
    console.log("Number of data points:", numPoints);
    console.log("Total time:", totalMinutes, "minutes =", (totalMinutes / 60), "hours");
    console.log("Hedge times:", hedgeTimes.length, "points");
    console.log("Expected: [0, 60, 120, ..., 1440] → 25 points");
    console.log("Match:", hedgeTimes.length === 25 ? "✓" : "✗");
    console.log("First few hedge times:", hedgeTimes.slice(0, 5));
    console.log("Last hedge time:", hedgeTimes[hedgeTimes.length - 1]);
    console.log("Aligned (last hedge = total):", hedgeTimes[hedgeTimes.length - 1] === totalMinutes ? "✓" : "✗");

    // Check spot indices
    console.log("\nSpot indices at hedge times:");
    console.log("  Hedge@0 → spot[0]");
    console.log("  Hedge@60 → spot[" + (60 / baseFreq) + "]");
    console.log("  Hedge@120 → spot[" + (120 / baseFreq) + "]");
    console.log("  Hedge@1440 → spot[" + (1440 / baseFreq) + "]");
}

console.log("\n=== Test 3: Base=10, Hedge=60, 8 points (70 min total - MISALIGNED) ===");
{
    const baseFreq = 10;
    const hedgeFreq = 60;
    const numPoints = 8;
    const totalMinutes = (numPoints - 1) * baseFreq;
    const hedgeTimes = calculateHedgeTimes(totalMinutes, hedgeFreq);

    console.log("Base frequency:", baseFreq, "min");
    console.log("Hedge frequency:", hedgeFreq, "min");
    console.log("Number of data points:", numPoints);
    console.log("Total time:", totalMinutes, "minutes");
    console.log("Hedge times:", hedgeTimes);
    console.log("Number of hedge times:", hedgeTimes.length);
    console.log("Expected: [0, 60] → 2 points");
    console.log("Match:", hedgeTimes.length === 2 ? "✓" : "✗");
    console.log("Last hedge time:", hedgeTimes[hedgeTimes.length - 1]);
    console.log("Total time:", totalMinutes);
    console.log("Misaligned (last hedge < total):", hedgeTimes[hedgeTimes.length - 1] < totalMinutes ? "✓" : "✗");
    console.log("→ Need to add final row at time", totalMinutes);

    // Check for realized vol calculation
    console.log("\nRealized vol should use:");
    console.log("  Hedge times: [0, 60]");
    console.log("  Plus final time: 70");
    console.log("  Spot indices: [0, 6, 7]");
    console.log("  Returns: ln(spot[6]/spot[0]), ln(spot[7]/spot[6])");
}

console.log("\n=== Test 4: Base=30, Hedge=120, 97 points (48 hours) ===");
{
    const baseFreq = 30;
    const hedgeFreq = 120;
    const numPoints = 97;
    const totalMinutes = (numPoints - 1) * baseFreq;
    const totalHours = totalMinutes / 60;
    const hedgeTimes = calculateHedgeTimes(totalMinutes, hedgeFreq);

    console.log("Base frequency:", baseFreq, "min");
    console.log("Hedge frequency:", hedgeFreq, "min");
    console.log("Number of data points:", numPoints);
    console.log("Total time:", totalMinutes, "minutes =", totalHours, "hours");
    console.log("Hedge times:", hedgeTimes.length, "points");
    console.log("Expected: [0, 120, 240, ..., 2880] → 25 points");
    console.log("Match:", hedgeTimes.length === 25 ? "✓" : "✗");
    console.log("First few hedge times:", hedgeTimes.slice(0, 5));
    console.log("Last hedge time:", hedgeTimes[hedgeTimes.length - 1]);
    console.log("Aligned (last hedge = total):", hedgeTimes[hedgeTimes.length - 1] === totalMinutes ? "✓" : "✗");

    // Check spot indices
    console.log("\nSpot indices at hedge times:");
    console.log("  Hedge@0 → spot[0]");
    console.log("  Hedge@120 → spot[" + (120 / baseFreq) + "]");
    console.log("  Hedge@240 → spot[" + (240 / baseFreq) + "]");
}

console.log("\n=== Validation Tests ===");
{
    // Test validation: hedge frequency >= base frequency
    const validCombos = [
        {base: 10, hedge: 10, valid: true},
        {base: 10, hedge: 60, valid: true},
        {base: 30, hedge: 30, valid: true},
        {base: 30, hedge: 120, valid: true},
        {base: 60, hedge: 10, valid: false},  // Invalid
        {base: 120, hedge: 60, valid: false}, // Invalid
    ];

    console.log("\nTesting validation rule: hedge_freq >= base_freq");
    validCombos.forEach(({base, hedge, valid}) => {
        const isValid = hedge >= base;
        const status = isValid === valid ? "✓" : "✗";
        console.log(`  Base=${base}, Hedge=${hedge}: Expected ${valid}, Got ${isValid} ${status}`);
    });
}

console.log("\n=== All Tests Complete ===");
