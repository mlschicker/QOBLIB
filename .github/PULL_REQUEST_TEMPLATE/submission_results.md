## QOBLIB PR: Submission / Results Update

Use this template for new submission packages or updated result files.

### Change type
- [ ] New submission package
- [ ] Update to an existing submission package
- [ ] Submission fixes (format/validation only)

### Scope
- **Problem class(es)** (e.g. `01-marketsplit`):
- **Submission root path(s)** (e.g. `01-marketsplit/submissions/<name>`):
- **Instance ID(s) touched**:

### Where the details are
Do not duplicate CSV metadata here; point reviewers to the source files in this PR.
- **Summary CSV path(s)** (`*_summary.csv`):
- **Solution file path(s)** (`*_solution.*` or `solutions/`):
- **Reference/paper/code link(s)** (if applicable):

### Validation checklist (do not remove)
- [ ] I followed `CONTRIBUTING.md`.
- [ ] I ran `python misc/check_submission.py <submission_root>` for each changed submission root.
- [ ] Submission format checks pass locally.
- [ ] Every solution file is **valid** (parses and matches the instance format/size).
- [ ] Feasibility/optimality match what the CSV declares: runs that were **not feasible** have `# Feasible Runs = 0`, and I only asserted a proven optimum (`Optimality Bound` = `Best Objective Value`) when the solution truly is optimal. See `misc/CHECKER_CONTRACT.md`.

### Best-known value handling (do not remove)
- [ ] I checked whether this submission improves the current best-known value for any touched instance.
- [ ] If yes, I updated the corresponding files in `XX-problem/solutions/` in this same PR.
- [ ] If no, no `solutions/` update is required.

### Notes for reviewers
Any context that is not already present in the CSV/submission files.
