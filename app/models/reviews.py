from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional

from app.database import Base
from app.models import Product
from app.models import User

class Review(Base):
    __tablename__ = 'reviews'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable = False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable = False)
    comment: Mapped[Optional[str]] = mapped_column(String(500), nullable = True)
    comment_date: Mapped[datetime] = mapped_column(DateTime, default = datetime.now, nullable = False )
    grade: Mapped[int] = mapped_column(nullable = False)
    is_active: Mapped[Boolean] = mapped_column(Boolean, default = True, nullable = False)

    user: Mapped['User'] = relationship(back_populates='reviews')
    product: Mapped['Product'] = relationship(back_populates='reviews')
    __table_args__ = (
        CheckConstraint('grade >= 1 AND grade <= 5', name='check_grade_range'),
    )