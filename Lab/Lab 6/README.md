# L6_L7_03 — Coffee Shop Order

Lab 6: Code and Branch Coverage

## About

A small Python module that calculates order totals by drink size, milk choices, and syrup customizations, enforces allergy safety protocols, and monitors espresso machine temperature cycles.

## Files

| File | Description |
|------|-------------|
| `coffee_shop_order.py` | The module under test |
| `test_coffee_shop.py` | Starter test file |
| `CodeCoverageTest_PES2UG24CS128_coffee_shop_order.py` | Tests for code (line) coverage |
| `BranchCoverageTest_PES2UG24CS128_coffee_shop_order.py` | Tests for decision and branch coverage |

Keep all your Lab 6 work in this `LAB6` folder. Lab 7 will be added to this repo later.

## Run the coverage suites

Install the test tools with `python -m pip install pytest coverage`, then run
these commands from this folder:

```text
python -m coverage erase
python -m coverage run --source=coffee_shop_order -m pytest -q CodeCoverageTest_PES2UG24CS128_coffee_shop_order.py
python -m coverage report -m coffee_shop_order.py
```

The first suite measures line coverage. For branch coverage, run:

```text
python -m coverage erase
python -m coverage run --branch --source=coffee_shop_order -m pytest -q BranchCoverageTest_PES2UG24CS128_coffee_shop_order.py
python -m coverage report -m coffee_shop_order.py
```

Save a coverage report screenshot only after the corresponding suite achieves
at least 90% coverage.