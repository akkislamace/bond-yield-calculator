"""
Bond Yield Calculator
=====================
Calculates:
  - Current Yield
  - Yield to Maturity (YTM) using iterative approximation
  - Yield to Call (YTC)

Data sources:
  - Manual input (this file)
  - Yahoo Finance via yfinance (pip install yfinance)
  - NSE/BSE India bonds: https://www.nseindia.com/market-data/bonds-traded-in-capital-market
  - US Treasury: https://home.treasury.gov/resource-center/data-chart-center/interest-rates
"""

# ── Standard library ─────────────────────────────────────────────────────────
from scipy.optimize import brentq   # pip install scipy


# ─────────────────────────────────────────────────────────────────────────────
# 1.  CORE FORMULAS
# ─────────────────────────────────────────────────────────────────────────────

def current_yield(coupon_rate: float, face_value: float, market_price: float) -> float:
    """
    Current Yield = Annual Coupon Payment / Market Price

    Args:
        coupon_rate  : Annual coupon rate as a decimal (e.g. 0.08 for 8%)
        face_value   : Par / face value of the bond (e.g. 1000)
        market_price : Current market price of the bond

    Returns:
        Current yield as a percentage
    """
    annual_coupon = coupon_rate * face_value
    return (annual_coupon / market_price) * 100


def yield_to_maturity(
    face_value: float,
    coupon_rate: float,
    market_price: float,
    years_to_maturity: float,
    frequency: int = 2,
) -> float:
    """
    Yield to Maturity (YTM) — solved numerically with Brent's method.

    Args:
        face_value        : Par value of the bond
        coupon_rate       : Annual coupon rate as a decimal
        market_price      : Current price paid for the bond
        years_to_maturity : Years remaining until the bond matures
        frequency         : Coupon payments per year (1=annual, 2=semi-annual)

    Returns:
        YTM as a percentage (annualised)
    """
    periods = int(years_to_maturity * frequency)
    coupon  = (coupon_rate * face_value) / frequency

    def price_from_ytm(ytm_per_period):
        """Return theoretical price given a YTM per period."""
        pv_coupons  = sum(coupon / (1 + ytm_per_period) ** t for t in range(1, periods + 1))
        pv_face     = face_value / (1 + ytm_per_period) ** periods
        return pv_coupons + pv_face

    # We want: price_from_ytm(r) - market_price = 0
    ytm_per_period = brentq(lambda r: price_from_ytm(r) - market_price, 1e-10, 10)
    return ytm_per_period * frequency * 100   # annualise and convert to %


def yield_to_call(
    face_value: float,
    coupon_rate: float,
    market_price: float,
    years_to_call: float,
    call_price: float,
    frequency: int = 2,
) -> float:
    """
    Yield to Call (YTC) — same logic as YTM but uses call price & call date.

    Args:
        face_value    : Par value of the bond
        coupon_rate   : Annual coupon rate as a decimal
        market_price  : Current price
        years_to_call : Years until the bond can be called
        call_price    : Price at which the issuer can call the bond
        frequency     : Coupon payments per year

    Returns:
        YTC as a percentage (annualised)
    """
    periods = int(years_to_call * frequency)
    coupon  = (coupon_rate * face_value) / frequency

    def price_from_ytc(ytc_per_period):
        pv_coupons = sum(coupon / (1 + ytc_per_period) ** t for t in range(1, periods + 1))
        pv_call    = call_price / (1 + ytc_per_period) ** periods
        return pv_coupons + pv_call

    ytc_per_period = brentq(lambda r: price_from_ytc(r) - market_price, 1e-10, 10)
    return ytc_per_period * frequency * 100


# ─────────────────────────────────────────────────────────────────────────────
# 2.  OPTIONAL: FETCH LIVE DATA WITH yfinance
# ─────────────────────────────────────────────────────────────────────────────
# Install: pip install yfinance
# Example tickers:
#   US 10-yr Treasury Yield : ^TNX
#   US 30-yr Treasury Yield : ^TYX
#   US 5-yr Treasury Yield  : ^FVX
#   Corporate bonds on NSE  : search on https://www.nseindia.com

def fetch_bond_price_yfinance(ticker: str) -> float:
    """
    Fetch the latest closing price for a bond/yield ticker via Yahoo Finance.

    Args:
        ticker : Yahoo Finance ticker symbol (e.g. '^TNX')

    Returns:
        Latest closing price / yield value
    """
    try:
        import yfinance as yf
        data  = yf.Ticker(ticker)
        price = data.history(period="1d")["Close"].iloc[-1]
        return float(price)
    except ImportError:
        print("yfinance not installed. Run: pip install yfinance")
        return None
    except Exception as e:
        print(f"Could not fetch data for {ticker}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# 3.  USER-FRIENDLY DISPLAY
# ─────────────────────────────────────────────────────────────────────────────

def display_results(
    face_value, coupon_rate, market_price,
    years_to_maturity, frequency,
    call_price=None, years_to_call=None,
):
    print("\n" + "=" * 50)
    print("         BOND YIELD CALCULATOR RESULTS")
    print("=" * 50)
    print(f"  Face Value       : ₹ / $ {face_value:,.2f}")
    print(f"  Coupon Rate      : {coupon_rate * 100:.2f}%")
    print(f"  Market Price     : ₹ / $ {market_price:,.2f}")
    print(f"  Years to Maturity: {years_to_maturity}")
    print(f"  Payment Frequency: {'Semi-annual' if frequency == 2 else 'Annual'}")
    print("-" * 50)

    cy  = current_yield(coupon_rate, face_value, market_price)
    ytm = yield_to_maturity(face_value, coupon_rate, market_price, years_to_maturity, frequency)

    print(f"  Current Yield    : {cy:.4f}%")
    print(f"  Yield to Maturity: {ytm:.4f}%")

    if call_price and years_to_call:
        ytc = yield_to_call(face_value, coupon_rate, market_price, years_to_call, call_price, frequency)
        print(f"  Yield to Call    : {ytc:.4f}%")
        print(f"  (Call Price: {call_price}, Years to Call: {years_to_call})")

    print("=" * 50 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# 4.  INTERACTIVE INPUT (run from terminal)
# ─────────────────────────────────────────────────────────────────────────────

def get_user_input():
    print("\n╔══════════════════════════════════╗")
    print("║     BOND YIELD CALCULATOR        ║")
    print("╚══════════════════════════════════╝\n")

    face_value        = float(input("Enter Face Value (e.g. 1000): "))
    coupon_rate       = float(input("Enter Annual Coupon Rate in % (e.g. 8 for 8%): ")) / 100
    market_price      = float(input("Enter Current Market Price (e.g. 950): "))
    years_to_maturity = float(input("Enter Years to Maturity (e.g. 5): "))
    freq_input        = input("Payment Frequency — enter 1 (Annual) or 2 (Semi-annual) [default 2]: ").strip()
    frequency         = int(freq_input) if freq_input in ("1", "2") else 2

    callable_input = input("Is this bond callable? (y/n) [default n]: ").strip().lower()
    call_price, years_to_call = None, None
    if callable_input == "y":
        call_price    = float(input("Enter Call Price (e.g. 1050): "))
        years_to_call = float(input("Enter Years to Call (e.g. 3): "))

    display_results(face_value, coupon_rate, market_price, years_to_maturity,
                    frequency, call_price, years_to_call)


# ─────────────────────────────────────────────────────────────────────────────
# 5.  DEMO — runs automatically if you execute this file
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n--- DEMO (hard-coded example) ---")
    # A ₹1000 bond, 8% coupon, bought at ₹950, 5 years left, semi-annual payments
    display_results(
        face_value        = 1000,
        coupon_rate       = 0.08,
        market_price      = 950,
        years_to_maturity = 5,
        frequency         = 2,
        call_price        = 1050,
        years_to_call     = 3,
    )

    print("\n--- INTERACTIVE MODE ---")
    get_user_input()
