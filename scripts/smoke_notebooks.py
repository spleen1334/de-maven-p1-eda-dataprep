"""Execute only reviewed, offline solutions; keep sources and datasets intact."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
SELECTED = (
    "section04_solutions",
    "section05_solutions",
    "section06_exploring_data_solution",
    "section06_visualizing_data_solutions",
)


def hashes(directory):
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*")) if p.is_file()}


def main():
    os.environ["MPLBACKEND"] = "Agg"
    output = ROOT / "artifacts" / "smoke"
    output.mkdir(parents=True, exist_ok=True)
    before = hashes(ROOT / "data")
    report = {"notebooks": [], "data_sha256_before": before,
              "command": "make smoke", "python": sys.version,
              "versions": {name: importlib.metadata.version(name)
                           for name in ("numpy", "pandas", "nbclient", "nbformat")}}
    for name in SELECTED:
        path = ROOT / "notebooks" / "solutions" / f"{name}.ipynb"
        source_bytes = path.read_bytes()
        notebook = nbformat.reads(source_bytes.decode("utf-8"), as_version=4)
        result = {"source": path.relative_to(ROOT).as_posix(), "status": "passed",
                  "input_sha256": hashlib.sha256(source_bytes).hexdigest()}
        started = time.monotonic()
        try:
            NotebookClient(
                notebook, timeout=180, kernel_name="python3", allow_errors=False,
                resources={"metadata": {"path": str(path.parent)}},
            ).execute()
        except Exception as exc:
            result.update(status="failed", error=str(exc), error_type=type(exc).__name__)
            for index, cell in enumerate(notebook.cells, 1):
                errors = [o for o in cell.get("outputs", []) if o.output_type == "error"]
                if errors:
                    result.update(cell=index, source_excerpt=cell.source[:2000],
                                  cell_errors=[dict(o) for o in errors])
                    break
            print(f"FAILED {path.name}: {result.get('cell', 'kernel/setup')}\n{exc}")
        finally:
            result["seconds"] = round(time.monotonic() - started, 3)
            result["source_sha256_after"] = hashlib.sha256(path.read_bytes()).hexdigest()
            result["source_unchanged"] = (
                result["input_sha256"] == result["source_sha256_after"])
            nbformat.write(notebook, output / path.name)
            report["notebooks"].append(result)
        print(f"{result['status'].upper()}: {path.name} ({result['seconds']}s)")
    after = hashes(ROOT / "data")
    report.update(data_sha256_after=after, data_unchanged=before == after)
    report["passed"] = before == after and all(
        item["status"] == "passed" and item["source_unchanged"]
        for item in report["notebooks"])
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Data unchanged: {report['data_unchanged']}; report: {output / 'report.json'}")
    return not report["passed"]


if __name__ == "__main__":
    raise SystemExit(main())
