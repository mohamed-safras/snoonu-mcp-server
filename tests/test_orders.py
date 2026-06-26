import pytest
from src.api.client import client
from src.api.exceptions import ProductNotFoundError

def test_get_price_raises_for_unknown_product():
    with pytest.raises(ProductNotFoundError):
        client.products.get_price("does-not-exist")
