# Copilot Instructions — Gilded Rose Refactoring Kata

## Project Overview

This repository contains the **Gilded Rose Refactoring Kata**, a classic coding exercise
for practicing test-driven refactoring. The repo is polyglot (50+ language ports), but the
**primary working language is Python** (in the `python/` directory).

The business rules are defined in `GildedRoseRequirements.md` at the repo root.

## Architecture (Python port)

The Python implementation uses the **Strategy pattern** with a **Factory**:

| Class | Role |
|---|---|
| `Item` | Data holder (`name`, `sell_in`, `quality`). **Do not modify** — owned by the goblin. |
| `ItemUpdater` | Abstract base with shared helpers (`increase_quality`, `decrease_quality`, `decrease_sell_in`). |
| `NormalUpdater` | Default degradation: −1 before sell date, −2 after. |
| `ConjuredUpdater` | Degrades twice as fast as normal: −2 before sell date, −4 after. |
| `AgedBrieUpdater` | Quality increases: +1 before sell date, +2 after. |
| `BackstageUpdater` | Quality rises as concert approaches (+1 / +2 / +3), drops to 0 after. |
| `SulfurasUpdater` | Legendary — no-op; quality stays at 80, sell_in never changes. |
| `UpdaterFactory` | Maps item names → updater instances. Names starting with `"Conjured"` → `ConjuredUpdater`. |
| `GildedRose` | Entry point; iterates items and delegates to `UpdaterFactory`. |

### Key invariants

- Quality is always in the range **[0, 50]** (except Sulfuras, which is always 80).
- `sell_in` decreases by 1 each day for every item except Sulfuras.
- After the sell-by date (`sell_in <= 0`), degradation/appreciation rates double for normal items.

## Coding Conventions

- **Language**: Python 3.10+
- **Style**: PEP 8; snake_case for functions and variables; PascalCase for classes.
- **Tests**: `unittest` in `python/tests/test_gilded_rose.py`; Approval tests in `test_gilded_rose_approvals.py`.
- **Runner**: `pytest` (see `python/requirements.txt`).
- **No changes to `Item`**: The `Item` class must remain untouched per the kata constraints.

## When Generating or Modifying Code

1. **Preserve the Strategy pattern** — add new item types by creating a new `*Updater` subclass
   and registering it in `UpdaterFactory.get_updater()`.
2. **Write tests first** (or alongside) — every new behaviour needs at least one unit test
   in `test_gilded_rose.py` using the `update_once` helper.
3. **Keep quality bounds** — always clamp quality to 0–50 (use `increase_quality` / `decrease_quality`
   helpers rather than raw arithmetic).
4. **Respect sell_in** — call `decrease_sell_in` at the end of each updater's `update` method
   (except `SulfurasUpdater`).
5. **Match naming** — new conjured items should be detected by `item.name.startswith("Conjured")`.

## Testing

Run all tests from the `python/` directory:

```bash
cd python && python -m pytest tests/ -v
```

Run the text-test fixture for visual inspection:

```bash
cd python && python texttest_fixture.py 30
```

## Adding a New Item Type (checklist)

1. Create `class NewTypeUpdater(ItemUpdater)` with an `update(self, item)` method.
2. Add a name-matching branch in `UpdaterFactory.get_updater()`.
3. Add unit tests covering: before sell date, after sell date, quality floor/ceiling.
4. Run the full test suite and verify no regressions.

## Out of Scope

- Do not submit solutions as pull requests to the upstream `emilybache/GildedRose-Refactoring-Kata` repo.
- Other language ports (Java, TypeScript, etc.) are available for reference but are not the focus of active work.
