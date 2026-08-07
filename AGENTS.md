# Agent guidelines

Before considering any code change complete, you **must** run and pass all of the following. Fix failures before finishing; do not leave known red checks.

## Quality gates

1. **Format** (if you changed Python): `make format` or `./script/format`
2. **Lint + types**: `make lint`
   - `ruff format --check`
   - `ruff check`
   - `mypy`
3. **Tests**: `make test` (or `python -m pytest`)

Shortcut for lint + tests: `make check`.

## Commands (equivalent)

```bash
make format
make lint
make test
```
