# report_generator.py

import base64
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def _encode_image(path: str) -> str:
    """Encode a PNG file to base64 string for embedding in HTML."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _fmt_currency(value: float) -> str:
    """Format a float as a readable currency string."""
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:.2f}"


def _fmt_pct(value: float) -> str:
    """Format a float as a percentage string with sign."""
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def generate_pdf_report(
    summary: dict,
    monthly_kpi,
    product_kpi,
    output_filename: str = "Business_Report.pdf",
    company_name: str = "Acme Corp",
    chart_paths: dict = None,
    templates_dir: str = None,
):
    # ── Defaults ──────────────────────────────────────────────
    if chart_paths is None:
        chart_paths = {
            "revenue_trend": "revenue_trend.png",
            "revenue_growth": "revenue_growth.png",
            "top_products":   "top_products.png",
        }

    if templates_dir is None:
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    # ── Validate chart files exist ─────────────────────────────
    for key, path in chart_paths.items():
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Chart file missing: '{path}'. "
                f"Run visualization_engine first to generate all charts."
            )

    # ── Encode charts as base64 ───────────────────────────────
    charts = {key: _encode_image(path) for key, path in chart_paths.items()}

    # ── KPI context ───────────────────────────────────────────
    raw = summary["kpis"]
    kpis = {
        "latest_month":       str(raw["latest_month"]),
        "total_revenue":      _fmt_currency(raw["total_revenue"]),
        "revenue_growth_pct": _fmt_pct(raw["revenue_growth_pct"]),
        "revenue_growth_raw": raw["revenue_growth_pct"],
        "total_orders":       f"{raw['total_orders']:,}",
        "order_growth_pct":   _fmt_pct(raw["order_growth_pct"]),
        "order_growth_raw":   raw["order_growth_pct"],
        "avg_order_value":    f"${raw['average_order_value']:.2f}",
    }

    # ── Period label ──────────────────────────────────────────
    months = monthly_kpi["Year_Month"].astype(str).tolist()
    period = f"{months[0]}  →  {months[-1]}"

    # ── Executive summary ─────────────────────────────────────
    rev_dir = "grew" if raw["revenue_growth_pct"] >= 0 else "declined"
    executive_summary = (
        f"In {kpis['latest_month']}, the business generated {kpis['total_revenue']} in revenue, "
        f"which {rev_dir} by {kpis['revenue_growth_pct']} compared to the prior month. "
        f"A total of {kpis['total_orders']} orders were processed at an average value of "
        f"{kpis['avg_order_value']}. "
        f"{'Revenue is well distributed across products with no concentration risk. ' if not any('highly dependent' in r for r in summary['risks']) else 'Revenue concentration risk has been identified. '}"
        f"Detailed risk analysis and recommended actions are provided on page 3."
    )

    # ── Monthly table rows ─────────────────────────────────────
    monthly_table = []
    for _, row in monthly_kpi.iterrows():
        rg = row["Revenue_Growth_%"]
        og = row["Order_Growth_%"]
        monthly_table.append({
            "month":           str(row["Year_Month"]),
            "revenue":         _fmt_currency(row["Revenue"]),
            "orders":          f"{int(row['Total_Orders']):,}",
            "aov":             f"${row['Average_Order_Value']:.2f}",
            "rev_growth":      _fmt_pct(rg) if str(rg) != "nan" else "—",
            "rev_growth_raw":  rg if str(rg) != "nan" else None,
            "order_growth":    _fmt_pct(og) if str(og) != "nan" else "—",
            "order_growth_raw": og if str(og) != "nan" else None,
        })

    # ── Render template ───────────────────────────────────────
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("report.html")

    html_content = template.render(
        company_name=company_name,
        period=period,
        kpis=kpis,
        executive_summary=executive_summary,
        charts=charts,
        risks=summary["risks"],
        actions=summary["actions"],
        monthly_table=monthly_table,
    )

    # ── Convert to PDF ────────────────────────────────────────
    HTML(string=html_content, base_url=".").write_pdf(output_filename)
    print(f"Report saved → {output_filename}")