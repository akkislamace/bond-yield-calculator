"""
bond_yield_calculator.py

I made this to understand how bond yields work.
Covers current yield, YTM and YTC.
"""

from scipy.optimize import brentq


def current_yield(face_value, coupon_rate, market_price):
    coupon = coupon_rate * face_value
    return (coupon / market_price) * 100


def ytm(face_value, coupon_rate, market_price, years, freq=2):
    periods = int(years * freq)
    coupon = (coupon_rate * face_value) / freq

    def bond_price(r):
        pv = sum(coupon / (1 + r) ** t for t in range(1, periods + 1))
        pv += face_value / (1 + r) ** periods
        return pv

    rate = brentq(lambda r: bond_price(r) - market_price, 1e-9, 10)
    return rate * freq * 100


def ytc(face_value, coupon_rate, market_price, years_to_call, call_price, freq=2):
    periods = int(years_to_call * freq)
    coupon = (coupon_rate * face_value) / freq

    def bond_price(r):
        pv = sum(coupon / (1 + r) ** t for t in range(1, periods + 1))
        pv += call_price / (1 + r) ** periods
        return pv

    rate = brentq(lambda r: bond_price(r) - market_price, 1e-9, 10)
    return rate * freq * 100


def main():
    print("\n--- Bond Yield Calculator ---\n")

    face_value   = float(input("Face value (e.g. 1000): "))
    coupon_rate  = float(input("Coupon rate in % (e.g. 8): ")) / 100
    market_price = float(input("Market price (e.g. 950): "))
    years        = float(input("Years to maturity (e.g. 5): "))
    freq         = input("Payments per year — 1 or 2 [default 2]: ").strip()
    freq         = int(freq) if freq in ("1", "2") else 2

    cy      = current_yield(face_value, coupon_rate, market_price)
    ytm_val = ytm(face_value, coupon_rate, market_price, years, freq)

    print(f"\nCurrent Yield    : {cy:.2f}%")
    print(f"Yield to Maturity: {ytm_val:.2f}%")

    callable_bond = input("\nCallable bond? (y/n): ").strip().lower()
    if callable_bond == "y":
        call_price    = float(input("Call price: "))
        years_to_call = float(input("Years to call: "))
        ytc_val = ytc(face_value, coupon_rate, market_price, years_to_call, call_price, freq)
        print(f"Yield to Call    : {ytc_val:.2f}%")

    print()


if __name__ == "__main__":
    main()
