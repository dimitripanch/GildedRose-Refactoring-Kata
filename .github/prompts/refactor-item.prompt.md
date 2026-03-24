---
name: refactor-item
description: >
  Generates a new ItemUpdater subclass, registers it in the factory, and
  creates unit tests — all following the Strategy pattern used in this project.
mode: agent
---

# Refactor Item: Add a New Gilded Rose Item Type

You are given an **item name** and its **business rules** by the user
(e.g. `/refactor-item Enchanted — quality never drops below 10`).

Follow these steps exactly.

## Step 1 — Understand the rules

Parse the item name and behaviour description from the user's message.
If the rules are ambiguous, ask a clarifying question before proceeding.

## Step 2 — Create the updater class

In `python/gilded_rose.py`, add a new class that inherits from `ItemUpdater`:

```
class <Name>Updater(ItemUpdater):
    def update(self, item):
        # Implement the business rules here.
        # Use self.increase_quality() / self.decrease_quality() to respect bounds.
        # Call self.decrease_sell_in(item) at the end (unless the item is legendary).
```

Place the new class **above** `SulfurasUpdater` to keep legendary items last.

## Step 3 — Register in the factory

In `UpdaterFactory.get_updater()`, add a branch **before** the final
`return NormalUpdater()` that matches the item by name or prefix:

```
if item.name.startswith("<Name>"):
    return <Name>Updater()
```

## Step 4 — Write unit tests

In `python/tests/test_gilded_rose.py`, add tests using the existing
`update_once` helper. Cover **at minimum**:

| Scenario | Why |
|---|---|
| Normal behaviour before sell date | Verifies base rule |
| Behaviour after sell date (`sell_in <= 0`) | Verifies doubled degradation/appreciation |
| Quality floor (quality should not go below 0, or custom floor) | Boundary check |
| Quality ceiling (quality should not exceed 50) | Boundary check |

## Step 5 — Run the test suite

Execute:

```bash
cd python && python3 -m pytest tests/test_gilded_rose.py -v
```

All tests (existing + new) must pass. Fix any failures before finishing.

## Constraints

- **Never modify the `Item` class** — it belongs to the goblin.
- Quality must stay in **[0, 50]** (except Sulfuras at 80).
- Follow **PEP 8** and the naming conventions in `.github/copilot-instructions.md`.

## Reference files

- `python/gilded_rose.py` — source (Strategy pattern + Factory)
- `python/tests/test_gilded_rose.py` — unit tests
- `GildedRoseRequirements.md` — original business rules
