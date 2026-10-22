# Contributing to deadlock-external

Thanks for your interest. `deadlock-external` is a hobbyist, educational
project for studying external tooling against Deadlock. **Use at your own
risk** — running this against live matches violates the game's Terms of
Service and may result in a ban.

## Ground rules

- Keep it educational. PRs adding anti-cheat bypasses, kernel drivers, or
  HWID spoofers will be rejected.
- Do not commit real offsets you haven't verified. Placeholder values in
  `deadlock_external/models/offsets.py` are intentional — update them in
  your local `config.toml` or a private fork.
- Do not commit dumps, logs, or anything containing process memory.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Style

- Python 3.11+, type hints on public functions.
- `ruff check .` before opening a PR.
- Service layer is pure logic — no Win32 calls outside
  `deadlock_external/platform/`. This keeps tests headless.

## Pull request checklist

- [ ] Tests pass (`pytest -q`)
- [ ] `ruff check .` clean
- [ ] No offsets or memory dumps committed
- [ ] Change described in the PR body