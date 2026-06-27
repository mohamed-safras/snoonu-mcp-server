import random
from faker import Faker
from sqlalchemy import text
from src.api.database.session import engine
from scripts.fetch_openfoodfacts import fetch_grocery_products

fake = Faker()
random.seed(42)

CATEGORIES = [
    ("Flowers & Gifting", "flowers-gifting"),
    ("Grocery", "grocery"),
    ("Health & Beauty", "health-beauty"),
    ("Electronics", "electronics"),
    ("Fashion & Accessories", "fashion-accessories"),
    ("Home & Garden", "home-garden"),
    ("Toys & Kids", "toys-kids"),
    ("Sports & Outdoors", "sports-outdoors"),
    ("Pets", "pets"),
    ("Market", "market"),
]

# Synthetic templates for the categories OFF has no data for.
TEMPLATES = {
    "flowers-gifting": ["{adj} Rose Bouquet", "{adj} Orchid Arrangement", "Gift Hamper — {adj} Edition"],
    "health-beauty": ["{adj} Oud Perfume 50ml", "{adj} Skincare Set", "Luxury {adj} Soap Bar"],
    "electronics": ["{adj} Wireless Earbuds", "{adj} Power Bank 20000mAh", "Smart {adj} Watch"],
    "fashion-accessories": ["{adj} Leather Wallet", "{adj} Silk Scarf", "Classic {adj} Sunglasses"],
    "home-garden": ["{adj} Ceramic Vase", "{adj} Indoor Plant Pot", "Scented {adj} Candle Set"],
    "toys-kids": ["{adj} Building Blocks Set", "{adj} Plush Teddy Bear", "Educational {adj} Puzzle"],
    "sports-outdoors": ["{adj} Yoga Mat", "{adj} Camping Tent", "Pro {adj} Football"],
    "pets": ["{adj} Pet Bed", "Grain-Free {adj} Pet Food", "{adj} Cat Scratching Post"],
}
ADJECTIVES = ["Premium", "Royal", "Deluxe", "Classic", "Artisan", "Golden", "Elegant", "Heritage"]

# LoremFlickr keyword tags per template — real Flickr photos that actually match the
# product name, unlike Picsum's arbitrary random photos.
TEMPLATE_KEYWORDS = {
    "{adj} Rose Bouquet": "rose,bouquet",
    "{adj} Orchid Arrangement": "orchid,flowers",
    "Gift Hamper — {adj} Edition": "gift,hamper",
    "{adj} Oud Perfume 50ml": "perfume,bottle",
    "{adj} Skincare Set": "skincare,cosmetics",
    "Luxury {adj} Soap Bar": "soap,bar",
    "{adj} Wireless Earbuds": "earbuds,headphones",
    "{adj} Power Bank 20000mAh": "powerbank,charger",
    "Smart {adj} Watch": "smartwatch",
    "{adj} Leather Wallet": "wallet,leather",
    "{adj} Silk Scarf": "scarf,silk",
    "Classic {adj} Sunglasses": "sunglasses",
    "{adj} Ceramic Vase": "vase,ceramic",
    "{adj} Indoor Plant Pot": "plant,pot",
    "Scented {adj} Candle Set": "candle",
    "{adj} Building Blocks Set": "building.blocks,toy",
    "{adj} Plush Teddy Bear": "teddybear,plush",
    "Educational {adj} Puzzle": "puzzle,kids",
    "{adj} Yoga Mat": "yoga,mat",
    "{adj} Camping Tent": "camping,tent",
    "Pro {adj} Football": "football,soccerball",
    "{adj} Pet Bed": "petbed,dog",
    "Grain-Free {adj} Pet Food": "petfood,dog",
    "{adj} Cat Scratching Post": "cat,scratchingpost",
}

def _stock_level(in_stock: bool) -> str:
    return "out_of_stock" if not in_stock else random.choice(["high", "low"])

QATAR_CITIES = [
    ("Doha", 25.2854, 51.5310, ["doha"]),
    ("Al Rayyan", 25.2919, 51.4244, ["rayyan"]),
    ("Al Wakrah", 25.1659, 51.6038, ["wakrah"]),
    ("Umm Salal", 25.4151, 51.3973, ["umm salal"]),
    ("Al Khor", 25.6804, 51.4989, ["al khor", "khor"]),
    ("Al Daayen", 25.5197, 51.4926, ["daayen"]),
    ("Al Shamal", 26.1167, 51.2167, ["madinat shamal", "shamal"]),
    ("Al Shahaniya", 25.3705, 51.1969, ["shahaniya"]),
]

def seed():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE order_items, orders, products, categories, cities RESTART IDENTITY CASCADE"))

        cat_ids = {}
        for name, slug in CATEGORIES:
            row = conn.execute(
                text("INSERT INTO categories (name, slug) VALUES (:n, :s) RETURNING id"),
                {"n": name, "s": slug},
            ).fetchone()
            cat_ids[slug] = row[0]

        for name, lat, lng, aliases in QATAR_CITIES:
            conn.execute(
                text("INSERT INTO cities (name, lat, lng, aliases) VALUES (:n, :lat, :lng, :a)"),
                {"n": name, "lat": lat, "lng": lng, "a": aliases},
            )

        pid = 1
        rows = []

        # Grocery + Market: real OFF products, real images.
        off_products = fetch_grocery_products(total=420)  # ~210 per category
        half = len(off_products) // 2
        for slug, batch in (("grocery", off_products[:half]), ("market", off_products[half:])):
            for item in batch:
                price = round(random.uniform(5, 120), 2)  # OFF has no pricing — generated
                in_stock = random.random() > 0.05
                pid_str = f"snu-{pid:05d}"
                rows.append({
                    "id": pid_str,
                    "name": item["name"][:200],
                    "summary": item["brand"] or fake.sentence(nb_words=6),
                    "category_id": cat_ids[slug],
                    "price_amount": price,
                    "compare_at_amount": round(price * 1.2, 2) if random.random() < 0.2 else None,
                    "in_stock": in_stock,
                    "stock_level": _stock_level(in_stock),
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "image_url": item["image_url"],
                    "url": f"https://www.snoonu.com/qa-en/qatar/product/{pid_str}",
                })
                pid += 1

        # Remaining 8 categories: synthetic, as before.
        for slug, templates in TEMPLATES.items():
            for _ in range(100):  # 8 * 100 = 800
                template = random.choice(templates)
                name = template.format(adj=random.choice(ADJECTIVES))
                price = round(random.uniform(15, 800), 2)
                in_stock = random.random() > 0.05
                pid_str = f"snu-{pid:05d}"
                keywords = TEMPLATE_KEYWORDS[template]
                rows.append({
                    "id": pid_str,
                    "name": name,
                    "summary": fake.sentence(nb_words=8),
                    "category_id": cat_ids[slug],
                    "price_amount": price,
                    "compare_at_amount": round(price * 1.25, 2) if random.random() < 0.25 else None,
                    "in_stock": in_stock,
                    "stock_level": _stock_level(in_stock),
                    "rating": round(random.uniform(3.5, 5.0), 1),
                    "image_url": f"https://picsum.photos/seed/snu{pid}/600/600",
                    "url": f"https://www.snoonu.com/qa-en/qatar/product/{pid_str}",
                })
                pid += 1

        conn.execute(
            text("""INSERT INTO products
                (id, name, summary, category_id, price_amount, compare_at_amount,
                 in_stock, stock_level, rating, image_url, url)
                VALUES (:id, :name, :summary, :category_id, :price_amount,
                 :compare_at_amount, :in_stock, :stock_level, :rating, :image_url, :url)"""),
            rows,
        )
        print(f"Seeded {len(rows)} products ({len(off_products)} from Open Food Facts) "
              f"across {len(CATEGORIES)} categories, {len(QATAR_CITIES)} cities")

if __name__ == "__main__":
    seed()
