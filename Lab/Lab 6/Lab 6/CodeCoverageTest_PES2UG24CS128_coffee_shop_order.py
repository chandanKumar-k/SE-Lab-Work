import pytest

from coffee_shop_order import check_espresso_machine, process_order_batch


def test_process_order_batch_covers_sizes_customizations_and_discounts():
    orders = [
        {
            "paid": True,
            "size": "small",
            "is_member": True,
            "customizations": [
                {"type": "syrup", "cost": 1.0},
                {"type": "syrup", "cost": 2.0},
                {"type": "standard", "cost": 0.5},
            ],
        },
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"},
    ]

    assert process_order_batch(orders, 0.1) == {
        "total": 17.49,
        "status": "COMPLETED",
    }


@pytest.mark.parametrize(
    ("orders", "tax_rate"),
    [
        ("not a list", 0.0),
        ([], -0.01),
    ],
)
def test_process_order_batch_rejects_invalid_input(orders, tax_rate):
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch(orders, tax_rate)


def test_process_order_batch_skips_and_rejects_invalid_items():
    orders = [
        {},
        {"paid": True, "size": "extra-large"},
        {
            "paid": True,
            "size": "small",
            "customizations": [
                {"type": "standard", "cost": -1.0},
                {"type": "allergen_alert"},
            ],
        },
    ]

    assert process_order_batch(orders, 0.0) == {
        "total": 3.0,
        "status": "COMPLETED",
    }


def test_process_order_batch_audits_and_stops_strict_allergy_orders():
    orders = [
        {
            "paid": True,
            "strict_allergy": True,
            "is_member": True,
            "customizations": [{"type": "allergen_alert"}],
        },
        *({"paid": True, "size": "unknown"} for _ in range(5)),
    ]

    assert process_order_batch(orders, 0.1) == {
        "total": 0.0,
        "status": "AUDIT_REJECTED",
    }


def test_process_order_batch_returns_no_sale_for_empty_batch():
    assert process_order_batch([], 0.1) == {"total": 0.0, "status": "NO_SALE"}


def test_check_espresso_machine_covers_all_outcomes():
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine([[], [97.0, 96.0, 95.0]]) == "OPTIMAL"
    assert check_espresso_machine([[97.0, 97.0]]) == "SHUTDOWN"
