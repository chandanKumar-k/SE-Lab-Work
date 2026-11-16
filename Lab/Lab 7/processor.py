"""A small input-validation processor used for fuzz testing practice."""

from __future__ import annotations

import math


def normalize_text(value):
    """Trim whitespace and reject empty or invalid strings."""
    if value is None:
        raise TypeError("value cannot be None")
    if not isinstance(value, str):
        raise TypeError("value must be a string")

    cleaned = " ".join(value.strip().split())
    if not cleaned:
        raise ValueError("value cannot be empty")

    return cleaned


def parse_int_list(value):
    """Convert a comma-separated string or list-like input to a list of ints."""
    if value is None:
        raise TypeError("value cannot be None")

    if isinstance(value, int) and not isinstance(value, bool):
        return [value]

    if isinstance(value, str):
        if not value.strip():
            return []

        parts = value.split(",")
        result = []
        for part in parts:
            item = part.strip()
            if item == "":
                raise ValueError("empty item in list")
            try:
                result.append(int(item))
            except ValueError as exc:
                raise ValueError(f"invalid integer value: {item!r}") from exc
        return result

    if isinstance(value, (list, tuple)):
        result = []
        for item in value:
            if isinstance(item, bool):
                raise TypeError("boolean is not a valid integer item")
            if isinstance(item, (int, float)):
                if isinstance(item, float) and not item.is_integer():
                    raise ValueError(f"non-integer numeric value: {item!r}")
                result.append(int(item))
            elif isinstance(item, str):
                stripped = item.strip()
                if stripped == "":
                    raise ValueError("empty item in list")
                try:
                    result.append(int(stripped))
                except ValueError as exc:
                    raise ValueError(f"invalid integer value: {stripped!r}") from exc
            else:
                raise TypeError(f"unsupported item type: {type(item).__name__}")
        return result

    raise TypeError(f"unsupported value type: {type(value).__name__}")


def calculate_total(prices, tax_rate):
    """Return the total with tax applied, rejecting invalid input."""
    if prices is None:
        raise TypeError("prices cannot be None")
    if not isinstance(prices, (list, tuple)):
        raise TypeError("prices must be a list or tuple")
    if not isinstance(tax_rate, (int, float)) or isinstance(tax_rate, bool):
        raise TypeError("tax_rate must be a number")
    if isinstance(tax_rate, float) and not math.isfinite(tax_rate):
        raise ValueError("tax_rate must be finite")
    if tax_rate < 0 or tax_rate > 1:
        raise ValueError("tax_rate must be between 0 and 1")

    total = 0.0
    for price in prices:
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise TypeError(f"unsupported price value: {price!r}")
        try:
            numeric_price = float(price)
        except OverflowError as exc:
            raise ValueError("prices must be finite numbers") from exc
        if not math.isfinite(numeric_price):
            raise ValueError("prices must be finite numbers")
        if numeric_price < 0:
            raise ValueError("prices cannot be negative")
        total += numeric_price
        if not math.isfinite(total):
            raise ValueError("total exceeds the supported numeric range")

    total_with_tax = total * (1 + tax_rate)
    if not math.isfinite(total_with_tax):
        raise ValueError("total exceeds the supported numeric range")

    return round(total_with_tax, 2)


if __name__ == "__main__":
    print("normalized:", normalize_text("   hello   world   "))
    print("integers:", parse_int_list("1, 2, 3, 4"))
    print("total:", calculate_total([10, 20, 30], 0.1))
