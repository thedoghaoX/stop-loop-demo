"""Run the guard against the fake AI and demo_proj with real pytest."""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import fake_ai
from stop_loop_guard import pytest_check, run_with_brakes

def check(root):
    ok, passed, fb = pytest_check(root)
    print(f"  [pytest] {fb.strip().splitlines()[-1]}")
    return ok, passed, fb

for sc in fake_ai.SCENARIOS:
    fake_ai.reset()
    print(f"=== scenario {sc} ===")
    ai = fake_ai.make_ai(sc)
    status, step, fb = run_with_brakes(lambda i, f: ai(i), check, root=fake_ai.PROJ)
    print(f"  result: status={status} steps={step}" + (f" | {fb}" if status == "tampered" else ""))
fake_ai.reset()
