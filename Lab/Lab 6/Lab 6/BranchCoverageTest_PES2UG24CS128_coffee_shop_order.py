import pytest

from coffee_shop_order import check_espresso_machine, process_order_batch


def test_process_order_batch_validates_both_parts_of_input_condition():
    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch("not a list", 0.0)

    with pytest.raises(ValueError, match="Invalid orders list or tax rate"):
        process_order_batch([], -0.01)


def test_process_order_batch_covers_order_and_customization_branches():
    orders = [
        {},
        {
            "paid": True,
            "size": "small",
            "customizations": [
                {"type": "standard", "cost": -1.0},
                {"type": "allergen_alert"},
                {"type": "syrup", "cost": 1.5},
                {"type": "syrup", "cost": 2.0},
                {"type": "standard", "cost": 0.5},
            ],
        },
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large"},
        {"paid": True, "size": "unknown"},
        {
            "paid": True,
            "strict_allergy": True,
            "is_member": True,
            "customizations": [
                {"type": "allergen_alert"},
                {"type": "standard", "cost": 10.0},
            ],
        },
    ]

    assert process_order_batch(orders, 0.0) == {
        "total": 17.0,
        "status": "COMPLETED",
    }


def test_process_order_batch_covers_audit_no_sale_and_completed_statuses():
    audit_orders = [{"paid": True, "size": "invalid"} for _ in range(5)]
    assert process_order_batch(audit_orders, 0.1) == {
        "total": 0.0,
        "status": "AUDIT_REJECTED",
    }
    assert process_order_batch([], 0.1) == {"total": 0.0, "status": "NO_SALE"}
    assert process_order_batch([{"paid": True}], 0.0) == {
        "total": 4.5,
        "status": "COMPLETED",
    }


def test_check_espresso_machine_covers_temperature_streak_branches():
    assert check_espresso_machine([]) == "NO_DATA"
    assert check_espresso_machine([[], [97.0, 96.0]]) == "OPTIMAL"
    assert check_espresso_machine([[97.0, 97.0]]) == "SHUTDOWN"
