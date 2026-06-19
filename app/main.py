from .ai_brief import generate_sales_brief
from fastapi import FastAPI
from sqlalchemy.orm import Session

from .database import engine
from .database import SessionLocal

from . import models
from . import schemas

from .scoring import calculate_score
from sqlalchemy import func
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RevenueIQ AI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "status": "healthy",
        "service": "RevenueIQ AI"
    }


@app.post("/leads")
def create_lead(
    lead: schemas.LeadCreate
):

    db: Session = SessionLocal()

    try:

        score, tier = calculate_score(lead)

        new_lead = models.Lead(
    company_name=lead.company_name,
    company_size=lead.company_size,
    industry=lead.industry,
    job_title=lead.job_title,
    pricing_page_views=lead.pricing_page_views,
    email_opens=lead.email_opens,

    estimated_deal_value=lead.estimated_deal_value,
    sales_stage=lead.sales_stage,
    region=lead.region,

    score=score,
    tier=tier
    )

        db.add(new_lead)

        db.commit()

        db.refresh(new_lead)

        return new_lead

    finally:
        db.close()


@app.get("/leads")
def get_leads():

    db: Session = SessionLocal()

    try:

        leads = db.query(
            models.Lead
        ).all()

        return leads

    finally:
        db.close()


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
@app.get("/model-info")
def model_info():

    return {
        "model": "Logistic Regression",
        "training_rows": 10000,
        "status": "active"
    }
@app.get("/sales-brief/{lead_id}")
def sales_brief(lead_id: int):

    db = SessionLocal()

    try:

        lead = db.query(
            models.Lead
        ).filter(
            models.Lead.id == lead_id
        ).first()

        if not lead:

            return {
                "error": "Lead not found"
            }

        brief = generate_sales_brief(lead)

        return {
            "lead_id": lead.id,
            "company_name": lead.company_name,
            "score": lead.score,
            "tier": lead.tier,
            "brief": brief
        }

    finally:
        db.close()


@app.get("/dashboard")
def dashboard():

    db = SessionLocal()

    try:

        all_leads = db.query(models.Lead).all()

        total_leads = len(all_leads)

        hot_leads = len(
            [lead for lead in all_leads if lead.tier == "HOT"]
        )

        warm_leads = len(
            [lead for lead in all_leads if lead.tier == "WARM"]
        )

        cold_leads = len(
            [lead for lead in all_leads if lead.tier == "COLD"]
        )

        pipeline_value = sum(
            lead.estimated_deal_value
            for lead in all_leads
        )

        forecast_revenue = sum(
            (lead.score / 100)
            * lead.estimated_deal_value
            for lead in all_leads
        )

        return {
            "total_leads": total_leads,
            "hot_leads": hot_leads,
            "warm_leads": warm_leads,
            "cold_leads": cold_leads,
            "pipeline_value": round(
                pipeline_value,
                2
            ),
            "forecast_revenue": round(
                forecast_revenue,
                2
            )
        }

    finally:
        db.close()

@app.get("/strategy-insights")
def strategy_insights():

    db = SessionLocal()

    try:

        all_leads = db.query(
            models.Lead
        ).all()

        if not all_leads:

            return {
                "message": "No leads available"
            }

        total_pipeline = sum(
            lead.estimated_deal_value
            for lead in all_leads
        )

        victoria_pipeline = sum(
            lead.estimated_deal_value
            for lead in all_leads
            if lead.region == "Victoria"
        )

        hot_pipeline = sum(
            lead.estimated_deal_value
            for lead in all_leads
            if lead.tier == "HOT"
        )

        return {
            "total_pipeline": total_pipeline,
            "victoria_pipeline": victoria_pipeline,
            "hot_pipeline": hot_pipeline,
            "recommendation":
                "Focus sales efforts on HOT opportunities and high-value accounts."
        }

    finally:
        db.close()

@app.post("/scenario-analysis")
def scenario_analysis(
    scenario: schemas.ScenarioRequest
):

    db = SessionLocal()

    try:

        all_leads = db.query(
            models.Lead
        ).all()

        current_forecast = sum(
            (lead.score / 100)
            * lead.estimated_deal_value
            for lead in all_leads
        )

        growth_factor = (
            scenario.marketing_increase_percent
            * 0.4
        )

        projected_forecast = (
            current_forecast
            * (
                1 + growth_factor / 100
            )
        )

        revenue_growth = (
            (
                projected_forecast
                - current_forecast
            )
            / current_forecast
        ) * 100 if current_forecast > 0 else 0
        print("Current Forecast:", current_forecast)
        print("Growth Factor:", growth_factor)
        print("Projected Forecast:", projected_forecast)
        return {
            "current_forecast":
                round(
                    current_forecast,
                    2
                ),

            "projected_forecast":
                round(
                    projected_forecast,
                    2
                ),

            "revenue_growth":
                round(
                    revenue_growth,
                    2
                ),

            "recommendation":
                "Increasing marketing investment appears financially attractive."
                if revenue_growth > 0
                else
                "Further analysis recommended."
        }

    finally:
        db.close()

@app.get("/executive-brief")
def executive_brief():

    db = SessionLocal()

    try:

        leads = db.query(
            models.Lead
        ).all()

        total_pipeline = sum(
            lead.estimated_deal_value
            for lead in leads
        )

        hot_leads = [
            lead for lead in leads
            if lead.tier == "HOT"
        ]

        summary = (
            f"Revenue pipeline contains "
            f"{len(leads)} opportunities "
            f"worth ${total_pipeline:,.0f}."
        )

        risks = []

        if len(leads) <= 1:
            risks.append(
                "Pipeline concentration risk detected."
            )

        if total_pipeline < 100000:
            risks.append(
                "Pipeline value below target."
            )

        opportunities = []

        if len(hot_leads) > 0:
            opportunities.append(
                "High-value HOT opportunities identified."
            )

        if total_pipeline > 500000:
            opportunities.append(
                "Pipeline exceeds strategic growth target."
            )

        if len(hot_leads) > 3:
            opportunities.append(
                "Strong concentration of high-conversion opportunities."
            )

        recommended_actions = [
            "Prioritize follow-up on HOT leads.",
            "Expand pipeline through targeted marketing."
        ]

        return {
            "summary": summary,
            "risks": risks,
            "opportunities": opportunities,
            "recommended_actions": recommended_actions
        }

    finally:
        db.close()

@app.get("/regional-analysis")
def regional_analysis():

    db = SessionLocal()

    try:

        leads = db.query(
            models.Lead
        ).all()

        if not leads:
            return {
                "message": "No leads available"
            }

        region_totals = {}

        for lead in leads:

            region_totals.setdefault(
                lead.region,
                0
            )

            region_totals[
                lead.region
            ] += lead.estimated_deal_value

        best_region = max(
            region_totals,
            key=region_totals.get
        )

        return {
            "best_region": best_region,
            "pipeline_value":
                region_totals[best_region],
            "recommendation":
                f"Increase sales investment in {best_region}."
        }

    finally:
        db.close()

@app.get("/sales-funnel")
def sales_funnel():

    db = SessionLocal()

    try:

        leads = db.query(
            models.Lead
        ).all()

        if not leads:
            return {
                "message": "No leads available"
            }

        funnel = {}

        for lead in leads:

            funnel.setdefault(
                lead.sales_stage,
                0
            )

            funnel[
                lead.sales_stage
            ] += 1

        return funnel

    finally:
        db.close()
 