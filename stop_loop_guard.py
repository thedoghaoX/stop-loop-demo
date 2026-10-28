"""stop_loop_guard.py - a brake for AI fix-the-code loops: stop when all tests pass,
stop after N rounds without progress, void the round if test files are touched.
Standard library only, Python 3.8+. See README.md."""
import hashlib, re, subprocess, sys
from pathlib import Path

# Files that make up the "exam": all of tests/, test files and conftest.py anywhere, pytest config
LOCK_GLOBS = ("tests/**/*", "**/test_*.py", "**/*_test.py", "**/conftest.py",
              "pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini")
SKIP_DIRS = {"__pycache__", ".git", ".venv", "venv", "node_modules", ".pytest_cache"}


def snapshot(root=".", globs=LOCK_GLOBS):
    """Return {relative path: sha256}. Adding, deleting or editing any file changes the result."""
    root = Path(root)
    files = {p for g in globs for p in root.glob(g)
             if p.is_file() and not SKIP_DIRS & set(p.relative_to(root).parts)}
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(files)}


def diff(before, after):
    return sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))


def pytest_check(root=".", args=("-q",), timeout=600):
    """Run real pytest, return (all passed?, passed count, feedback for the AI).
    Progress is judged by the passed count, not by comparing output text
    (output contains timings and changes with every attempt)."""
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", *args], cwd=root,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, 0, f"pytest did not finish within {timeout} seconds"
    lines = r.stdout.strip().splitlines()
    passed = sum(int(n) for n in re.findall(r"(\d+) passed", lines[-1] if lines else ""))
    ok = r.returncode == 0 and passed > 0  # zero tests (returncode 5) or collection errors do not count as passing
    return ok, passed, (r.stdout + r.stderr)[-3000:]


def run_with_brakes(step_fn, check_fn=pytest_check, root=".", max_steps=8, stall_limit=2):
    """step_fn(step number, last feedback) only edits code; check_fn(root) is the independent check.
    Returns (status, steps, feedback); status is done / stalled / tampered / budget."""
    locked = snapshot(root)
    ok, best, feedback = check_fn(root)  # measure the starting point first, so progress can be detected later
    if ok:
        return "done", 0, feedback
    stall = 0
    for step in range(1, max_steps + 1):
        step_fn(step, feedback)
        changed = diff(locked, snapshot(root))
        if changed:  # Rule 0: test-related files changed -> this round is void (restore with git, then investigate)
            return "tampered", step, "test-related files changed: " + ", ".join(changed)
        ok, passed, feedback = check_fn(root)
        if ok:  # Rule 1: all tests pass -> stop
            return "done", step, feedback
        if passed > best:
            best, stall = passed, 0
        else:  # Rule 2: passed count did not beat the best so far -> count it; stop after stall_limit in a row
            stall += 1
            if stall >= stall_limit:
                return "stalled", step, feedback
    return "budget", max_steps, feedback  # Rule 3: out of steps -> stop too
