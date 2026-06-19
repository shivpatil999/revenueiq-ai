from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from .database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String, nullable=False)

    company_size = Column(Integer)

    industry = Column(String)

    job_title = Column(String)

    pricing_page_views = Column(Integer)

    email_opens = Column(Integer)

    score = Column(Float)

    tier = Column(String)

    estimated_deal_value = Column(Float, default=0)

    sales_stage = Column(String, default="Prospecting")

    region = Column(String, default="Victoria")