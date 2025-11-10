// Test variable-length spot series calculations

const INTERVAL_MINUTES = 10;

function calculateTimePeriod(numPoints) {
    const numIntervals = numPoints - 1;
    const totalMinutes = numIntervals * INTERVAL_MINUTES;
    const totalHours = totalMinutes / 60;
    const totalDays = totalHours / 24;
    const timeYears = totalDays / 365;

    return { numIntervals, totalMinutes, totalHours, totalDays, timeYears };
}

console.log("=== Variable-Length Time Period Calculations ===\n");

// Test Case 1: 1 hour of data (7 points)
console.log("Test Case 1: 1 hour of data");
const test1 = calculateTimePeriod(7);
console.log("  Points: 7");
console.log("  Intervals:", test1.numIntervals);
console.log("  Total minutes:", test1.totalMinutes);
console.log("  Total hours:", test1.totalHours);
console.log("  Total days:", test1.totalDays);
console.log("  Time (years):", test1.timeYears.toFixed(10));
console.log("  Expected: 1/(365×24) =", (1/(365*24)).toFixed(10));
console.log("  Match:", Math.abs(test1.timeYears - 1/(365*24)) < 0.0000001 ? "✓" : "✗");

// Test Case 2: 24 hours (145 points) - original
console.log("\nTest Case 2: 24 hours of data (original)");
const test2 = calculateTimePeriod(145);
console.log("  Points: 145");
console.log("  Intervals:", test2.numIntervals);
console.log("  Total minutes:", test2.totalMinutes);
console.log("  Total hours:", test2.totalHours);
console.log("  Total days:", test2.totalDays);
console.log("  Time (years):", test2.timeYears.toFixed(10));
console.log("  Expected: 1/365 =", (1/365).toFixed(10));
console.log("  Match:", Math.abs(test2.timeYears - 1/365) < 0.0000001 ? "✓" : "✗");

// Test Case 3: 48 hours (289 points)
console.log("\nTest Case 3: 48 hours of data");
const test3 = calculateTimePeriod(289);
console.log("  Points: 289");
console.log("  Intervals:", test3.numIntervals);
console.log("  Total minutes:", test3.totalMinutes);
console.log("  Total hours:", test3.totalHours);
console.log("  Total days:", test3.totalDays);
console.log("  Time (years):", test3.timeYears.toFixed(10));
console.log("  Expected: 2/365 =", (2/365).toFixed(10));
console.log("  Match:", Math.abs(test3.timeYears - 2/365) < 0.0000001 ? "✓" : "✗");

// Test Case 4: 6 hours (37 points)
console.log("\nTest Case 4: 6 hours of data");
const test4 = calculateTimePeriod(37);
console.log("  Points: 37");
console.log("  Intervals:", test4.numIntervals);
console.log("  Total minutes:", test4.totalMinutes);
console.log("  Total hours:", test4.totalHours);
console.log("  Total days:", test4.totalDays);
console.log("  Time (years):", test4.timeYears.toFixed(10));
console.log("  Expected: 0.25/365 =", (0.25/365).toFixed(10));
console.log("  Match:", Math.abs(test4.timeYears - 0.25/365) < 0.0000001 ? "✓" : "✗");

// Test realized volatility annualization
console.log("\n=== Realized Volatility Annualization ===\n");

function calculateRealizedVolatility(spotPrices, totalDays) {
    const returns = [];
    for (let i = 1; i < spotPrices.length; i++) {
        returns.push(Math.log(spotPrices[i] / spotPrices[i-1]));
    }

    const varianceTotalPeriod = returns.reduce((sum, r) => sum + r*r, 0);
    const annualizedVariance = varianceTotalPeriod * (365 / totalDays);
    const realizedVol = Math.sqrt(annualizedVariance);

    return realizedVol;
}

// Test with 1 hour vs 24 hours - same return pattern
console.log("Test: Annualization consistency");
const constantReturn = 0.001; // 0.1% per interval

// 1 hour (7 points = 6 intervals)
const spots1h = [1.1000];
for (let i = 0; i < 6; i++) {
    spots1h.push(spots1h[spots1h.length - 1] * Math.exp(constantReturn));
}
const vol1h = calculateRealizedVolatility(spots1h, test1.totalDays);

// 24 hours (145 points = 144 intervals)
const spots24h = [1.1000];
for (let i = 0; i < 144; i++) {
    spots24h.push(spots24h[spots24h.length - 1] * Math.exp(constantReturn));
}
const vol24h = calculateRealizedVolatility(spots24h, test2.totalDays);

console.log("  1-hour vol:", (vol1h * 100).toFixed(2) + "%");
console.log("  24-hour vol:", (vol24h * 100).toFixed(2) + "%");
console.log("  Difference:", Math.abs(vol1h - vol24h).toFixed(6));
console.log("  Similar (within 0.01):", Math.abs(vol1h - vol24h) < 0.01 ? "✓" : "✗");

console.log("\n=== All Tests Complete ===");
