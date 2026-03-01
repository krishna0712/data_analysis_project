# main.py
from data_loader import load_data
from kpi_engine import build_monthly_kpi, build_product_kpi
from risk_engine import detect_risks
from summary_engine import generate_summary
from visualization_engine import (
    plot_revenue_growth,
    plot_revenue_trend,
    plot_top_products
)

def run_analysis(filepath):

    df = load_data(filepath)

    monthly_kpi, incomplete_last_month = build_monthly_kpi(df)
    product_kpi = build_product_kpi(df)

    risks = detect_risks(monthly_kpi, product_kpi)

    summary = generate_summary(monthly_kpi, product_kpi, risks, incomplete_last_month)

    plot_revenue_trend(monthly_kpi)
    plot_revenue_growth(monthly_kpi)
    plot_top_products(product_kpi)
    print("\n===== STRUCTURED SUMMARY =====\n")

    print(summary)

    return monthly_kpi, product_kpi, risks, summary




if __name__ == "__main__":
    run_analysis("sales_data.csv")