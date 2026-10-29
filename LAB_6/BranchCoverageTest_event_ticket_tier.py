import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


@pytest.mark.parametrize("manifests,tax", [
    ("invalid", 0),
    (None, 0),
    ([], -0.01),
])
def test_invalid_inputs(manifests, tax):
    with pytest.raises(ValueError):
        process_ticket_manifest(manifests, tax)


def test_empty_manifest_list():
    assert process_ticket_manifest([], 0) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"
    }


def test_unconfirmed_manifest_is_skipped():
    result = process_ticket_manifest(
        [{"is_confirmed": False, "tier": "vip"}], 0
    )
    assert result["status"] == "ZERO_SALES"


@pytest.mark.parametrize("tier,price", [
    ("vip", 150.0),
    ("premium", 90.0),
    ("general", 45.0),
])
def test_each_valid_tier(tier, price):
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": tier,
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == price
    assert result["status"] == "COMPLETED"


def test_default_tier_and_orders():
    result = process_ticket_manifest(
        [{"is_confirmed": True}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_unknown_tier_is_rejected():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "student"}], 0
    )
    assert result["status"] == "ZERO_SALES"


@pytest.mark.parametrize("qty", [0, -1])
def test_invalid_quantities(qty):
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": qty}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_empty_orders():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": []}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_earlybird_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}], 0
    )
    assert result["total_revenue"] == 72.0


def test_bulk_discount_at_five():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 5}]}], 0
    )
    assert result["total_revenue"] == 205.0


def test_no_bulk_discount_below_five():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 4}]}], 0
    )
    assert result["total_revenue"] == 180.0


def test_fraud_on_general_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 1, "promo": "FRAUD_RISK"}]}], 0
    )
    assert result["total_revenue"] == 45.0


def test_fraud_on_vip_breaks_order_loop():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [
              {"qty": 1},
              {"qty": 1, "promo": "FRAUD_RISK"},
              {"qty": 1},
          ]}], 0
    )
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_SALES"


def test_lounge_enabled():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": True,
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 120.0


def test_lounge_disabled():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": False,
          "orders": [{"qty": 1}]}], 0
    )
    assert result["total_revenue"] == 45.0


def test_audit_threshold_is_strictly_greater_than_four():
    manifests = [
        {"is_confirmed": True, "tier": "invalid"}
        for _ in range(4)
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "ZERO_SALES"


def test_audit_rejection_above_four():
    manifests = [
        {"is_confirmed": True, "tier": "invalid"}
        for _ in range(5)
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result["status"] == "AUDIT_REJECTED"


def test_completed_result_with_tax():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0.1
    )
    assert result == {
        "total_revenue": 99.0, "status": "COMPLETED"
    }


def test_gate_flow_empty_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_flow_empty_stream():
    assert monitor_gate_flow([[]]) == "FLOW_NORMAL"


def test_gate_flow_single_high_rate_is_not_overflow():
    assert monitor_gate_flow([[60]]) == "FLOW_NORMAL"


def test_gate_flow_consecutive_high_rates():
    assert monitor_gate_flow([[51, 52]]) == "OVERFLOW"


def test_gate_flow_streak_resets_after_low_rate():
    assert monitor_gate_flow([[60, 20, 60]]) == "FLOW_NORMAL"


def test_gate_flow_overflow_in_later_stream():
    assert monitor_gate_flow([[60], [51, 55]]) == "OVERFLOW"
