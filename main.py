# main.py
import pprint
from data_loader import load_data
from kpi_engine import build_monthly_kpi, build_product_kpi
from risk_engine import detect_risks
from summary_engine import generate_summary

def run_analysis(filepath):

    df = load_data(filepath)

    monthly_kpi, incomplete_last_month = build_monthly_kpi(df)
    product_kpi = build_product_kpi(df)

    risks = detect_risks(monthly_kpi, product_kpi)

    summary = generate_summary(monthly_kpi, product_kpi, risks, incomplete_last_month)

    print("\n===== STRUCTURED SUMMARY =====\n")

    print(summary)

    return monthly_kpi, product_kpi, risks, summary




if __name__ == "__main__":
    run_analysis("sales_data.csv")