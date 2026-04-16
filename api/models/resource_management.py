from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Resource_Management(Base):
    __tablename__ = "resource_management"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    resource_id = Column(Integer, ForeignKey("resources.id"))
    resource_amount = Column(Integer, nullable=False)
    unit = Column(String(50), nullable=False)
    resource = relationship("Resource", back_populates="resource_management")