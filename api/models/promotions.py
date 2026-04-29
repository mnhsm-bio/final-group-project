from sqlalchemy import Column, Integer, String, DATETIME, Float
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promotion_code = Column(String(50), nullable=False, unique=True)
    expiration_date = Column(DATETIME, nullable=False)
    discount_value = Column(Float, nullable=False)
