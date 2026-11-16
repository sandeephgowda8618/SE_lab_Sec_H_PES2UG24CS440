import pytest
from hypothesis import given, strategies as st

from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


@given(
    manifests=st.one_of(
        st.none(),
        st.integers(),
        st.text(),
        st.lists(
            st.one_of(
                st.none(),
                st.integers(),
                st.text(),
                st.dictionaries(st.text(), st.integers()),
            ),
            max_size=10,
        ),
    ),
    tax_rate=st.one_of(st.none(), st.text(), st.integers(), st.floats(allow_nan=True)),
)
def test_process_ticket_manifest_handles_unexpected_inputs(manifests, tax_rate):
    if isinstance(manifests, list) and isinstance(tax_rate, (int, float)) and not isinstance(tax_rate, bool):
        try:
            process_ticket_manifest(manifests, tax_rate)
        except (ValueError, OverflowError, TypeError):
            pass
    else:
        with pytest.raises(ValueError):
            process_ticket_manifest(manifests, tax_rate)


@given(
    streams=st.one_of(
        st.none(),
        st.integers(),
        st.text(),
        st.lists(
            st.one_of(
                st.none(),
                st.integers(),
                st.text(),
                st.lists(st.one_of(st.none(), st.integers(), st.floats(allow_nan=True)), max_size=10),
            ),
            max_size=10,
        ),
    )
)
def test_monitor_gate_flow_handles_unexpected_inputs(streams):
    result = monitor_gate_flow(streams)
    assert result in {"NO_DATA", "FLOW_NORMAL", "OVERFLOW"}


def test_single_general_order():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "exclusive_lounge": False,
            "orders": [{"qty": 2, "promo": ""}],
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 99.0, "status": "COMPLETED"}


def test_empty_manifest_list():
    assert process_ticket_manifest([], 0.1) == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES",
    }


def test_confirmed_vip_with_fraud_order_is_rejected():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "vip",
            "orders": [{"qty": 1, "promo": "FRAUD_RISK"}],
        }
    ]
    assert process_ticket_manifest(manifests, 0) == {
        "total_revenue": 0.0,
        "status": "ZERO_SALES",
    }


def test_many_rejected_orders_trigger_audit():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [
                {"qty": 0},
                {"qty": -1},
                {"qty": "invalid"},
                None,
                {"qty": 1, "promo": 123},
            ],
        }
    ]
    assert process_ticket_manifest(manifests, 0)["status"] == "AUDIT_REJECTED"


def test_earlybird_discount_and_lounge_fee():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "premium",
            "exclusive_lounge": True,
            "orders": [{"qty": 2, "promo": "EARLYBIRD"}],
        }
    ]
    assert process_ticket_manifest(manifests, 0) == {
        "total_revenue": 219.0,
        "status": "COMPLETED",
    }


def test_large_order_discount():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "orders": [{"qty": 5, "promo": ""}],
        }
    ]
    assert process_ticket_manifest(manifests, 0) == {
        "total_revenue": 205.0,
        "status": "COMPLETED",
    }


def test_invalid_tax_rate_raises_value_error():
    with pytest.raises(ValueError):
        process_ticket_manifest([], float("nan"))


def test_gate_flow_results():
    assert monitor_gate_flow([]) == "NO_DATA"
    assert monitor_gate_flow([[10, 20, 30]]) == "FLOW_NORMAL"
    assert monitor_gate_flow([[51, 52]]) == "OVERFLOW"
    assert monitor_gate_flow([[51, 50, 52]]) == "FLOW_NORMAL"
