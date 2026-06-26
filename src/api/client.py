from .database.repositories.products import ProductsRepository
from .database.repositories.categories import CategoriesRepository
from .database.repositories.cities import CitiesRepository
from .database.repositories.orders import OrdersRepository

class DatabaseCatalogClient:
    def __init__(self):
        self.products = ProductsRepository()
        self.categories = CategoriesRepository()
        self.cities = CitiesRepository()
        self.orders = OrdersRepository()