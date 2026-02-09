This is a summary of the results for the LABS problem with $N= 6, 8, 10, 12$. 

We formulate the LABS cost function as a Higher-Order Unconstrained Binary Optimization (HUBO) problem (as first formulated in [1]):

$$ H_C = 2 \sum_{i=1}^{N-3} Z_i \sum_{t=1}^{\lfloor \frac{N-i-1}{2} \rfloor} \sum_{k=t+1}^{N-i-t} Z_{i+t} Z_{i+k} Z_{i+k+t} + \sum_{i=1}^{N-2} Z_i \sum_{k=1}^{\lfloor \frac{N-i}{2} \rfloor} Z_{i+2k} \,, $$

where $Z_i$ denotes the Pauli-$Z$ operator acting on qubit $i$. 

We solve the problem with the Quantum Approximate Optimization Algorithm (QAOA) on the trapped-ion quantum hardware IBEX from Alpine Quantum Technologies (AQT). We use depth $p=1$ and calculate the optimal QAOA parameters $\beta_0$ and $\gamma_0$ with the differential evolution algorithm of the Python package scipy.

We distinguish the CPU time (the time for the parameter optimization), the QPU time (the total time on the quantum processor) and the total runtime. The total runtime includes the CPU time, the QPU time, and a small overhead. The overhead consists mostly of the time for accessing the backend. The QPU time includes the gate times and the calibration time (the ion-trap machine recalibrates the qubits when it detects deviations). We include results with and without the calibration in the table below to illustrate the changes in QPU time and solution quality with calibration.

[1] R. Shaydulin et al., "Evidence of scaling advantage for the quantum approximate optimization algorithm on a
classically intractable problem" Sci. Adv. 10 no. 22, (2024) adm6761, arXiv:2308.02342 [quant-ph].

| Problem Identifier | Best Objective Solution | # Decision Variables | # Binary Variables | # Non-Zero Coefficients <br>(quadratic + quartic terms) | # Successful Runs | Total Runtime [s] | CPU Runtime [s] | QPU Runtime [s] | Calibration | Ground State Probability | Ground State Probability <br>(Random Distribution) | 
| :----------------- | :---------------------- | -------------------: | -----------------: | :------------------------------------------------------ | ----------------: | ----------------: | --------------- | --------------: | ----------- | --------------------------------- | --- | 
| LABS (N = 6)       | 7 (optimal)             |                    6 |                  6 | 6 + 7                                                   |             25/25 |           341.376 |        0.13686    |         334.491 | yes         | 79.98%                            |   43.75%  | 
| LABS (N = 6)       | 7 (optimal)             |                    6 |                  6 | 6 + 7                                                   |             25/25 |           280.306 |        0.13686    |         273.605 | no          | 25.22%                            |   43.75%  | 
| LABS (N = 8)       | 8 (optimal)             |                    8 |                  8 | 12 + 22                                                 |             25/25 |           913.034 |        0.03295    |         906.245 | yes         | 5.18%                             |  6.25%   | 
| LABS (N = 8)       | 8 (optimal)             |                    8 |                  8 | 12 + 22                                                 |             25/25 |           648.782 |        0.03295    |         641.974 | no          | 6.72%                             |  6.25%   | 
| LABS (N = 10)      | 13 (optimal)            |                   10 |                 10 | 20 + 50                                                 |             25/25 |           4.820.06 |        0.05946    |         4812.99 | yes         | 3.5%                              |  3.91%   | 
| LABS (N = 10)      | 13 (optimal)            |                   10 |                 10 | 20 + 50                                                 |             25/25 |           1186.68 |        0.05946    |         1179.95 | no          | 3.82%                              |  3.91%   | 
| LABS (N = 12)      | 10 (optimal)            |                   12 |                 12 | 30 + 95                                                 |             16/25 |           5097.17 |        0.06368    |         5090.35 | yes         | 0.58%                             |  0.39%   | 
| LABS (N = 12)      | 10 (optimal)            |                   12 |                 12 | 30 + 95                                                 |             13/25 |           2522.60 |        0.06368    |         2515.93 | no          | 0.34%                             |  0.39%   | 


The following fields are the same across all instances:

| Field                   | Value                                                   |
| ----------------------- | ------------------------------------------------------- |
| Problem                 | LABS                                                    |
| Date                    | Dec. 2, 2025                                           |
| Submitter               | Daniel Egger (IBM) <br>Christoph Regner (Math.Tec) <br>Juris Ulmanis (AQT) <br>Angelika Widl (Math.Tec) |
| ======                  |                                                         |
| Reference               | -                                                       |
| ======                  |                                                         |
| Best Objective Value    | see table below                                         |
| Optimality Bound        | N/A                                                     |
| ======                  |                                                         |
| Modeling Approach       | HUBO                                                    |
| # Decision Variables    | see table below                                         |
| # Binary Variables      | see table below                                         |
| # Integer Variables     | 0                                                       |
| # Continuous Variables  | 0                                                       |
| # Non-Zero Coefficients | see table below                                         |
| Coefficients Type       | integer                                                 |
| Coefficients Range      | {1, 2}                                                  |
| ======                  |                                                         |
| Workflow                | QAOA (p = 1) and 200 shots per run                      |
| Algorithm Type          | stochastic                                              |
| # Runs                  | 25                                                      |
| # Feasible Runs         | 25 (unconstrained problem)                              |
| # Successful Runs       | see table below                                         |
| Success Threshold       | 0 (requiring optimal solution)                          |
| ======                  |                                                         |
| Hardware Specifications | CPU: HPC University of Innsbruck (Leo 5) <br>QPU: AQT IBEX |
| ======                  |                                                         |
| Total Runtime           | see table below                                         |
| CPU Runtime             | see table below                                         |
| GPU Runtime             | N/A                                                     |
| QPU Runtime             | see table below                                         |
| Other HW Runtime        | N/A                                                     |
