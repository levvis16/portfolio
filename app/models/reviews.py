from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, DateTime, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.products import Product

class Review(Base):
    __tablename__ = 'reviews'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    comment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    comment_date: Mapped[datetime] = mapped_column(
    DateTime(timezone=False),  # БЕЗ часового пояса
    default=datetime.now,      # Локальное время сервера
    nullable=False
    )
    grade: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Строковые аннотации
    user: Mapped['User'] = relationship(back_populates='reviews')
    product: Mapped['Product'] = relationship(back_populates='reviews')
    
    __table_args__ = (
        CheckConstraint('grade >= 1 AND grade <= 5', name='check_grade_range'),
    )