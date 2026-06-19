from pydantic import BaseModel


class LeadCreate(BaseModel):
    company_name: str
    company_size: int
    industry: str
    job_title: str
    pricing_page_views: int
    email_opens: int

    estimated_deal_value: float

    sales_stage: str

    region: str


class LeadResponse(LeadCreate):
    id: int
    score: float
    tier: str

    class Config:
        from_attributes = True


class ScenarioRequest(BaseModel):
    marketing_increase_percent: float