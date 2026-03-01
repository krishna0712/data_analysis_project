# risk_engine.py

def detect_risks(monthly_kpi, product_kpi):

    risks = {}

    # Concentration risk
    risks["concentration_risk"] = bool(
        product_kpi["Revenue_%"].max() > 40
    )

    # Revenue decline streak
    decline = (monthly_kpi["Revenue"].diff() < 0)

    max_decline_streak = (
        decline.astype(int)
        .groupby((decline != decline.shift()).cumsum())
        .cumsum()
        .max()
    )

    risks["max_decline_streak"] = int(max_decline_streak)

    # Growth slowing
    risks["growth_slowing"] = bool(
        (monthly_kpi["Revenue_Growth_%"].diff() < 0).sum() >= 2
    )

    return risks