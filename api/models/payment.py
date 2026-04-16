from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from ..dependencies.database import Base

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    card_id = Column(String(4), nullable=True)
    payment_type = Column(String(50), nullable=False)
    transaction_status = Column(String(50), nullable=False, default='pending')
    order = relationship("Order", back_populates="payment")