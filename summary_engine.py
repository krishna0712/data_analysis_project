# summary_engine.py

def generate_summary(monthly_kpi, product_kpi, risks, incomplete_last_month,as_dict=False):

    latest = monthly_kpi.iloc[-1]
    latest_month = str(latest["Year_Month"])

    # ===== KPI SECTION =====
    kpis = {
        "latest_month": latest_month,
        "total_revenue": float(latest["Revenue"]),
        "revenue_growth_pct": float(latest["Revenue_Growth_%"]),
        "total_orders": int(latest["Total_Orders"]),
        "order_growth_pct": float(latest["Order_Growth_%"]),
        "average_order_value": float(latest["Average_Order_Value"])
    }

    # ===== RISK SECTION =====
    risk_points = []

    if risks["growth_slowing"]:
        risk_points.append("Revenue growth momentum is slowing down.")

    if risks["max_decline_streak"] >= 2:
        risk_points.append(
            f"Revenue declined for {risks['max_decline_streak']} consecutive months earlier."
        )

    if risks["concentration_risk"]:
        risk_points.append(
            "Revenue is highly dependent on one product."
        )
    else:
        risk_points.append(
            "Revenue is well distributed across products."
        )

    if incomplete_last_month:
        risk_points.append(
            "Latest month data may be incomplete, interpret with caution."
        )

    # ===== ACTION SECTION =====
    action_points = []

    if risks["growth_slowing"]:
        action_points.append(
            "Focus on boosting demand through marketing or expansion."
        )

    if risks["max_decline_streak"] >= 2:
        action_points.append(
            "Investigate causes of previous decline and stabilize revenue."
        )

    if not risks["concentration_risk"]:
        action_points.append(
            "Maintain diversified product strategy."
        )

    # ===== FORMATTED SUMMARY STRING =====
    summary_str = "===== KPI SUMMARY =====\n\n"
    for key, value in kpis.items():
        if key in ["revenue_growth_pct", "order_growth_pct"]:
            summary_str += f"{key}: {value}%\n"
        elif key in ["total_revenue"]:
            summary_str += f"{key}: ₹{value}\n"
        else:
            summary_str += f"{key}: {value}\n"

    summary_str += "\n===== RISK SUMMARY =====\n"
    for risk in risk_points:
        summary_str += f"- {risk}\n"

    summary_str += "\n===== ACTIONS =====\n"
    for action in action_points:
        summary_str += f"- {action}\n"

    if as_dict:
        return {
            "kpis": kpis,
            "risks": risk_points,
            "actions": action_points
        }
    else:
        # return formatted string as before
        return summary_str