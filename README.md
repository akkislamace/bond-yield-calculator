# 📈 Bond Yield Calculator

A Python command-line tool to calculate **Current Yield**, **Yield to Maturity (YTM)**, and **Yield to Call (YTC)** for bonds.

Built as a mini finance project to learn Python and financial concepts.

---

## 🚀 Features

- ✅ Current Yield
- ✅ Yield to Maturity (YTM) — solved numerically using Brent's method
- ✅ Yield to Call (YTC) — for callable bonds
- ✅ Optional: fetch live bond prices using `yfinance`
- ✅ Interactive terminal input

---

## 📦 Installation

```bash
pip install scipy yfinance
```

---

## ▶️ How to Run

```bash
python bond_yield_calculator.py
```

The demo runs first with a hardcoded example, then prompts you for your own bond details.

---

## 📊 Where to Get Bond Data

| Source | What You Get | Link |
|---|---|---|
| NSE India | Indian govt & corporate bonds | https://www.nseindia.com/market-data/bonds-traded-in-capital-market |
| BSE India | Bond listings | https://www.bseindia.com/markets/debt/debt_overview.aspx |
| RBI | Government securities (G-Secs) | https://www.rbi.org.in/Scripts/BS_ViewMasCirculardetails.aspx |
| Yahoo Finance | US Treasuries, bond ETFs | `^TNX` (10-yr), `^TYX` (30-yr) |
| Investing.com | Global bond yields | https://www.investing.com/rates-bonds |

---

## 🧮 Formulas Used

**Current Yield**
```
Current Yield = (Coupon Rate × Face Value) / Market Price
```

**Yield to Maturity** — solved by finding `r` such that:
```
Market Price = Σ [Coupon / (1+r)^t] + Face Value / (1+r)^n
```

**Yield to Call** — same as YTM but uses call price and call date.

---

## 📁 Project Structure

```
bond_yield_calculator.py   ← main file (all-in-one)
README.md                  ← this file
```

---

## 🛠️ Built With

- Python 3
- `scipy` — for numerical root-finding (Brent's method)
- `yfinance` — optional, for live data

---

## 👤 Author

Made by [Your Name] — first Python mini project!
