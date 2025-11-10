// Test custom strike functionality

console.log("=== Testing Custom Strike Logic ===\n");

const initialSpot = 1.1000;

console.log("Initial spot:", initialSpot);
console.log("");

// Test 1: Strike Price mode - OTM Put
console.log("Test 1: Strike Price = 1.0850 (below spot)");
const strike1 = 1.0850;
const optionType1 = strike1 < initialSpot ? 'put' : 'call';
console.log("  Strike:", strike1);
console.log("  Auto-determined type:", optionType1);
console.log("  Expected: Put (since 1.0850 < 1.1000)");
console.log("  Result:", optionType1 === 'put' ? "✓" : "✗");
console.log("");

// Test 2: Strike Price mode - OTM Call
console.log("Test 2: Strike Price = 1.1250 (above spot)");
const strike2 = 1.1250;
const optionType2 = strike2 < initialSpot ? 'put' : 'call';
console.log("  Strike:", strike2);
console.log("  Auto-determined type:", optionType2);
console.log("  Expected: Call (since 1.1250 > 1.1000)");
console.log("  Result:", optionType2 === 'call' ? "✓" : "✗");
console.log("");

// Test 3: Strike Price mode - ATM
console.log("Test 3: Strike Price = 1.1000 (at spot)");
const strike3 = 1.1000;
const optionType3 = strike3 < initialSpot ? 'put' : 'call';
console.log("  Strike:", strike3);
console.log("  Auto-determined type:", optionType3);
console.log("  Expected: Call (ATM convention: >= spot is call)");
console.log("  Result:", optionType3 === 'call' ? "✓" : "✗");
console.log("");

// Test 4: Delta mode - 15 delta Call
console.log("Test 4: Delta mode - 15Δ Call");
const deltaInput4 = 15;
const deltaDecimal4 = deltaInput4 / 100;
const userType4 = 'call';
const targetDelta4 = userType4 === 'put' ? -deltaDecimal4 : deltaDecimal4;
console.log("  Input delta:", deltaInput4);
console.log("  Delta decimal:", deltaDecimal4);
console.log("  User selected:", userType4);
console.log("  Target delta for calculation:", targetDelta4);
console.log("  Expected: +0.15");
console.log("  Result:", targetDelta4 === 0.15 ? "✓" : "✗");
console.log("");

// Test 5: Delta mode - 35 delta Put
console.log("Test 5: Delta mode - 35Δ Put");
const deltaInput5 = 35;
const deltaDecimal5 = deltaInput5 / 100;
const userType5 = 'put';
const targetDelta5 = userType5 === 'put' ? -deltaDecimal5 : deltaDecimal5;
console.log("  Input delta:", deltaInput5);
console.log("  Delta decimal:", deltaDecimal5);
console.log("  User selected:", userType5);
console.log("  Target delta for calculation:", targetDelta5);
console.log("  Expected: -0.35");
console.log("  Result:", targetDelta5 === -0.35 ? "✓" : "✗");
console.log("");

// Test 6: Delta mode - 50 delta Call (ATM)
console.log("Test 6: Delta mode - 50Δ Call (ATM)");
const deltaInput6 = 50;
const deltaDecimal6 = deltaInput6 / 100;
const userType6 = 'call';
const targetDelta6 = userType6 === 'put' ? -deltaDecimal6 : deltaDecimal6;
console.log("  Input delta:", deltaInput6);
console.log("  Delta decimal:", deltaDecimal6);
console.log("  User selected:", userType6);
console.log("  Target delta for calculation:", targetDelta6);
console.log("  Expected: +0.50 (ATM)");
console.log("  Result:", targetDelta6 === 0.50 ? "✓" : "✗");
console.log("");

// Test 7: Validation - Delta out of range
console.log("Test 7: Validation - Delta = 105 (invalid)");
const deltaInput7 = 105;
const isValid7 = deltaInput7 >= 0 && deltaInput7 <= 100;
console.log("  Input delta:", deltaInput7);
console.log("  Valid range: 0-100");
console.log("  Is valid:", isValid7);
console.log("  Expected: false");
console.log("  Result:", !isValid7 ? "✓" : "✗");
console.log("");

// Test 8: Validation - Delta = 0 (valid edge case)
console.log("Test 8: Validation - Delta = 0 (valid edge case)");
const deltaInput8 = 0;
const isValid8 = deltaInput8 >= 0 && deltaInput8 <= 100;
console.log("  Input delta:", deltaInput8);
console.log("  Valid range: 0-100");
console.log("  Is valid:", isValid8);
console.log("  Expected: true");
console.log("  Result:", isValid8 ? "✓" : "✗");
console.log("");

// Test 9: Validation - Delta = 100 (valid edge case)
console.log("Test 9: Validation - Delta = 100 (valid edge case)");
const deltaInput9 = 100;
const isValid9 = deltaInput9 >= 0 && deltaInput9 <= 100;
console.log("  Input delta:", deltaInput9);
console.log("  Valid range: 0-100");
console.log("  Is valid:", isValid9);
console.log("  Expected: true");
console.log("  Result:", isValid9 ? "✓" : "✗");
console.log("");

// Test 10: Label formatting
console.log("Test 10: Label formatting");
console.log("  Strike Price mode (1.0850, Put):");
const label10a = `Custom: ${1.0850.toFixed(4)} Put`;
console.log("    " + label10a);
console.log("");
console.log("  Delta mode (15Δ Call, strike=1.1065):");
const label10b = `Custom: 15Δ Call (Strike: ${1.1065.toFixed(4)})`;
console.log("    " + label10b);
console.log("");

console.log("=== All Tests Complete ===");
