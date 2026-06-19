import random
import pandas as pd

random.seed(42)

rows = []

industries = [
    "SaaS",
    "Finance",
    "Healthcare",
    "Retail",
    "Manufacturing"
]

titles = [
    "Manager",
    "Director",
    "VP",
    "CEO",
    "Coordinator"
]

for _ in range(10000):

    company_size = random.randint(10, 5000)

    pricing_views = random.randint(0, 10)

    email_opens = random.randint(0, 15)

    industry = random.choice(industries)

    title = random.choice(titles)

    score = (
        company_size * 0.001 +
        pricing_views * 3 +
        email_opens * 2
    )

    if title in ["Director", "VP", "CEO"]:
        score += 20

    converted = 1 if score > 45 else 0

    rows.append({
        "company_size": company_size,
        "pricing_views": pricing_views,
        "email_opens": email_opens,
        "industry": industry,
        "title": title,
        "converted": converted
    })

df = pd.DataFrame(rows)

df.to_csv("ml/leads.csv", index=False)

print("Generated 10,000 leads")