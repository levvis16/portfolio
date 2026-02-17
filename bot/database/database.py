from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import Category as CategoryModel, Product as ProductModel
from app.schemas import Category, Product
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.engine = create_async_engine(dsn)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)
    
    async def get_root_categories(self) -> list[Category]:
        """Получить корневые категории"""
        async with self.async_session() as session:
            stmt = select(CategoryModel).where(
                CategoryModel.parent_id.is_(None),
                CategoryModel.is_active == True
            ).order_by(CategoryModel.name)
            result = await session.execute(stmt)
            categories = result.scalars().all()
            
            return [Category.model_validate(cat) for cat in categories]
    
    async def get_subcategories(self, parent_id: int) -> list[Category]:
        """Получить подкатегории"""
        async with self.async_session() as session:
            stmt = select(CategoryModel).where(
                CategoryModel.parent_id == parent_id,
                CategoryModel.is_active == True
            ).order_by(CategoryModel.name)
            result = await session.execute(stmt)
            categories = result.scalars().all()
            return [Category.model_validate(cat) for cat in categories]
    
    async def get_products_by_category(self, category_id: int) -> list[Product]:
        """Получить товары в категории"""
        async with self.async_session() as session:
            stmt = select(ProductModel).where(
                ProductModel.category_id == category_id,
                ProductModel.is_active == True,
                ProductModel.stock > 0
            ).order_by(ProductModel.name)
            result = await session.execute(stmt)
            products = result.scalars().all()
            return [Product.model_validate(prod) for prod in products]
    
    async def get_product(self, product_id: int) -> Product | None:
        """Получить товар по ID"""
        async with self.async_session() as session:
            product = await session.get(ProductModel, product_id)
            if product and product.is_active:
                return Product.model_validate(product)
            return None