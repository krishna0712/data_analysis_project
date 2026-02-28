# risk_engine.py

def detect_risks(monthly_kpi, product_kpi):

    risks = {}

    # Concentration risk
    risks["concentration_risk"] = (
        product_kpi["Revenue_%"].max() > 40
    )

    # Revenue decline streak
    monthly_kpi["Decline"] = (
        monthly_kpi["Revenue"].diff() < 0
    )

    max_decline_streak = (
        monthly_kpi["Decline"]
        .astype(int)
        .groupby(
            (monthly_kpi["Decline"] != 
             monthly_kpi["Decline"].shift()).cumsum()
        )
        .cumsum()
        .max()
    )

    risks["max_decline_streak"] = int(max_decline_streak)

    # Growth slowing
    risks["growth_slowing"] = (
        (monthly_kpi["Revenue_Growth_%"].diff() < 0)
        .sum() >= 2
    )

    return risks