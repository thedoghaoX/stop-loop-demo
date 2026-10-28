# Close Loop for AI

A tiny brake for AI coding loops. Copy **one file** (`stop_loop_guard.py`) into your project root. It needs only Python 3.8+ and `pytest`.

When you let an AI fix code in a loop, three things go wrong: it never stops, it keeps trying the same dead end, or it edits the tests so they pass. This guard applies three plain rules:

1. **All tests pass → stop.**
2. **No progress for N rounds in a row → stop** (progress means the number of passing tests beats the best so far; it does not compare output text).
3. **Any test-related file touched, added or deleted → that round is void** (`tests/`, any `conftest.py`, `test_*.py`, `pytest.ini`, `pyproject.toml`, ...).

## Use

```python
from stop_loop_guard import run_with_brakes

def step(i, feedback):          # your AI call: give it the pytest feedback, let it edit src/
    ask_ai_to_fix(feedback)

status, steps, feedback = run_with_brakes(step, root=".", max_steps=8, stall_limit=2)
# status: done / stalled / tampered / budget
```

`tampered` means a locked file changed. Check with `git status` and restore with `git checkout`; the guard never deletes anything for you.

## Try it without any AI

```
pip install pytest
python examples/try_guard.py
```

`examples/fake_ai.py` plays six scripted "AI" behaviours against a small project with a real bug, and every round really runs pytest. Output is in `examples/out.txt`.

## Known limits

- It is a brake, not a fixer: it decides when to stop, not how to repair.
- `pyproject.toml` is locked too. If your AI must edit dependencies, remove it from `LOCK_GLOBS`.
- Python/pytest projects only for now.
