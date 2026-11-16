import pytest
from hypothesis import given, strategies as st

from processor import (
    calculate_seat_tier_price,
    decode_promo_voucher,
    parse_attendee_badge,
)


@given(st.text() | st.none())
def test_decode_promo_voucher_no_crash(s):
    try:
        decode_promo_voucher(s)
    except Exception as exc:
        pytest.fail(f"decode_promo_voucher crashed with {exc!r} for input {s!r}")


@given(st.text() | st.none())
def test_calculate_seat_tier_price_safe(s):
    try:
        calculate_seat_tier_price(s)
    except Exception as exc:
        pytest.fail(
            f"calculate_seat_tier_price crashed with {exc!r} for input {s!r}"
        )


@given(st.text() | st.none())
def test_parse_attendee_badge_safe(s):
    try:
        parse_attendee_badge(s)
    except Exception as exc:
        pytest.fail(f"parse_attendee_badge crashed with {exc!r} for input {s!r}")


def test_valid_inputs():
    assert decode_promo_voucher("EARLY-20") == "Valid EARLY: 20% OFF"
    assert calculate_seat_tier_price("VIP@4") == 158.0
    assert parse_attendee_badge("Alex,17,A1") == "Alex [Child] - Seat A1"


def test_invalid_inputs_are_handled():
    assert decode_promo_voucher(None) == "Invalid voucher"
    assert decode_promo_voucher("EARLY-120") == "Invalid voucher"
    assert calculate_seat_tier_price("UNKNOWN@2") == "Invalid seat specification"
    assert parse_attendee_badge("Alex,not-a-number,A1") == "Invalid attendee badge"