"""
Pulls real grocery/food products (name + real image) from Open Food Facts
(https://openfoodfacts.org) — open data (ODbL license) + open images
(CC-BY-SA 3.0). Used only for the Grocery/Market categories; OFF has no
electronics/fashion/toys data, so other categories stay synthetic.

Attribution required wherever these images are displayed:
"Photos: Open Food Facts contributors, CC-BY-SA 3.0".
"""
import time
import requests

# OFF's API usage policy requires a descriptive User-Agent identifying your app.
USER_AGENT = "SnoonuMockMCP/1.0 (contact@example.com)"
BASE = "https://world.openfoodfacts.org/api/v2/search"

# OFF category facet tags relevant to a grocery/market shelf.
OFF_CATEGORIES = [
    "beverages", "snacks", "dairies", "confectioneries",
    "biscuits-and-cakes", "breakfast-cereals", "canned-foods", "spices",
]

def _get_with_retry(params: dict, max_retries: int = 5):
    """GET with exponential backoff for transient errors (e.g. OFF's frequent 503s)."""
    for attempt in range(max_retries):
        try:
            resp = requests.get(BASE, params=params, headers={"User-Agent": USER_AGENT}, timeout=15)
            if resp.status_code in (429, 500, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise

def _fetch_category(tag: str, target_count: int, page_size: int = 100):
    """Yield OFF products for one category tag until target_count valid items found."""
    collected = 0
    page = 1
    while collected < target_count:
        resp = _get_with_retry({
            "categories_tags_en": tag,
            "fields": "code,product_name,image_front_url,brands",
            "page_size": page_size,
            "page": page,
        })
        products = resp.json().get("products", [])
        if not products:
            break  # exhausted this category
        for product in products:
            name = (product.get("product_name") or "").strip()
            image = product.get("image_front_url")
            if not name or not image:
                continue  # skip incomplete entries — name/image are required for our catalog
            yield {
                "name": name,
                "image_url": image,
                "brand": (product.get("brands") or "").split(",")[0].strip(),
            }
            collected += 1
            if collected >= target_count:
                return
        page += 1
        time.sleep(1)  # polite pacing, respects OFF's fair-use rate limits

def fetch_grocery_products(total: int = 400) -> list[dict]:
    per_category = max(1, total // len(OFF_CATEGORIES))
    items: list[dict] = []
    for tag in OFF_CATEGORIES:
        items.extend(_fetch_category(tag, per_category))
    return items
