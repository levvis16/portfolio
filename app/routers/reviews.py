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

from sqlalchemy.sql import func

async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
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

@router.delete('/{review_id}')
async def delete_review(review_id: int, current_user: UserModel = Depends(get_current_user), db:AsyncSession = Depends(get_async_db)):
    if current_user.role != 'admin':
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= 'only for admin')
    
    review = await db.get(ReviewModel, review_id)

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Review not found')
    
    if not review.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Review not active')
    
    review.is_active = False
    product_id = review.product_id
    
    await db.commit()
    await update_product_rating(db, product_id)

    return {'message': 'Review deleted'}