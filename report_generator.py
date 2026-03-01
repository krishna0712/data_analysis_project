# report_generator.py

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(summary, output_filename="Business_Report.pdf"):

    doc = SimpleDocTemplate(output_filename)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    heading_style = styles["Heading1"]

    # Title
    elements.append(Paragraph("Business Performance Report", heading_style))
    elements.append(Spacer(1, 0.3 * inch))

    # KPI Section
    elements.append(Paragraph("Key Performance Indicators", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    for key, value in summary["kpis"].items():
        elements.append(
            Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", normal_style)
        )
        elements.append(Spacer(1, 0.1 * inch))

    elements.append(Spacer(1, 0.3 * inch))

    # Risk Section
    elements.append(Paragraph("Risk Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    risk_list = [
        ListItem(Paragraph(risk, normal_style))
        for risk in summary["risks"]
    ]

    elements.append(ListFlowable(risk_list, bulletType="bullet"))
    elements.append(Spacer(1, 0.3 * inch))

    # Action Section
    elements.append(Paragraph("Recommended Actions", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    action_list = [
        ListItem(Paragraph(action, normal_style))
        for action in summary["actions"]
    ]

    elements.append(ListFlowable(action_list, bulletType="bullet"))
    elements.append(Spacer(1, 0.5 * inch))

    # Add Charts
    elements.append(Paragraph("Revenue Trend", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image("revenue_trend.png", width=6 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("Revenue Growth", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image("revenue_growth.png", width=6 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.4 * inch))

    elements.append(Paragraph("Top Products", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image("top_products.png", width=6 * inch, height=3 * inch))

    doc.build(elements)