from sqlalchemy import select
from ..session import get_session
from ..models import Category

class CategoriesRepository:
    def list_all(self):
        with get_session() as session:
            rows = session.execute(select(Category.name, Category.slug).order_by(Category.name)).all()
            return [(name, slug) for name, slug in rows]