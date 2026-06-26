from __future__ import annotations
from typing import Protocol, Optional, TypedDict
from datetime import datetime

class ProductRecord(TypedDict):
    id: str
    name: str
    summary: Optional[str]
    description: Optional[str]
    price_amount: float
    price_currency: str
    compare_at_amount: Optional[float]
    in_stock: bool
    image_url: Optional[str]
    images: Optional[list[str]]
    rating: Optional[float]
    category_name: str
    category_slug: str
    
class CityRecord(TypedDict):
    name: str
    lat: float
    lng: float
    aliases: list[str]
    
class OrderRecord(TypedDict):
    id: str
    status: str
    total_amount: float
    currency: str
    created_at: datetime
    
class ProductsRepository(Protocol):
    def search(self, q: str, category: Optional[str], min_price: Optional[float],
               max_price: Optional[float], limit: int) -> list[ProductRecord]: ...
    def get(self, product_id: str) -> Optional[ProductRecord]: ...
    def get_price(self, product_id: str) -> float: ...  # raises ProductNotFoundError
    
class CategoriesRepository(Protocol):
    def list_all(self) -> list[tuple[str, str]]: ...  # (name, slug)
    
class CitiesRepository(Protocol):
    def list(self, query: Optional[str]) -> list[CityRecord]: ...
    def get(self, name: str) -> Optional[CityRecord]: ...
    
class OrdersRepository(Protocol):
    def create(self, ref: str, total: float, currency: str, recipient: dict,
               delivery: dict, sender: dict, gift_message: Optional[str],
               expires_at: datetime, cart: list[dict]) -> None: ...
    def get(self, order_id: str) -> Optional[OrderRecord]: ...
    
class CatalogClient(Protocol):
    products: ProductsRepository
    categories: CategoriesRepository
    cities: CitiesRepository
    orders: OrdersRepository