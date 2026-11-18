
from datetime import date, datetime
from zoneinfo import ZoneInfo

from fetchers.lbma_fetcher import fetch_lbma_fixings
from fetchers.jm_fetcher import fetch_jm_prices
from fetchers.ibja_fetcher import fetch_ibja_silver999
from fetchers.rbi_fetcher import fetch_rbi_exchange_rates


def _iso_date(value):
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def collect_rates(target_date: date) -> dict:
    rates = []

    def add_rate(metal, source, session, price, currency, unit, rate_date):
        actual_date = _iso_date(rate_date)

        if actual_date != target_date.isoformat():
            raise ValueError(
                f"{source} {metal}: expected {target_date}, "
                f"but received {actual_date}"
            )

        if price is None:
            raise ValueError(f"Missing price: {source} {metal}")

        rates.append({
            "metal": metal,
            "source": source,
            "session": session,
            "price": float(price),
            "currency": currency,
            "unit": unit,
            "rate_date": actual_date,
        })

    # 1. LBMA
    lbma = fetch_lbma_fixings(target_date)

    for session in ("AM", "PM"):
        for metal, price in lbma[session]["prices"].items():
            add_rate(
                metal, "LBMA", session, price,
                "USD", "troy_ounce",
                lbma[session]["dates"][metal]
            )

    # 2. Johnson Matthey
    jm_prices, jm_dates = fetch_jm_prices(target_date)

    for metal, price in jm_prices.items():
        add_rate(
            metal, "JM", "AM", price,
            "USD", "troy_ounce", jm_dates[metal]
        )

    # 3. IBJA
    ibja_prices, ibja_dates = fetch_ibja_silver999(target_date)

    for metal, price in ibja_prices.items():
        add_rate(
            metal, "IBJA", "AM" if metal.endswith("_AM") else "PM",
            price, "INR", "kg", ibja_dates[metal]
        )

    # 4. RBI
    rbi_prices, rbi_dates = fetch_rbi_exchange_rates(target_date)

    for currency_pair, price in rbi_prices.items():
        add_rate(
            currency_pair, "RBI", "DAILY", price,
            "INR", "per_currency_unit", rbi_dates[currency_pair]
        )

    return {
        "business_date": target_date.isoformat(),
        "generated_at": datetime.now(
            ZoneInfo("Asia/Kolkata")
        ).isoformat(),
        "timezone": "Asia/Kolkata",
        "status": "success",
        "rates": rates,
    }