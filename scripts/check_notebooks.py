"""Validate primary notebook schemas, literal input paths, and Markdown links."""
import ast
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import nbformat

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NOTEBOOKS = 18
# These deliberately illustrate alternative locations, not shipped inputs.
PATH_EXAMPLES = {
    ("notebooks/demos/section04_gathering_data_code.ipynb", "course_offerings.csv"),
    ("notebooks/demos/section04_gathering_data_code.ipynb",
     "/Users/alice/Desktop/Course_Materials/Data/course_offerings.csv"),
    ("notebooks/demos/section04_gathering_data_code.ipynb", "Data/course_offerings.csv"),
}


def local_target(base, target):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    return base / unquote(parsed.path)


def markdown_links(text):
    # Inline links/images and reference-link definitions; spaces use <...> or %20.
    for match in re.finditer(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^\s)]+)", text):
        yield match.group(1).strip("<>")
    for match in re.finditer(r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)", text):
        yield match.group(1).strip("<>")
    for match in re.finditer(r"""(?:href|src)=["']([^"']+)["']""", text):
        yield match.group(1)


def input_paths(source):
    # Strip IPython line magics so unrelated pandas literals still get checked.
    source = "\n".join("" if line.lstrip().startswith(("!", "%")) else line
                       for line in source.splitlines())
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"cannot inspect Python paths: {exc}") from exc
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        name = node.func.attr
        if not (name.startswith("read_") or name == "connect"):
            continue
        if name == "connect" and not (
            isinstance(node.func.value, ast.Name) and node.func.value.id == "sqlite3"
        ):
            continue
        if name in {"read_sql", "read_sql_query", "read_sql_table"}:
            continue
        args = list(node.args[:1]) + [
            kw.value for kw in node.keywords
            if kw.arg in {"filepath_or_buffer", "path", "io", "database"}
        ]
        for arg in args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                yield arg.value


def main():
    errors = []
    notebooks = sorted((ROOT / "notebooks").glob("*/*.ipynb"))
    if len(notebooks) != EXPECTED_NOTEBOOKS:
        errors.append(f"expected {EXPECTED_NOTEBOOKS} primary notebooks, found {len(notebooks)}")
    references = 0
    for path in notebooks:
        rel = path.relative_to(ROOT).as_posix()
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            nbformat.validate(raw)
        except Exception as exc:
            errors.append(f"{rel}: invalid notebook: {exc}")
            continue
        for index, cell in enumerate(raw["cells"], 1):
            source = "".join(cell["source"])
            try:
                targets = (input_paths(source) if cell["cell_type"] == "code"
                           else markdown_links(source))
                for target in targets:
                    if (rel, target) in PATH_EXAMPLES:
                        continue
                    local = local_target(path.parent, target)
                    if local is not None:
                        references += 1
                        if not local.exists():
                            errors.append(f"{rel}: cell {index}: missing local target {target!r}")
            except ValueError as exc:
                errors.append(f"{rel}: cell {index}: {exc}")
    # Documentation navigation is part of the local link graph; archive is excluded.
    markdown = [ROOT / "README.md", ROOT / "AGENTS.md",
                *sorted((ROOT / "docs").rglob("*.md"))]
    for path in markdown:
        if not path.exists():
            continue
        for target in markdown_links(path.read_text(encoding="utf-8")):
            local = local_target(path.parent, target)
            if local is not None:
                references += 1
                if not local.exists():
                    errors.append(f"{path.relative_to(ROOT)}: missing local target {target!r}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Checked {len(notebooks)} notebooks and {references} local references; {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
