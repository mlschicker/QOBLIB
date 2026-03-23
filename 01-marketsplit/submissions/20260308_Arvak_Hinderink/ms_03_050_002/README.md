# Submission for ms_03_050_002

**Status: WITHDRAWN — solution is infeasible.**

The PCE dense encoding (20 variables → 5 qubits) maps 2^5 = 32 qubit states
to 32 out of 2^20 possible variable assignments. None of these 32 assignments
satisfy the market split equality constraints. The encoding is structurally
unable to reach any feasible solution for this instance.

Row violations of the submitted solution:
- Row 0: sum=313, target=299, off by +14
- Row 1: sum=252, target=217, off by +35
- Row 2: sum=256, target=257, off by −1

## CSV Summary

| Field | Value |
|-------|-------|
| Problem | ms_03_050_002 |
| Submitter | Daniel Hinderink (hiq-lab) |
| Date | 8. Mar. 2026 |
|======||
| Reference | https://arvak.io |
|======||
| Best Objective Value | -201117 |
| Optimality Bound | N/A |
|======||
| Modeling Approach | QUBO |
| # Decision Variables | 20 |
| # Binary Variables | 20 |
| # Integer Variables | 0 |
| # Continuous Variables | 0 |
| # Non-Zero Coefficients | 211 |
| Coefficients Type | Integer |
| Coefficients Range | {-202539, 50000} |
|======||
| Workflow | PCE dense: 20 vars -> 5 qubits. COBYLA + statevector sim (2048 shots/eval). |
| Algorithm Type | Stochastic |
| # Runs | 1 |
| # Feasible Runs | 0 |
| # Successful Runs | 0 |
| Success Threshold | 0 |
|======||
| Hardware Specifications | Apple M3 Pro (statevector simulation) |
|======||
| Total Runtime | 0.38 |
| CPU Runtime | 0.38 |
| GPU Runtime | N/A |
| QPU Runtime | N/A |
| Other HW Runtime | N/A |
|======||
| Remarks | INFEASIBLE — withdrawn. PCE compression structurally unable to reach feasible region for constraint-satisfaction problems like market split. |
