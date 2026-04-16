from sqlalchemy import Column, Integer, String
from ..dependencies.database import Base


class Resource_Management(Base):
    __tablename__ = "resource_management"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resource_amount = Column(Integer, nullable=False)
    unit = Column(String(50), nullable=False)