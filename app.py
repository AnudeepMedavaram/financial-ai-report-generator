from pathlib import Path
import json
import streamlit as st

from extractor import extract_pdf_text
from llm_extractor import extract_financials
from report_generator import generate_pdf_report

# Page config (must come before any Streamlit widgets)
st.set_page_config(page_title="Financial AI Report Generator", layout="wide")

# Title
st.title("📊 Financial AI Report Generator")
st.write("Upload a company financial PDF or TXT file and generate an AI-powered analyst report.")

# Company name input
company_input = st.text_input(
    "Company Name (Optional)",
    placeholder="Enter company name"
)

# File upload
uploaded_file = st.file_uploader(
    "Upload Financial Document",
    type=["pdf", "txt"]
)

if uploaded_file is not None:

    # Extract text
    with st.spinner("Extracting text from document..."):

        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode("utf-8")
        else:
            text = extract_pdf_text(uploaded_file)

    st.success("Document processed successfully!")

    # Preview
    st.subheader("📄 Extracted Text Preview")
    st.text_area("Preview", value=text[:2000], height=250)

    # Analyze button
    if st.button("🤖 Analyze Financial Report"):

        with st.spinner("Analyzing financial report with AI..."):
            financials = extract_financials(text)

        # Override company name if user entered one
        if company_input.strip():
            financials.company_name = company_input.strip()

        st.success("AI analysis completed!")

        # Metrics section
        st.header("📌 Company Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Company", financials.company_name or "N/A")
            st.metric("Quarter", financials.quarter or "N/A")
            st.metric("Revenue", financials.revenue or "N/A")

        with col2:
            st.metric("Net Profit", financials.net_profit or "N/A")
            st.metric("Operating Margin", financials.operating_margin or "N/A")
            st.metric("Revenue Growth YoY", financials.revenue_growth_yoy or "N/A")

        # Executive summary
        st.header("📝 Executive Summary")

        if financials.executive_summary:
            st.write(financials.executive_summary)
        else:
            st.write("Summary not available.")

        # Highlights
        st.header("⭐ Key Highlights")

        if financials.highlights:
            for item in financials.highlights:
                st.write(f"• {item}")
        else:
            st.write("No highlights available.")

        # Raw JSON
        st.header("🔍 Structured Financial Output")
        st.json(financials.model_dump())

        # Save JSON
        Path("outputs").mkdir(exist_ok=True)

        company_slug = (
            (financials.company_name or "company")
            .replace(" ", "_")
            .replace("/", "_")
        )

        json_path = Path(f"outputs/{company_slug}_financials.json")

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                financials.model_dump(),
                f,
                indent=2,
                ensure_ascii=False
            )

        st.success(f"💾 Saved structured data to {json_path}")

        # Download JSON button
        with open(json_path, "rb") as f:
            st.download_button(
                label="⬇ Download JSON Output",
                data=f,
                file_name=json_path.name,
                mime="application/json"
            )

        # Generate PDF
        Path("reports").mkdir(exist_ok=True)

        pdf_path = Path(f"reports/{company_slug}_report.pdf")

        generate_pdf_report(financials, str(pdf_path))

        st.success("📄 PDF report generated successfully!")

        # Download PDF button
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇ Download Analyst Report PDF",
                data=f,
                file_name=pdf_path.name,
                mime="application/pdf"
            )   