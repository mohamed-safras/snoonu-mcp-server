from sqlalchemy import select, func
from ..session import get_session
from ..models import Product, Category
from ...exceptions import ProductNotFoundError

class ProductsRepository:
    def search(self, q, category, min_price, max_price, limit):
        with get_session() as session:
            stmt = (
                select(Product, Category.name.label("category_name"), Category.slug.label("category_slug"))
                .join(Category, Product.category_id == Category.id)
                .where(
                    (Product.name.ilike(f"%{q}%")) | (Product.summary.ilike(f"%{q}%"))
                    | (func.similarity(Product.name, q) > 0.2)
                )
            )
            if category:
                stmt = stmt.where(Category.slug == category)
            if min_price is not None:
                stmt = stmt.where(Product.price_amount >= min_price)
            if max_price is not None:
                stmt = stmt.where(Product.price_amount <= max_price)
            stmt = stmt.order_by(func.similarity(Product.name, q).desc()).limit(limit)
            return [self._to_record(p, cn, cs) for p, cn, cs in session.execute(stmt).all()]
        
    
    def get(self, product_id):
        with get_session() as session:
            stmt = (
                select(Product, Category.name.label("category_name"), Category.slug.label("category_slug"))
                .join(Category, Product.category_id == Category.id)
                .where(Product.id == product_id)
            )
            row = session.execute(stmt).first()
            return self._to_record(*row) if row else None
    
    def get_price(self, product_id):
        with get_session() as session:
            product = session.get(Product, product_id)
            if not product:
                raise ProductNotFoundError(product_id)
            return float(product.price_amount)
    
    @staticmethod
    def _to_record(product: Product, category_name: str, category_slug: str) -> dict:
        return {
            "id": product.id, 
            "name": product.name,
            "summary": product.summary,
            "description": product.description,
            "price_amount": float(product.price_amount), 
            "price_currency": product.price_currency,
            "compare_at_amount": float(product.compare_at_amount) if product.compare_at_amount else None,
            "in_stock": product.in_stock, 
            "image_url": product.image_url,
            "images": product.images, 
            "rating": float(product.rating) if product.rating else None,
            "category_name": category_name, 
            "category_slug": category_slug,
        }