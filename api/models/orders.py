from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100))
    order_date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    description = Column(String(300))

    order_details = relationship("OrderDetail", back_populates="order")

    # Add remaining database design considerations
    tracking_number = Column(String(50), unique=True, nullable=True)
    order_status = Column(String(20), nullable=False, default="Pending")
    total_price = Column(DECIMAL(10, 2), nullable=False, default=0.00)