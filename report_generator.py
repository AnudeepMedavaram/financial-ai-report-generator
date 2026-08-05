from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from charts import create_revenue_chart


def safe_value(value):
    if value is None:
        return "Not available in source document"
    return str(value)


def detect_sector(company_name: str) -> str:
    name = (company_name or "").lower()

    if "energy" in name or "power" in name:
        return "Power / Utilities"
    if "bank" in name or "finance" in name:
        return "Banking & Financial Services"
    if "steel" in name or "metal" in name or "oxide" in name:
        return "Metals & Recycling"

    return "Diversified"


def section_heading(text, styles):
    return Table(
        [[Paragraph(f"<font color='white'><b>{text}</b></font>", styles["BodyText"])]],
        colWidths=[500],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1F4E78")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#1F4E78")),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]),
    )


def generate_pdf_report(financials, output_path="generated_report.pdf"):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()
    elements = []

    company_name = financials.company_name or "Company"
    sector = detect_sector(company_name)
    quarter = financials.quarter or "Quarter not available"

    # =========================================================
    # Broker Header
    # =========================================================
    broker = Table(
        [["Geojit Financial Services - Equity Research"]],
        colWidths=[500],
    )

    broker.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(broker)
    elements.append(Spacer(1, 14))

    # =========================================================
    # Company Title
    # =========================================================
    elements.append(
        Paragraph(
            f"<font size=20><b>{company_name}</b></font>",
            styles["BodyText"],
        )
    )
    elements.append(Spacer(1, 8))

    # =========================================================
    # Research Metadata Table
    # =========================================================
    meta = [
        ["Quarter", quarter, "Date", "17-Oct-2025"],
        ["Sector", sector, "Rating", "HOLD"],
        ["Target", "Not available", "Return", "Not available"],
    ]

    meta_table = Table(meta, colWidths=[90, 160, 90, 160])

    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F5")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(meta_table)
    elements.append(Spacer(1, 14))

    # =========================================================
    # Investment Thesis
    # =========================================================
    headline = (
        financials.executive_summary
        or "Operational performance remains stable with improving business visibility."
    )

    elements.append(
        Paragraph(f"<b>{headline}</b>", styles["Heading2"])
    )
    elements.append(Spacer(1, 12))

    # =========================================================
    # Investment Rationale
    # =========================================================
    elements.append(section_heading("Investment Rationale", styles))
    elements.append(Spacer(1, 8))

    rationale = financials.executive_summary or "Detailed rationale not available."
    elements.append(Paragraph(rationale, styles["BodyText"]))
    elements.append(Spacer(1, 20))

    # =========================================================
    # Key Financials
    # =========================================================
    elements.append(section_heading("Key Financials", styles))
    elements.append(Spacer(1, 8))

    data = [
        ["Metric", "Value"],
        ["Revenue", safe_value(financials.revenue)],
        ["Net Profit", safe_value(financials.net_profit)],
        ["Operating Margin", safe_value(financials.operating_margin)],
        ["Revenue Growth YoY", safe_value(financials.revenue_growth_yoy)],
        ["Profit Growth YoY", safe_value(financials.profit_growth_yoy)],
    ]

    table = Table(data, colWidths=[250, 250])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 18))

    # =========================================================
    # Valuation Snapshot
    # =========================================================
    elements.append(section_heading("Valuation Snapshot", styles))
    elements.append(Spacer(1, 8))

    valuation = [
        ["Metric", "Value"],
        ["CMP", "Not available"],
        ["Target Price", "Not available"],
        ["P/E", "Not available"],
        ["EV/EBITDA", "Not available"],
    ]

    val_table = Table(valuation, colWidths=[250, 250])

    val_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.75, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(val_table)
    elements.append(Spacer(1, 20))

    # =========================================================
    # Revenue Chart
    # =========================================================
    elements.append(section_heading("Revenue Trend", styles))
    elements.append(Spacer(1, 8))

    chart_path = create_revenue_chart()

    elements.append(Image(chart_path, width=420, height=240))
    elements.append(Spacer(1, 20))

    # =========================================================
    # Key Highlights
    # =========================================================
    elements.append(section_heading("Key Highlights", styles))
    elements.append(Spacer(1, 8))

    if financials.highlights:
        highlight_rows = [
            [Paragraph(f"• {h}", styles["BodyText"])]
            for h in financials.highlights
        ]
    else:
        highlight_rows = [[Paragraph("No highlights available.", styles["BodyText"])]]

    highlight_table = Table(highlight_rows, colWidths=[500])

    highlight_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF5FB")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#B7C9E2")),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(highlight_table)
    elements.append(Spacer(1, 20))

    # =========================================================
    # Risks & Outlook
    # =========================================================
    elements.append(section_heading("Risks & Outlook", styles))
    elements.append(Spacer(1, 8))

    risk_text = (
        "Key monitorables include commodity price volatility, demand conditions, working capital "
        "requirements, and execution of expansion projects. Sustained operational efficiency remains "
        "important for earnings visibility."
    )

    elements.append(Paragraph(risk_text, styles["BodyText"]))
    elements.append(Spacer(1, 20))

    # =========================================================
    # Recommendation History
    # =========================================================
    elements.append(section_heading("Recommendation Summary", styles))
    elements.append(Spacer(1, 8))

    rec_data = [
        ["Date", "Rating", "Target"],
        ["29-Jul-2025", "HOLD", "337"],
        ["30-Jan-2025", "BUY", "254"],
        ["28-Oct-2024", "BUY", "284"],
    ]

    rec_table = Table(rec_data, colWidths=[170, 170, 160])

    rec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(rec_table)
    elements.append(Spacer(1, 20))

    # =========================================================
    # Disclaimer
    # =========================================================
    elements.append(section_heading("Disclaimer", styles))
    elements.append(Spacer(1, 8))

    disclaimer = (
        "This report was generated automatically using AI-based document analysis. The information is intended "
        "for demonstration purposes and should not be considered investment advice. Financial figures may be "
        "unavailable if not clearly present in the source document."
    )

    disc = Table(
        [[Paragraph(disclaimer, styles["BodyText"])]],
        colWidths=[500],
    )

    disc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F2F2")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(disc)

    # =========================================================
    # Disclosure Page
    # =========================================================
    elements.append(PageBreak())

    elements.append(Paragraph("<b>DISCLAIMER & DISCLOSURES</b>", styles["Heading2"]))
    elements.append(Spacer(1, 12))

    disclosure_text = (
        "This document is an AI-generated demonstration report prepared for technical evaluation purposes. "
        "It is not an official research publication and should not be used for investment decisions. "
        "Users should independently verify all financial information before acting on it."
    )

    elements.append(Paragraph(disclosure_text, styles["BodyText"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>Prepared using:</b> Python, Streamlit, Groq LLM, ReportLab", styles["BodyText"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph("<b>Generated by:</b> Financial AI Report Generator", styles["BodyText"]))

    # Build PDF
    doc.build(elements)

    return output_path