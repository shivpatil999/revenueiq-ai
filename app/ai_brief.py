def generate_sales_brief(lead):

    reasons = []

    if lead.company_size > 1000:
        reasons.append("large company size")

    if lead.pricing_page_views > 5:
        reasons.append("high pricing page engagement")

    if lead.email_opens > 10:
        reasons.append("strong email engagement")

    if lead.job_title.lower() in [
        "ceo",
        "cfo",
        "cto",
        "vp",
        "director"
    ]:
        reasons.append("senior decision maker")

    if len(reasons) == 0:
        reasons.append("limited engagement signals")

    return (
        f"This lead shows {', '.join(reasons)}. "
        f"Recommended action: contact within 24 hours."
    )