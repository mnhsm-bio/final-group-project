from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Review(Base):
    __tablename__ = ("reviews")
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    review_text = Column(String(500), nullable=True)
    score = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="review")

