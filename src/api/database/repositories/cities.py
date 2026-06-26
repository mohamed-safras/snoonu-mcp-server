from sqlalchemy import select
from ..session import get_session
from ..models import City

class CitiesRepository:
    def list(self, query):
        with get_session() as session:
            stmt = select(City)
            if query:
                stmt = stmt.where(City.name.ilike(f"%{query}%"))
            rows = session.execute(stmt.order_by(City.name)).scalars().all()
            return [self._to_record(c) for c in rows]

    def get(self, name):
        with get_session() as session:
            row = session.execute(select(City).where(City.name.ilike(name))).scalars().first()
            return self._to_record(row) if row else None

    @staticmethod
    def _to_record(city: City) -> dict:
        return {"name": city.name, "lat": float(city.lat), "lng": float(city.lng), "aliases": city.aliases or []}