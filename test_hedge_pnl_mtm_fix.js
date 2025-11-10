// Test hedge P&L mark-to-market fix for misaligned final time

console.log("=== Testing Hedge P&L Mark-to-Market at Final Time ===\n");

// Scenario: Base=10min, Hedge=60min, 8 points (70min total)
// Spots: [1.1000, 1.1030, 1.1020, 1.1050, 1.1060, 1.1070, 1.1060, 1.1050]
// Hedge times: [0, 60]
// Final time: 70 (not a hedge time)

const spots = [1.1000, 1.1030, 1.1020, 1.1050, 1.1060, 1.1070, 1.1060, 1.1050];

console.log("Setup:");
console.log("  Base frequency: 10 minutes");
console.log("  Hedge frequency: 60 minutes");
console.log("  Total time: 70 minutes");
console.log("  Spot prices:", spots);
console.log("");

// Simplified calculation (assume ATM call for demonstration)
console.log("Hedge Activity:");
console.log("");

console.log("t=0: Spot = 1.1000");
console.log("  Initial hedge: Assume -50M (short 50M)");
console.log("  Cumulative hedge: -50M");
console.log("  Weighted avg spot: 1.1000");
console.log("");

console.log("t=60: Spot = 1.1060 (index 6)");
console.log("  Rehedge (delta change): Assume +10M");
console.log("  Cumulative hedge: -50M + 10M = -40M");
console.log("  Update weighted avg spot");
console.log("  Assume weighted avg = 1.1015 (simplified)");
console.log("");

const cumulativeHedge = -40; // millions
const avgSpot = 1.1015;
const spotAt60 = spots[6]; // 1.1060
const spotAt70 = spots[7]; // 1.1050

console.log("Position after t=60 hedge:");
console.log("  Cumulative hedge: " + cumulativeHedge + "M");
console.log("  Weighted avg spot: " + avgSpot);
console.log("");

console.log("=== BEFORE FIX (WRONG) ===");
console.log("t=70: Spot = " + spotAt70);
console.log("  Hedge P&L frozen at t=60 spot level");
console.log("  Hedge P&L = " + cumulativeHedge + " × (" + spotAt60 + " - " + avgSpot + ")");
const wrongPnL = cumulativeHedge * (spotAt60 - avgSpot);
console.log("  Hedge P&L = " + wrongPnL + "M = " + (wrongPnL * 1000) + "k");
console.log("  Problem: Uses spot from t=60 (1.1060), not current spot at t=70 (1.1050)");
console.log("");

console.log("=== AFTER FIX (CORRECT) ===");
console.log("t=70: Spot = " + spotAt70);
console.log("  Hedge P&L mark-to-market at current spot");
console.log("  Hedge P&L = " + cumulativeHedge + " × (" + spotAt70 + " - " + avgSpot + ")");
const correctPnL = cumulativeHedge * (spotAt70 - avgSpot);
console.log("  Hedge P&L = " + correctPnL + "M = " + (correctPnL * 1000) + "k");
console.log("  Correct: Uses current spot at t=70 (1.1050)");
console.log("");

console.log("Difference:");
const difference = correctPnL - wrongPnL;
console.log("  " + (difference * 1000).toFixed(1) + "k");
console.log("");

console.log("Explanation:");
console.log("  Cumulative hedge: -40M (short position)");
console.log("  Weighted avg: 1.1015");
console.log("  Spot at t=60: 1.1060 (higher)");
console.log("  Spot at t=70: 1.1050 (moved down from t=60)");
console.log("");
console.log("  Since we're short and spot moved DOWN from 1.1060 to 1.1050:");
console.log("  → We make money! Hedge P&L should IMPROVE");
console.log("");
console.log("  Wrong (frozen at t=60):");
console.log("    -40M × (1.1060 - 1.1015) = -40M × 0.0045 = -1.8M = -1800k (loss)");
console.log("");
console.log("  Correct (mark-to-market at t=70):");
console.log("    -40M × (1.1050 - 1.1015) = -40M × 0.0035 = -1.4M = -1400k (smaller loss)");
console.log("");
console.log("  Improvement: +400k (because spot moved in our favor)");
console.log("");

console.log("KEY INSIGHT:");
console.log("  Hedge P&L MUST always be calculated as:");
console.log("  Hedge_P&L = Cumulative_Hedge × (Current_Spot - Weighted_Avg_Spot)");
console.log("");
console.log("  Where 'Current_Spot' is the spot at the TIME we're displaying,");
console.log("  NOT the spot at the last hedge time.");
console.log("");
console.log("  This is mark-to-market: the hedge position gets revalued");
console.log("  at every time step, even when we're not actively trading.");

console.log("\n=== Test Complete ===");
