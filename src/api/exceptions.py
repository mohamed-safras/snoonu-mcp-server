class CatalogError(Exception):
    """Base class for all catalog/order data-access errors"""

class ProductNotFoundError(CatalogError):
    def __init__(self, product_id:str):
        super().__init__(f"Product not found: {product_id}")
        self.product_id = product_id
        
class CityNotFoundError(CatalogError):
    def __init__(self, city:str):
        super().__init__(f"City not found: {city}")
        self.city = city
        
class OrderNotFoundError(CatalogError):
    def __init__(self, order_id:str):
        super().__init__(f"Order not found: {order_id}")
        self.order_id = order_id