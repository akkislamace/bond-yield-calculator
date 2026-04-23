# Bond Yield Calculator

A small Python project I built while learning about bonds and fixed income.

Takes bond details as input and calculates:
- Current Yield
- Yield to Maturity (YTM)
- Yield to Call (YTC) — optional, for callable bonds

## How to run

Install the dependency first:
```
pip install scipy
```

Then run:
```
python bond_yield_calculator.py
```

It'll ask for face value, coupon rate, market price, and maturity — you can find these on NSE or BSE for any listed bond.

## Example

```
Face value: 1000
Coupon rate: 8
Market price: 950
Years to maturity: 5

Current Yield    : 8.42%
Yield to Maturity: 9.35%
```

## What I learned

- How YTM is not just the coupon rate — it accounts for the price difference too
- Why bonds trading below face value have a higher YTM
- Numerical methods (Brent's) are used to solve YTM since there's no closed-form formula

---
*First mini project — more to come.*
