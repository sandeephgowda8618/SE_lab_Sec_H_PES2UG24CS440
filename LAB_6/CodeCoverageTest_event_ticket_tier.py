import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def test_invalid_manifests_type():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_vip_premium_and_general_tiers():
    manifests = [
        {"is_confirmed": True, "tier": "vip",
         "orders": [{"qty": 1, "promo": ""}]},
        {"is_confirmed": True, "tier": "premium",
         "orders": [{"qty": 1, "promo": ""}]},
        {"is_confirmed": True, "tier": "general",
         "orders": [{"qty": 1, "promo": ""}]},
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 285.0, "status": "COMPLETED"}


def test_unconfirmed_and_unknown_tier():
    manifests = [
        {"is_confirmed": False, "tier": "vip",
         "orders": [{"qty": 2}]},
        {"is_confirmed": True, "tier": "student",
         "orders": [{"qty": 1}]},
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_default_tier_and_default_orders():
    result = process_ticket_manifest(
        [{"is_confirmed": True}], 0
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_earlybird_promotion_and_service_tax():
    manifests = [
        {"is_confirmed": True, "tier": "premium",
         "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 158.4, "status": "COMPLETED"}


def test_bulk_order_discount():
    manifests = [
        {"is_confirmed": True, "tier": "general",
         "orders": [{"qty": 5, "promo": ""}]}
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 205.0, "status": "COMPLETED"}


def test_nonpositive_quantities_are_rejected():
    manifests = [
        {"is_confirmed": True, "tier": "general",
         "orders": [{"qty": 0}, {"qty": -1}]}
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_fraud_promo_on_non_vip_order():
    manifests = [
        {"is_confirmed": True, "tier": "general",
         "orders": [{"qty": 1, "promo": "FRAUD_RISK"}]}
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 45.0, "status": "COMPLETED"}


def test_vip_fraud_resets_manifest_total():
    manifests = [
        {"is_confirmed": True, "tier": "vip",
         "exclusive_lounge": False,
         "orders": [
             {"qty": 1, "promo": ""},
             {"qty": 1, "promo": "FRAUD_RISK"},
             {"qty": 1, "promo": ""},
         ]}
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_exclusive_lounge_fee():
    manifests = [
        {"is_confirmed": True, "tier": "general",
         "exclusive_lounge": True,
         "orders": [{"qty": 1, "promo": ""}]}
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {"total_revenue": 120.0, "status": "COMPLETED"}


def test_audit_rejected_after_more_than_four_rejections():
    manifests = [
        {"is_confirmed": True, "tier": "unknown"}
        for _ in range(5)
    ]
    result = process_ticket_manifest(manifests, 0)
    assert result == {
        "total_revenue": 0.0,
        "status": "AUDIT_REJECTED",
    }


def test_gate_flow_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_flow_normal_and_congestion_reset():
    assert monitor_gate_flow([[51, 40, 51], [10, 20]]) == "FLOW_NORMAL"


def test_gate_flow_overflow():
    assert monitor_gate_flow([[51, 52]]) == "OVERFLOW"
