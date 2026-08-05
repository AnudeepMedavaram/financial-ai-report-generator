import os
import json
from groq import Groq
from dotenv import load_dotenv
from schemas import Financials

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_financials(text: str) -> Financials:

    prompt = f"""
You are a professional equity research analyst.

Extract the following information from the financial report.

Return ONLY a valid JSON object.
Do not add explanations, markdown, or code fences.

Required JSON format:

{{
  "company_name": "",
  "quarter": "",
  "revenue": null,
  "net_profit": null,
  "operating_margin": null,
  "revenue_growth_yoy": null,
  "profit_growth_yoy": null,
  "highlights": ["", "", ""],
  "executive_summary": ""
}}

Financial report:
{text[:10000]}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=800
    )

    content = response.choices[0].message.content

    # Debug print
    print("\n=== RAW LLM OUTPUT ===\n")
    print(content)
    print("\n======================\n")

    if content is None or content.strip() == "":
        raise ValueError("LLM returned an empty response")

    content = content.strip()

    # Remove markdown fences if present
    content = content.replace("```json", "").replace("```", "").strip()

    data = json.loads(content)

    return Financials(**data)