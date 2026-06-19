import joblib
import pandas as pd

model = joblib.load("ml/lead_model.pkl")


def calculate_score(lead):

    df = pd.DataFrame([
        {
            "company_size": lead.company_size,
            "pricing_views": lead.pricing_page_views,
            "email_opens": lead.email_opens,
            "industry": lead.industry,
            "title": lead.job_title
        }
    ])

    probability = model.predict_proba(df)[0][1]

    score = round(probability * 100)

    if score >= 70:
        tier = "HOT"
    elif score >= 40:
        tier = "WARM"
    else:
        tier = "COLD"

    return score, tier