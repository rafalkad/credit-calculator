import uuid

from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from model.inmemo.app_engine import app_engine

Base = declarative_base()


class Credit(Base):
    __tablename__ = 'credit_2'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    credit_type = Column(String, nullable=False)
    credit_value = Column(Float, nullable=False)
    remaining_balance = Column(Float, nullable=False)
    credit_date = Column(DateTime, nullable=False)
    monthly_payment = Column(Float, nullable=False)
    annual_interest_rate = Column(Float, nullable=False)


Base.metadata.create_all(app_engine)
