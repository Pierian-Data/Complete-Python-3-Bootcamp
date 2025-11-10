// Test realized volatility calculation

function calculateRealizedVolatility(spotPrices) {
    // Calculate log returns
    const returns = [];
    for (let i = 1; i < spotPrices.length; i++) {
        returns.push(Math.log(spotPrices[i] / spotPrices[i-1]));
    }

    // Calculate 24-hour variance (sum of squared returns)
    const variance24h = returns.reduce((sum, r) => sum + r*r, 0);

    // Annualize
    const timeCoveredDays = 1.0;
    const annualizedVariance = variance24h * (365 / timeCoveredDays);

    // Get volatility
    const realizedVol = Math.sqrt(annualizedVariance);

    return realizedVol;
}

// Test 1: Flat spot series (no volatility)
console.log("Test 1: Flat spot series");
const flatSpots = new Array(145).fill(1.1000);
const flatVol = calculateRealizedVolatility(flatSpots);
console.log("Expected: 0%, Actual:", (flatVol * 100).toFixed(2) + "%");
console.log("Pass:", flatVol === 0 ? "✓" : "✗");

// Test 2: Known volatility
console.log("\nTest 2: Simulated spot series with known moves");
const spots = [1.1000];
// Create 144 small moves of 0.001 each (upward trend)
for (let i = 1; i < 145; i++) {
    spots.push(spots[i-1] * 1.001); // 0.1% move per interval
}

const testVol = calculateRealizedVolatility(spots);
console.log("First spot:", spots[0].toFixed(4));
console.log("Last spot:", spots[144].toFixed(4));
console.log("Realized vol:", (testVol * 100).toFixed(2) + "%");

// Calculate expected: 144 returns of ln(1.001) each
const expectedReturn = Math.log(1.001);
const expectedVariance24h = 144 * expectedReturn * expectedReturn;
const expectedAnnualVol = Math.sqrt(expectedVariance24h * 365);
console.log("Expected vol:", (expectedAnnualVol * 100).toFixed(2) + "%");
console.log("Match:", Math.abs(testVol - expectedAnnualVol) < 0.0001 ? "✓" : "✗");

// Test 3: Random walk
console.log("\nTest 3: Random walk");
const randomSpots = [1.1000];
for (let i = 1; i < 145; i++) {
    const move = (Math.random() - 0.5) * 0.002;
    randomSpots.push(randomSpots[i-1] * (1 + move));
}

const randomVol = calculateRealizedVolatility(randomSpots);
console.log("First spot:", randomSpots[0].toFixed(4));
console.log("Last spot:", randomSpots[144].toFixed(4));
console.log("Realized vol:", (randomVol * 100).toFixed(2) + "%");
console.log("Reasonable (0.1% - 50%):", randomVol > 0.001 && randomVol < 0.5 ? "✓" : "✗");

console.log("\n=== All tests complete ===");
