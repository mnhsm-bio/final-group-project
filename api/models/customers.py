from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base
from sqlalchemy.orm import relationship


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    address = Column(String(255), nullable=True)
    orders = relationship("Order", back_populates="customer")