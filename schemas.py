from typing import Optional, List
from pydantic import BaseModel


class Financials(BaseModel):
    company_name: Optional[str] = None
    quarter: Optional[str] = None

    # Allow both numbers and text
    revenue: Optional[str | float | int] = None
    net_profit: Optional[str | float | int] = None
    operating_margin: Optional[str | float | int] = None
    revenue_growth_yoy: Optional[str | float | int] = None
    profit_growth_yoy: Optional[str | float | int] = None

    executive_summary: Optional[str] = None
    highlights: List[str] = []