import math


def decode_promo_voucher(voucher_code):
    if not isinstance(voucher_code, str):
        return "Invalid voucher"

    parts = voucher_code.strip().split("-")
    if len(parts) != 2:
        return "Invalid voucher"

    prefix, pct_str = (part.strip() for part in parts)

    if not prefix or not pct_str or not pct_str.isdecimal():
        return "Invalid voucher"

    percentage = int(pct_str)
    if not 1 <= percentage <= 100:
        return "Invalid voucher"

    return f"Valid {prefix.upper()}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    if not isinstance(tier_spec, str):
        return "Invalid seat specification"

    parts = tier_spec.split("@")
    if len(parts) != 2:
        return "Invalid seat specification"

    tier = parts[0].strip().upper()
    row_text = parts[1].strip()

    tier_rates = {
        "VIP": 150.0,
        "PREMIUM": 90.0,
        "GENERAL": 45.0,
    }

    if tier not in tier_rates or not row_text.isdecimal():
        return "Invalid seat specification"

    row = int(row_text)
    if row < 1:
        return "Invalid seat specification"

    return tier_rates[tier] + (row * 2.0)


def parse_attendee_badge(badge_csv):
    if not isinstance(badge_csv, str):
        return "Invalid attendee badge"

    tokens = badge_csv.split(",")
    if len(tokens) != 3:
        return "Invalid attendee badge"

    name = tokens[0].strip()
    age_text = tokens[1].strip()
    seat = tokens[2].strip()

    if not name or not seat or not age_text.isdecimal():
        return "Invalid attendee badge"

    age = int(age_text)
    category = "Child" if age < 18 else "Adult"

    return f"{name} [{category}] - Seat {seat}"


def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    print("Seat Price:", calculate_seat_tier_price(t_input))

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))


if __name__ == "__main__":
    main()