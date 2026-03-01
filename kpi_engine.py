# kpi_engine.py

import pandas as pd

def build_monthly_kpi(df: pd.DataFrame) -> pd.DataFrame:

    monthly_kpi = df.groupby("Year_Month").agg({
        "Revenue": "sum",
        "Quantity": "sum",
        "Order ID": "nunique"
    }).reset_index()

    monthly_kpi.rename(columns={
        "Order ID": "Total_Orders"
    }, inplace=True)

    monthly_kpi["Average_Order_Value"] = (
        round(monthly_kpi["Revenue"] / monthly_kpi["Total_Orders"],2)
    )

    monthly_kpi["Revenue_Growth_%"] = (
        round(monthly_kpi["Revenue"].pct_change() * 100,2)
    )

    monthly_kpi["Order_Growth_%"] = (
        round(monthly_kpi["Total_Orders"].pct_change() * 100,3)
    )

    last_date = df["Date"].max()
    last_month_end = last_date.to_period("M").to_timestamp("M")
    incomplete_last_month = last_date < last_month_end

    return monthly_kpi, incomplete_last_month


def build_product_kpi(df: pd.DataFrame) -> pd.DataFrame:

    product_kpi = df.groupby("Product").agg({
        "Revenue": "sum",
        "Quantity": "sum",
        "Order ID": "nunique"
    }).reset_index()

    product_kpi.rename(columns={
        "Order ID": "Total_Orders"
    }, inplace=True)

    product_kpi = product_kpi.sort_values("Revenue", ascending=False)

    total_revenue = product_kpi["Revenue"].sum()

    product_kpi["Revenue_%"] = (
        product_kpi["Revenue"] / total_revenue * 100
    )

    return product_kpi