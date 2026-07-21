# `misc/ci/` — workflow & pipeline scripts

The scripts GitHub Actions runs to validate submissions, keep best-known values
current, and build the public site. They depend only on the Python standard
library and share the [`site_builder/`](site_builder/) package. Each is exposed
as a `qoblib-*` console script (see [`../pyproject.toml`](../pyproject.toml)) and
is also directly executable.

| Script / command | Used by workflow | Purpose |
| --- | --- | --- |
| `check_submission.py` — `qoblib-check-submission` | `validate-submission.yml` | Authoritative submission validator (structure, CSV format, solution checks). |
| `check_bkv_updates.py` — `qoblib-check-bkv` | `validate-submission.yml` | Informational best-known-value diff for a PR (warn-only). |
| `update_bkv.py` — `qoblib-update-bkv` | `update-bkv.yml` | Recomputes best-known values, copies improving solutions, regenerates the `solutions/README.md` tables. |
| `build_site.py` — `qoblib-build-site` | `pages.yml` | Builds the static GitHub Pages site (JSON data + static frontend copy). |
| `generate_all_readmes.sh` | — (manual) | Runs `check_submission.py --generate-readme` over every submission root. |
| `CHECKER_CONTRACT.md` | — | The exit-code contract shared by the per-problem Rust checkers and `check_submission.py`. |

Run any of them via uv from the repository root:

```bash
uv run --project misc qoblib-check-submission <problem>/submissions/<name>
uv run --project misc qoblib-update-bkv --check
uv run --project misc qoblib-build-site --out _site
```

## `check_submission.py`

Validates that a submission matches the QOBLIB contribution guidelines.

```bash
# Validate one submission root:
uv run --project misc qoblib-check-submission <path_to_submission>

# Validate every submission at once (point --all at the repo root, a problem
# dir, or a submissions/ dir):
uv run --project misc qoblib-check-submission --all .
uv run --project misc qoblib-check-submission --all 03-birkhoff

# Full option list:
uv run --project misc qoblib-check-submission -h
```

`--all` discovers every submission under `<root>/*/submissions/*`, validates each,
and prints a grand-total summary; it exits non-zero if any submission fails.
Combine with `--quiet` (failing instances only) and `--no-check` (skip the
per-problem solution checker for a fast structural pass).

**Solution-checker policy.** The per-problem checkers report a fact about each
solution file via a fixed exit-code contract, and this script turns that into a
pass/fail decision using what the submission declares in its `*_summary.csv`:

- A **malformed / unparseable** solution file always fails.
- **Infeasibility** fails only when the submission claims feasibility
  (`# Feasible Runs > 0` or blank); declare `# Feasible Runs = 0` to report a valid
  but infeasible run without failing.
- **Non-optimality** fails only when the submission asserts a proven optimum
  (`Optimality Bound == Best Objective Value`); a heuristic with
  `Optimality Bound = N/A` is accepted.

See [`CHECKER_CONTRACT.md`](CHECKER_CONTRACT.md) for the exit codes (`0`, `20`,
`21`, `10`, `2`) and the full decision table.

## `update_bkv.py` — best-known values

Replays every submission in release-date order, combines it with the curated
reference solutions, and writes one best-known value per instance:

- copies an improving submission solution into `NN-problem/solutions/` (one file
  per instance), and
- regenerates the attributed table inside each `solutions/README.md` between the
  `<!-- BKV:START … -->` / `<!-- BKV:END -->` markers.

Every problem class is handled; the format-aware objective readers live in
[`site_builder/solutions.py`](site_builder/solutions.py). Preview locally with
`--check` (exits non-zero if anything is stale, writes nothing).

## `check_bkv_updates.py`

Given a PR's base/head SHAs, reports any instance where a changed submission
beats the current reference best-known value. Run with `--warn-only` in CI so it
never blocks the PR — the reference files and tables are regenerated on merge by
`update-bkv.yml`.

## Website data builder

The public site is a static frontend (committed under [`../../website/`](../../website))
driven entirely by JSON generated from the repository. The Python side produces
**only data — never HTML.**

```bash
uv run --project misc qoblib-build-site --out _site                     # full site
uv run --project misc qoblib-build-site --out _site --repo-url <url> --ref <sha>  # PR preview links
uv run --project misc qoblib-build-site --out _site --no-static         # data only
```

### `site_builder/`

The data builder, split into focused modules:

| Module | Responsibility |
| --- | --- |
| `config.py` | Build context (repo/ref URL helpers), problem metadata, table columns |
| `text.py` | Date / name / number parsing and README section extraction |
| `classify.py` | Quantum-hardware / quantum-sim / classical submission classification |
| `solutions.py` | Reference-solution / best-known-value readers (format-aware per problem) |
| `submissions.py` | Canonical `*_summary.csv` submission reader |
| `models.py` | Downloadable model-artifact scanning |
| `metrics.py` | Per-instance metric columns |
| `instances.py` | Instance discovery (flat, bundle, recursive, Birkhoff) |
| `problem.py` | Per-problem payload assembly + best-value resolution |
| `build.py` | Orchestration and JSON output / static-copy |

**Output layout** (consumed by the frontend's `fetch` calls):

```
<out>/data/index.json
<out>/data/leaderboard.json
<out>/data/problems/<id>/{meta,instances,solutions,submissions,submission_groups,instance_submissions}.json
```
