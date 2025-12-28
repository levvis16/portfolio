from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.products import Product

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    comment = Column(Text, nullable=True)
    comment_date = Column(DateTime, default=lambda: datetime.utcnow())
    grade = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Отношения
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")  # эта строка важна
    
    __table_args__ = (
        CheckConstraint("grade >= 1 AND grade <= 5", name="reviews_grade_check"),
    )