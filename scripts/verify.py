"""Run finite mathematical checks in an isolated temporary source copy.

Requires numpy and sympy. No renders, point-cloud allocation, network calls,
or TouchDesigner changes. Outputs from each check stay in the temporary copy.
Analytic proofs and historical novelty are outside this executable suite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
CHECKS = [
    ("Rational polygon link projection and Fox colourings", ["research/verify_link.py"]),
    ("Rational graph scalar bounds", ["survey/verify_exact.py"]),
    ("Graph numerical endpoint, symmetry and enclosure checks", ["survey/model.py"]),
    ("Selected axis variants and their rational dimension bounds", ["survey/axis_variants.py"]),
    ("Dense variants and their rational volume bounds", ["survey/dense_variants.py"]),
    ("Thin linked member and matched unlink control", ["survey/low_dimension.py"]),
    ("Graph compiler certificates and allocation guard", ["survey/verify_compiler.py"]),
    ("Independent integer membrane matrix audit", ["survey/audit_membrane.py"]),
    ("Membrane numerical implementation checks", ["constructive/membrane.py"]),
    ("Twenty exact membrane and anchored similarities", ["constructive/export_exact.py"]),
    ("Sixty-four affine equalities and improved dimension brackets", ["constructive/overlaps/certify_bounds.py"]),
    ("Bounded exact distinct-word screen", ["constructive/overlaps/screen_short_words.py"]),
    ("Finite quaternion premises for the free-rotation proof", ["constructive/overlaps/free_rotations.py"]),
    ("Exact norm-13 variant export", ["constructive/overlaps/export_norm13.py"]),
    ("Selected 127-map symbolic similarity export", ["survey/export_aifs.py", "--m", "3", "--axis", "6", "--central", "1/8"]),
    ("Exact complete-sphere membrane tangent bounds", ["constructive/tangent_bounds/certify.py", "--verify"]),
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=ROOT / "scripts" / "verification.json")
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit("Verification requires assertions; do not use python -O.")
    records, sources = [], {}
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="rotational-seeds-check-") as folder:
        work = Path(folder)
        for subtree in ("survey", "constructive", "research"):
            for path in (ROOT / subtree).rglob("*"):
                if path.is_file() and path.suffix in (".py", ".json", ".aifs") and "__pycache__" not in path.parts:
                    relative = path.relative_to(ROOT)
                    target = work / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(path, target)
                    if path.suffix == ".py":
                        sources[relative.as_posix()] = digest(path)
        env = dict(os.environ, PYTHONUTF8="1", PYTHONHASHSEED="0")
        env.pop("PYTHONOPTIMIZE", None)
        for label, command in CHECKS:
            tick = time.monotonic()
            run = subprocess.run([sys.executable, *command], cwd=work, env=env,
                                 capture_output=True, text=True, encoding="utf-8", timeout=300)
            record = {"check": label, "command": "python " + " ".join(command),
                      "status": "passed" if run.returncode == 0 else "failed",
                      "seconds": round(time.monotonic() - tick, 3)}
            records.append(record)
            print(f"{record['status']}: {label}", flush=True)
            if run.returncode:
                record["output"] = (run.stdout + run.stderr)[-6000:]
                break
        # Hash regenerated exact artifacts as provenance without copying them
        # over the reviewed source tree or asserting float bitwise portability.
        certificates = {p.relative_to(work).as_posix(): digest(p)
                        for p in work.rglob("*.json")
                        if "certificate" in p.name or p.name in ("compiler-verification.json", "short_word_screen.json")}
    result = {
        "status": "passed" if len(records) == len(CHECKS) and all(r["status"] == "passed" for r in records) else "failed",
        "checks_passed": sum(r["status"] == "passed" for r in records),
        "checks_total": len(CHECKS), "python": sys.version.split()[0],
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "isolated_temporary_copy": True, "checks": records,
        "source_sha256": sources, "certificate_sha256": certificates,
        "scope": "Finite exact and numerical implementation checks. Analytic proofs require mathematical review; historical novelty is unresolved.",
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{result['checks_passed']}/{len(CHECKS)} checks passed; receipt: {args.receipt}")
    if result["status"] != "passed":
        for entry in records:
            if "output" in entry:
                print(entry["output"])
        raise SystemExit(1)


if __name__ == "__main__":
    main()
