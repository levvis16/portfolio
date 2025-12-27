from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime, timezone

from app.db_depends import get_async_db
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.models.users import User as UserModel
from app.auth import get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

async def update_product_rating(db: AsyncSession, product_id: int):
    """
    Пересчитывает средний рейтинг товара на основе активных отзывов.
    """
    rating_query = await db.execute(
        select(
            func.avg(ReviewModel.grade).label('avg_rating'),
            func.count(ReviewModel.id).label('review_count')
        ).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    
    result = rating_query.first()
    
    avg_rating = result[0] if result else None  
    review_count = result[1] if result else 0   
    
    if review_count and review_count > 0 and avg_rating is not None:
        # Обновляем рейтинг товара
        await db.execute(
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(rating=float(avg_rating))
        )
    else:
        # Если нет отзывов, устанавливаем рейтинг 0
        await db.execute(
            update(ProductModel)
            .where(ProductModel.id == product_id)
            .values(rating=0.0)
        )
    
    await db.commit()


@router.get('/', response_model=list[ReviewSchema])
async def get_review(db: AsyncSession = Depends(get_async_db)):
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return reviews.all()

@router.get("/products/{product_id}/reviews/", response_model=list[ReviewSchema])
async def get_product_review(product_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.scalars(select(ProductModel).where(ProductModel.id == product_id,
                                                         ProductModel.is_active == True))
    product = result.first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")
    
    review_result = await db.scalars(select(ReviewModel).where(ReviewModel.product_id == product_id,
                                                               ReviewModel.is_active == True))
    return review_result.all()

@router.post('/', response_model=ReviewSchema)
async def create_review(review_data: ReviewCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role != 'buyer':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only buyers can create reviews")
    
    product_result = await db.scalars(select(ProductModel).where(ProductModel.id == review_data.product_id,
                                                                 ProductModel.is_active == True))
    product = product_result.first()

    if not product:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail ='Product not found or inactive')
    
    existing_review = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True, 
                                                                 ReviewModel.user_id == current_user.id, 
                                                                 ReviewModel.product_id == review_data.product_id))
    
    if existing_review.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="You have already reviewed this product")
    
    new_review = ReviewModel(
        user_id = current_user.id,
        product_id = review_data.product_id,
        comment = review_data.comment,
        grade = review_data.grade,
        comment_date=datetime.now(timezone.utc),
        is_active = True
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)

    await update_product_rating(db, review_data.product_id)

    return new_review