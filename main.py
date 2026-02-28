# main.py

from data_loader import load_data
from kpi_engine import build_monthly_kpi, build_product_kpi
from risk_engine import detect_risks

def run_analysis(filepath):

    df = load_data(filepath)

    monthly_kpi = build_monthly_kpi(df)
    product_kpi = build_product_kpi(df)

    risks = detect_risks(monthly_kpi, product_kpi)

    print("\n===== RISK SUMMARY =====")
    print(risks)

    return monthly_kpi, product_kpi, risks


if __name__ == "__main__":
    run_analysis("sales_data.csv")