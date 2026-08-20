#!/usr/bin/env python3
"""Generate manifest.json for the QOBLIB repository.

Run from the repository root:

    python misc/ci/generate_manifest.py > manifest.json

Or with a specific root:

    python misc/ci/generate_manifest.py --root /path/to/QOBLIB > manifest.json

The manifest is consumed by the qoblib-python package to enumerate and
download files without cloning the repository.

Schema
------
{
  "schema_version": 1,
  "repository": "ZIB-AOPT/QOBLIB",
  "problems": {
    "<slug>": {
      "directory": "<top-level directory name, e.g. 01-marketsplit>",
      "files": [
        {
          "path":     "<repo-relative path>",
          "kind":     "instance" | "solution" | "model" | "submission",
          "name":     "<logical name, e.g. ms_03_050_002>",
          "filename": "<basename of the file>",
          "size":     <byte count as integer>,
          "sha256":   "<64-character hex digest>"
        },
        ...
      ]
    },
    ...
  }
}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Problem class configuration
#
# Maps the manifest slug to:
#   - directory   : top-level directory in the repo
#   - kinds       : mapping of subdirectory name -> KindConfig dict with keys:
#       kind        file kind string ("instance", "solution", "model", "submission")
#       exts        allowlist of lowercase file extensions to include;
#                   any file whose final extension is NOT in this set is skipped
#                   (catches README.md, *.sh, *.zpl, *.csv metadata files, etc.)
#       skip_dirs   (optional) set of immediate child directory names under the
#                   kind subdir to exclude entirely (e.g. instance_gen_set)
#
# Files whose basename starts with '.' are always skipped.
# ---------------------------------------------------------------------------

# Extensions considered data files for each broad category.
_INSTANCE_EXTS  = {".dat", ".json", ".gph", ".xml", ".vrp", ".lp", ".mps", ".gz", ".xz", ".bz2", ".lzma"}
_SOLUTION_EXTS  = {".sol", ".xml", ".gz", ".xz", ".bz2", ".lzma", ".json"}
_MODEL_EXTS     = {".lp", ".mps", ".gz", ".xz", ".bz2", ".lzma", ".qs"}
_SUBMISSION_EXTS = {".sol", ".csv", ".json", ".xml", ".gz", ".xz", ".bz2", ".lzma",
                    ".dat", ".gph", ".lp", ".mps", ".vrp"}

_PROBLEMS: dict[str, dict] = {
    "marketsplit": {
        "directory": "01-marketsplit",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS,
                            "skip_dirs": {"instance_gen_set"}},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "labs": {
        "directory": "02-labs",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "birkhoff": {
        "directory": "03-birkhoff",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "steiner": {
        "directory": "04-steiner",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "sports": {
        "directory": "05-sports",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "portfolio": {
        "directory": "06-portfolio",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "independentset": {
        "directory": "07-independentset",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "network": {
        "directory": "08-network",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "routing": {
        "directory": "09-routing",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
    "topology": {
        "directory": "10-topology",
        "kinds": {
            "instances":   {"kind": "instance",   "exts": _INSTANCE_EXTS},
            "solutions":   {"kind": "solution",   "exts": _SOLUTION_EXTS},
            "models":      {"kind": "model",      "exts": _MODEL_EXTS},
            "submissions": {"kind": "submission", "exts": _SUBMISSION_EXTS},
        },
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _logical_name(rel_path: Path) -> str:
    """Derive the logical instance/solution name from a repo-relative path.

    Strips all known compressed and data suffixes so that, for example:
        01-marketsplit/instances/ms_03_050_002.dat  ->  ms_03_050_002
        02-labs/models/binary_linear/labs_032.lp.xz ->  labs_032

    For directory-based instances (steiner, portfolio) the logical name is
    the name of the subdirectory directly under the kind directory:
        04-steiner/instances/stp_s003_l1_t2_h0_rs97531/arcs.dat
            ->  stp_s003_l1_t2_h0_rs97531
    """
    _STRIP = {".dat", ".sol", ".gph", ".json", ".lp", ".mps",
              ".gz", ".xz", ".bz2", ".lzma", ".xml", ".vrp", ".csv",
              ".opt", ".bst"}   # solution quality suffixes, e.g. foo.opt.sol
    name = rel_path.name
    # Strip suffixes until nothing more can be removed
    while True:
        stem, suffix = Path(name).stem, Path(name).suffix
        if suffix.lower() in _STRIP:
            name = stem
        else:
            break
    return name


def _kind_dir_name(rel_path: Path, prob_dir: str) -> str | None:
    """Return the first path component after <prob_dir>/, or None."""
    parts = rel_path.parts
    # parts[0] == prob_dir, parts[1] == kind subdir, ...
    if len(parts) >= 2 and parts[0] == prob_dir:
        return parts[1]
    return None


def _collect_files(
    root: Path,
    prob_dir: str,
    kinds: dict[str, dict],
) -> list[dict]:
    """Walk one problem directory and return a list of FileEntry dicts."""
    base = root / prob_dir
    if not base.is_dir():
        print(f"  WARNING: {prob_dir}/ not found, skipping", file=sys.stderr)
        return []

    entries: list[dict] = []

    for kind_subdir, cfg in kinds.items():
        kind_str  = cfg["kind"]
        exts      = cfg["exts"]
        skip_dirs = cfg.get("skip_dirs", set())

        kind_path = base / kind_subdir
        if not kind_path.is_dir():
            continue

        for file_path in sorted(kind_path.rglob("*")):
            if not file_path.is_file():
                continue
            if file_path.name.startswith("."):
                continue

            rel = file_path.relative_to(root)
            rel_parts = rel.parts  # (prob_dir, kind_subdir, [...,] filename)

            # Skip explicitly excluded immediate subdirectories.
            if len(rel_parts) > 2 and rel_parts[2] in skip_dirs:
                continue

            # Skip files whose extension is not in the allowlist for this kind.
            if Path(file_path.name).suffix.lower() not in exts:
                continue

            # For directory-based instances (steiner, portfolio) the logical
            # name is the subdirectory directly under the kind dir, not the
            # leaf filename.
            if len(rel_parts) > 3:
                # e.g. 04-steiner/instances/stp_s003_.../arcs.dat
                logical = rel_parts[2]
            else:
                logical = _logical_name(rel)

            entries.append({
                "path":     rel.as_posix(),
                "kind":     kind_str,
                "name":     logical,
                "filename": file_path.name,
                "size":     file_path.stat().st_size,
                "sha256":   _sha256(file_path),
            })

    return entries


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate(root: Path) -> dict:
    manifest: dict = {
        "schema_version": 1,
        "repository": "ZIB-AOPT/QOBLIB",
        "problems": {},
    }

    for slug, cfg in _PROBLEMS.items():
        prob_dir = cfg["directory"]
        print(f"Scanning {prob_dir}/…", file=sys.stderr)
        files = _collect_files(root, prob_dir, cfg["kinds"])
        manifest["problems"][slug] = {
            "directory": prob_dir,
            "files": files,
        }
        print(f"  {len(files)} file(s)", file=sys.stderr)

    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root (default: current directory)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation (default: 2; use 0 for compact output)",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "manifest.json").parent.is_dir():
        pass  # root may not yet have a manifest; that's fine

    manifest = generate(root)
    indent = args.indent if args.indent > 0 else None
    print(json.dumps(manifest, indent=indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
