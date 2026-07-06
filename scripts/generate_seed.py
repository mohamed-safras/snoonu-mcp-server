"""
Generates deploy/gcloud/db/02-seed-data.sql with real Qatar/GCC products
pulled from the OpenFoodFacts public API (openfoodfacts.org).

Products are mapped to our 10 categories based on their OFN category tags,
then merged with curated Qatar-specific products (Baladna, Mazzraty, Rayyan,
Doha Dates, etc.) that may have limited OFN coverage.

Usage:
    python scripts/generate_seed.py
    python scripts/generate_seed.py --count 1200
"""

import json, time, urllib.request, urllib.parse, re, sys, os, hashlib

CREATED_AT = "2026-06-26 15:55:09.901789+00"
TARGET = int(sys.argv[sys.argv.index("--count")+1]) if "--count" in sys.argv else 1200

# ── Category map: OFN tag → our category id ──────────────────────────────────
OFN_CAT_MAP = {
    "en:milks":2,"en:dairy":2,"en:yogurts":2,"en:fermented-milks":2,
    "en:cheeses":2,"en:butters":2,"en:beverages":2,"en:waters":2,
    "en:sodas":2,"en:fruit-juices":2,"en:coffees":2,"en:teas":2,
    "en:instant-coffees":2,"en:cereals-and-their-products":2,"en:breads":2,
    "en:biscuits-and-cakes":2,"en:chocolates":2,"en:confectioneries":2,
    "en:snacks":2,"en:chips-and-crackers":2,"en:dates":2,"en:dried-fruits":2,
    "en:rices":2,"en:pastas":2,"en:cooking-oils":2,"en:sauces":2,
    "en:condiments":2,"en:eggs":2,"en:meats":2,"en:frozen-foods":2,
    "en:nut-butters":2,"en:spreadable-fats":2,"en:jams":2,"en:honeys":2,
    "en:dietary-supplements":3,"en:vitamins":3,"en:cosmetics":3,
    "en:beauty":3,"en:personal-care":3,"en:hair-care":3,"en:skin-care":3,
    "en:oral-hygiene":3,"en:deodorants":3,
    "en:electronics":4,"en:headphones":4,"en:speakers":4,
    "en:baby-foods":7,"en:infant-formulas":7,"en:baby-milks":7,"en:diapers":7,
    "en:sports-nutrition":8,"en:energy-drinks":8,"en:sports-drinks":8,
    "en:protein-supplements":8,
    "en:pet-foods":9,"en:cat-foods":9,"en:dog-foods":9,
}

KEYWORD_CAT = [
    ("milk",2),("laban",2),("yogh",2),("yogurt",2),("cheese",2),("butter",2),
    ("juice",2),("water",2),("cola",2),("pepsi",2),("7up",2),("fanta",2),
    ("sprite",2),("coffee",2),("nescaf",2),("tea",2),("lipton",2),("bread",2),
    ("toast",2),("rice",2),("date",2),("chips",2),("pringles",2),("doritos",2),
    ("lay's",2),("kitkat",2),("cadbury",2),("snickers",2),("twix",2),
    ("nutella",2),("ketchup",2),("pasta",2),("biscuit",2),("cookie",2),
    ("cracker",2),("chocolate",2),("candy",2),("sugar",2),("flour",2),
    ("egg",2),("chicken",2),("beef",2),("tuna",2),("salmon",2),
    ("baladna",2),("mazzraty",2),("almarai",2),("rayyan",2),("oasis",2),
    ("aquafina",2),("evian",2),("rani",2),("cream",2),("mayonnaise",2),
    ("vitamin",3),("supplement",3),("panadol",3),("vicks",3),("shampoo",3),
    ("soap",3),("lotion",3),("moisturis",3),("sunscreen",3),("toothpaste",3),
    ("mouthwash",3),("deodorant",3),("perfume",3),("cologne",3),
    ("face wash",3),("micellar",3),("serum",3),("conditioner",3),
    ("airpods",4),("earbuds",4),("headphone",4),("speaker",4),
    ("charger",4),("cable",4),("power bank",4),
    ("shirt",5),("shoe",5),("sneaker",5),("watch",5),("sunglasses",5),
    ("wallet",5),("belt",5),
    ("detergent",6),("cleaner",6),("bleach",6),("trash",6),("tissue",6),
    ("wipe",6),("sponge",6),("pan",6),("air purifier",6),
    ("toothbrush",6),("electric toothbrush",6),
    ("lego",7),("toy",7),("doll",7),("diaper",7),("nappy",7),
    ("formula",7),("baby",7),("hot wheels",7),("barbie",7),
    ("protein",8),("whey",8),("gatorade",8),("energy drink",8),
    ("royal canin",9),("pedigree",9),("whiskas",9),("kong",9),
    ("cat food",9),("dog food",9),("cat litter",9),("pet",9),
    ("battery",10),("sanitizer",10),("tape",10),("pen",10),
    ("post-it",10),("scotch",10),("notebook",10),
]

def guess_category(name, brands, tags):
    for t in tags:
        if t in OFN_CAT_MAP:
            return OFN_CAT_MAP[t]
    txt = (name+" "+brands).lower()
    for kw, c in KEYWORD_CAT:
        if kw in txt:
            return c
    return 2

def guess_price(cat_id, name):
    ranges={1:(45,250),2:(1.5,90),3:(8,120),4:(50,3500),
            5:(100,1200),6:(8,550),7:(15,250),8:(6,900),9:(15,200),10:(5,150)}
    lo,hi=ranges.get(cat_id,(5,100))
    seed=int(hashlib.md5(name.encode()).hexdigest(),16)%1000
    return round(lo+(hi-lo)*seed/1000,2)

def esc(s):
    if not s: return "NULL"
    return "'"+str(s).replace("'","''")+"'"

def fetch_page(params, page, page_size=200):
    p={**params,"page":page,"page_size":page_size,"json":"1",
       "fields":"id,code,product_name,brands,categories_tags,image_front_url,quantity"}
    url="https://world.openfoodfacts.org/cgi/search.pl?"+urllib.parse.urlencode(p)
    try:
        req=urllib.request.Request(url,headers={
            "User-Agent":"SnoounuMCPServer/1.0 seed-gen (github.com/Mohamed-safras/snoonu-mcp-server)"})
        with urllib.request.urlopen(req,timeout=40) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  [warn] page {page}: {e}",file=sys.stderr)
        return None

def collect(params, max_p=500):
    out=[]
    for page in range(1,20):
        if len(out)>=max_p: break
        print(f"  page {page}...",file=sys.stderr)
        data=fetch_page(params,page)
        if not data or not data.get("products"): break
        for p in data["products"]:
            name=(p.get("product_name") or "").strip()
            brands=(p.get("brands") or "").strip()
            img=(p.get("image_front_url") or "").strip()
            if not name or not img or not img.startswith("http"): continue
            if len(name)>120: continue
            out.append({"name":name,"brands":brands[:80],"img":img,
                        "tags":p.get("categories_tags") or []})
        total=data.get("count",0)
        if page*200>=total: break
        time.sleep(0.4)
    return out

# ── Curated products (always included) ───────────────────────────────────────
# (id, name, brand, desc, cat_id, price, img, rating, in_stock, compare_at)
CURATED = [
    ("snu-c001","Baladna Full Fat Fresh Milk 1L","Baladna","Farm-fresh full-fat milk — Qatar's most-consumed fresh milk brand. Processed the same day on their farm north of Doha.",2,7.00,"https://images.openfoodfacts.org/images/products/629/100/300/9842/front_en.3.400.jpg",4.7,True,None),
    ("snu-c002","Baladna Fresh Milk 2L","Baladna","Family-size carton of full-fat fresh milk. No preservatives, locally produced.",2,12.00,None,4.6,True,None),
    ("snu-c003","Baladna Low Fat Fresh Milk 1L","Baladna","Fresh low-fat milk for health-conscious shoppers. Same farm-fresh quality.",2,7.50,None,4.5,True,None),
    ("snu-c004","Baladna Greek Style Yoghurt 4x150g","Baladna","Thick, creamy Greek-style yoghurt made from fresh Qatar milk. High protein, rich in probiotics.",2,9.75,None,4.8,True,None),
    ("snu-c005","Baladna Full Fat Yoghurt 1kg","Baladna","Smooth full-fat fresh yoghurt. Perfect with dates and honey, or as a cooking base for Gulf recipes.",2,8.50,None,4.7,True,None),
    ("snu-c006","Baladna Laban Drinking Yoghurt 1L","Baladna","Chilled laban — the classic Gulf drinking yoghurt. Light, tangy, and refreshing.",2,6.50,None,4.8,True,None),
    ("snu-c007","Baladna Laban Drinking Yoghurt 2L","Baladna","Large-format laban for family gatherings. Same refreshing taste, better value.",2,10.00,None,4.7,True,None),
    ("snu-c008","Baladna Custard Vanilla & Chocolate 4x110g","Baladna","Ready-to-eat custard cups in vanilla and chocolate. Made with fresh Qatar milk.",2,6.25,None,4.4,True,None),
    ("snu-c009","Mazzraty Probiotic Laban Full Fat 1L","Mazzraty","Probiotic laban from Qatar's 100% national NGAAP-certified brand. Full-fat, creamy, great for digestion.",2,6.00,None,4.6,True,None),
    ("snu-c010","Mazzraty Probiotic Laban Full Fat 500ml","Mazzraty","Individual-serve laban with live probiotic cultures.",2,3.50,None,4.5,True,None),
    ("snu-c011","Mazzraty Fresh Full Cream Milk 1L","Mazzraty","100% Qatari full-cream fresh milk from NGAAP farms.",2,8.00,None,4.5,True,None),
    ("snu-c012","Almarai Fresh Milk 1L","Almarai","Fresh pasteurised full-fat milk from Almarai, the GCC's leading dairy brand.",2,7.25,"https://images.openfoodfacts.org/images/products/628/176/400/0038/front_en.12.400.jpg",4.5,True,None),
    ("snu-c013","Almarai Cream Cheese 200g","Almarai","Smooth spreadable cream cheese. No artificial preservatives.",2,12.00,None,4.4,True,None),
    ("snu-c014","Lurpak Butter Slightly Salted 200g","Lurpak","The world's most popular butter — slightly salted, made from fresh cream.",2,16.00,"https://images.openfoodfacts.org/images/products/570/160/003/1154/front_en.34.400.jpg",4.7,True,None),
    ("snu-c015","Philadelphia Original Cream Cheese 200g","Mondelez","The iconic cream cheese — rich, versatile. Perfect for cheesecakes and bagels.",2,14.00,"https://images.openfoodfacts.org/images/products/768/901/237/0005/front_en.44.400.jpg",4.6,True,None),
    ("snu-c016","Kiri Cream Cheese Portions 8x17.5g","Bel Group","Individually portioned cream cheese — ideal for lunchboxes and kids.",2,12.00,None,4.3,True,None),
    ("snu-c017","Rayyan Natural Mineral Water 1.5L","Rayyan","Natural mineral water from Qatar's own aquifer 60 km north of Doha.",2,2.00,None,4.6,True,None),
    ("snu-c018","Rayyan Natural Mineral Water 6x1.5L","Rayyan","Six-pack of Rayyan — better value for daily hydration.",2,9.50,None,4.6,True,11.50),
    ("snu-c019","Qatar Oasis Balanced Drinking Water 1.5L","Qatar Oasis","Locally produced pH-balanced drinking water.",2,1.50,None,4.2,True,None),
    ("snu-c020","Qatar Oasis Drinking Water 6x1.5L","Qatar Oasis","Bulk pack of Qatar Oasis water — great for households.",2,7.50,None,4.2,True,9.00),
    ("snu-c021","Aquafina Purified Drinking Water 1.5L","PepsiCo","Seven-step HydRO-7 purified drinking water. Available across all Qatar outlets.",2,2.50,None,4.3,True,None),
    ("snu-c022","Evian Natural Spring Water 1.5L","Danone","Alpine natural spring water, naturally filtered over 15 years through glacial rocks.",2,5.00,"https://images.openfoodfacts.org/images/products/305/764/025/7773/front_en.343.400.jpg",4.5,True,None),
    ("snu-c023","Coca-Cola Original Taste 330ml Can","Coca-Cola","The world's favourite soft drink. Served chilled — great with meals.",2,2.50,"https://images.openfoodfacts.org/images/products/544/900/021/4911/front_fr.335.400.jpg",4.5,True,None),
    ("snu-c024","Coca-Cola Zero Sugar 330ml Can","Coca-Cola","Full Coca-Cola taste, zero sugar and zero calories.",2,2.50,None,4.4,True,None),
    ("snu-c025","Pepsi Cola 330ml Can","PepsiCo","Refreshing carbonated cola — Pepsi's bold, crisp taste.",2,2.50,None,4.4,True,None),
    ("snu-c026","7UP Lemon-Lime 330ml Can","PepsiCo","Crisp lemon-lime carbonated drink. Caffeine-free, refreshingly light.",2,2.25,None,4.3,True,None),
    ("snu-c027","Rani Float Mango Juice with Fruit Pieces 240ml","Al Aujan","Iconic Gulf mango juice drink with real fruit pieces. A regional classic enjoyed across Qatar.",2,2.50,"https://images.openfoodfacts.org/images/products/628/176/420/6028/front_en.5.400.jpg",4.7,True,None),
    ("snu-c028","Rani Float Orange Juice with Fruit Pieces 240ml","Al Aujan","Orange juice drink with real fruit pieces. Refreshing tropical taste.",2,2.50,None,4.6,True,None),
    ("snu-c029","Almarai Apple & Grape Juice 1L","Almarai","100% blended apple and grape juice. No added sugar, no preservatives.",2,9.50,None,4.5,True,None),
    ("snu-c030","Baladna Fresh Orange Juice 1L","Baladna","Freshly squeezed-style orange juice. No artificial colours or flavours.",2,8.50,None,4.6,True,None),
    ("snu-c031","Nescafe Classic Instant Coffee 200g","Nestle","Rich roasted aroma with a smooth, full-bodied flavour. Dissolves instantly.",2,17.00,"https://images.openfoodfacts.org/images/products/611/101/890/3161/front_fr.48.400.jpg",4.5,True,None),
    ("snu-c032","Nescafe Gold Blend Instant Coffee 95g","Nestle","Premium blend of finely roasted Arabica and Robusta beans. Distinctly smooth taste.",2,26.50,None,4.7,True,None),
    ("snu-c033","Nescafe Arabiana Arabic Coffee with Cardamom 20 Sachets","Nestle","Authentic Arabic coffee with real cardamom in single-serve sachets. A beloved Qatari morning ritual.",2,13.50,None,4.8,True,None),
    ("snu-c034","Nescafe 3-in-1 Original Coffee Mix 20 Sachets","Nestle","Coffee, creamer, and sugar in one sachet — just add hot water.",2,19.50,None,4.3,True,None),
    ("snu-c035","Cafe Najjar Classic Ground Coffee with Cardamom 200g","Cafe Najjar","Traditional Arabic ground coffee with cardamom from Lebanon's iconic brand.",2,16.00,None,4.7,True,None),
    ("snu-c036","Al Rifai Turkish Ground Coffee with Cardamom 250g","Al Rifai","Finely ground Turkish-style coffee enriched with cardamom. Bold and aromatic.",2,23.75,None,4.6,True,None),
    ("snu-c037","Lipton Yellow Label Black Tea 100 Bags","Unilever","Bright, brisk black tea — perfect with milk, lemon, or plain.",2,18.00,"https://images.openfoodfacts.org/images/products/800/235/005/4231/front_en.21.400.jpg",4.6,True,None),
    ("snu-c038","Ahmad Tea English Breakfast 100 Bags","Ahmad Tea","Premium English Breakfast blend — rich, malty, full-bodied. Popular in Qatar cafes.",2,22.00,None,4.7,True,None),
    ("snu-c039","Lipton Green Tea 100 Bags","Unilever","Light refreshing green tea with natural antioxidants. Great hot or chilled.",2,18.00,None,4.4,True,None),
    ("snu-c040","L'usine White Toast Bread 500g","Almarai","Soft white sliced toast bread from L'usine by Almarai. Fresh-baked, evenly sliced.",2,5.50,None,4.5,True,None),
    ("snu-c041","L'usine Whole Wheat Toast Bread 500g","Almarai","Whole wheat toast bread — higher in fibre, hearty flavour.",2,6.00,None,4.4,True,None),
    ("snu-c042","QBake White Sandwich Bread 500g","QBake","Locally baked white sandwich bread from Qatar's own QBake brand.",2,4.75,None,4.3,True,None),
    ("snu-c043","Arabic Pita Bread 10 Pieces","Local Bakery","Freshly baked thin Arabic pita bread. Essential for shawarma, hummus, and Gulf breakfasts.",2,3.50,None,4.6,True,None),
    ("snu-c044","Nutella Hazelnut & Cocoa Spread 400g","Ferrero","The world's favourite hazelnut spread with cocoa. Rich and creamy on toast or waffles.",2,18.00,"https://images.openfoodfacts.org/images/products/000/008/017/6800/front_en.273.400.jpg",4.9,True,None),
    ("snu-c045","Doha Dates Medjool Premium 500g","Doha Dates","Plump, soft Medjool dates from Doha Dates by NAFCO — Qatar's largest date processor.",2,16.75,None,4.8,True,None),
    ("snu-c046","Doha Dates Khalas 500g","Doha Dates","Khalas dates — considered the finest Gulf dates. Deep toffee-honey flavour. Grown in Qatar.",2,12.00,None,4.9,True,None),
    ("snu-c047","Doha Dates Sukkari 500g","Doha Dates","Sukkari dates — ultra-sweet, melt-in-the-mouth. A Ramadan and Eid favourite.",2,11.00,None,4.8,True,None),
    ("snu-c048","Bateel Kholas Premium Dates Gift Box 300g","Bateel","Luxury Kholas dates in a signature Bateel gift box. Hand-selected and elegantly presented.",2,55.00,None,4.9,True,None),
    ("snu-c049","Bateel Organic Assorted Dates Gift Box 500g","Bateel","Curated Bateel organic dates — Kholas, Wanan, and Segae — in a luxurious gift box.",2,89.00,None,5.0,True,None),
    ("snu-c050","Local Medjool Dates 1kg","Local Farm","Fresh Medjool dates from Qatari farms. Large, moist, naturally sweet.",2,30.00,None,4.7,True,None),
    ("snu-c051","Pringles Original Chips 165g","Kellogg's","The iconic stackable crisp with Pringles' signature original flavour.",2,11.00,"https://images.openfoodfacts.org/images/products/038/000/845/5963/front_en.15.400.jpg",4.6,True,None),
    ("snu-c052","Pringles Sour Cream & Onion 165g","Kellogg's","Fan-favourite flavour — tangy, savoury, impossible to put down.",2,11.00,None,4.7,True,None),
    ("snu-c053","Pringles Hot & Spicy 165g","Kellogg's","Bold, fiery kick in Pringles' signature stackable crisp format.",2,11.00,None,4.5,True,None),
    ("snu-c054","Doritos Nacho Cheese 48g","PepsiCo","Boldly flavoured nacho cheese tortilla chips. A party staple across Qatar.",2,4.50,None,4.5,True,None),
    ("snu-c055","Doritos Cool Ranch 48g","PepsiCo","Cool, tangy ranch flavour on Doritos' crunchy triangular chips.",2,4.50,None,4.5,True,None),
    ("snu-c056","Lay's Classic Potato Chips 145g","PepsiCo","Light, crispy potato chips with a simple salted flavour. A Qatar household staple.",2,7.50,None,4.5,True,None),
    ("snu-c057","Lay's BBQ Flavour 145g","PepsiCo","Smoky BBQ seasoned potato chips — rich, tangy, and perfectly balanced.",2,7.50,None,4.4,True,None),
    ("snu-c058","KitKat 4-Finger Milk Chocolate 45g","Nestle","Crispy wafer covered in smooth milk chocolate. Qatar's best-selling chocolate bar.",2,4.00,"https://images.openfoodfacts.org/images/products/400/009/007/5050/front_en.131.400.jpg",4.7,True,None),
    ("snu-c059","Cadbury Dairy Milk 90g","Mondelez","Creamy, smooth British milk chocolate. A household name in Qatar.",2,7.00,None,4.7,True,None),
    ("snu-c060","Twix Caramel Chocolate Bar 58g","Mars","Crunchy biscuit, smooth caramel, and milk chocolate — the classic twin bar.",2,4.00,None,4.6,True,None),
    ("snu-c061","Snickers Chocolate Bar 52g","Mars","Peanuts, caramel, nougat, and milk chocolate. One of Qatar's top confectionery bars.",2,4.00,None,4.6,True,None),
    ("snu-c062","M&M's Peanut Chocolate 250g","Mars","Whole peanuts coated in milk chocolate and a colourful candy shell. Great for sharing.",2,16.00,None,4.7,True,None),
    ("snu-c063","Tilda Pure Basmati Rice 2kg","Tilda","The world's finest basmati rice — long, slender, naturally aromatic grains.",2,24.00,"https://images.openfoodfacts.org/images/products/500/030/126/8620/front_en.38.400.jpg",4.8,True,None),
    ("snu-c064","Golden Sella Basmati Rice 5kg","Golden","Parboiled basmati rice ideal for biryani, kabsa, and machboos.",2,32.00,None,4.6,True,38.00),
    ("snu-c065","Mazzraty Fresh Eggs Large 12 Pieces","Mazzraty","Fresh large eggs from Mazzraty's 100% Qatari poultry farms.",2,11.00,None,4.7,True,None),
    ("snu-c066","Americana Chicken Breast Fillets 1kg","Americana","Boneless, skinless chicken fillets — Halal-certified, IQF frozen.",2,28.00,None,4.5,True,None),
    ("snu-c067","Hellmann's Real Mayonnaise 400g","Unilever","Rich, creamy real mayonnaise. The go-to condiment for sandwiches and dips.",2,14.00,None,4.6,True,None),
    ("snu-c068","Heinz Tomato Ketchup 570g","Kraft Heinz","Thick, tangy, naturally sweet ketchup. Essential in every Qatari household.",2,12.00,"https://images.openfoodfacts.org/images/products/000/001/700/7033/front_en.280.400.jpg",4.7,True,None),
    # Flowers & Gifting (1)
    ("snu-c069","Red Rose Bouquet 12 Stems","Snooflower","Twelve fresh-cut red roses wrapped in premium floral paper. Delivered same day across Doha.",1,85.00,None,4.7,True,None),
    ("snu-c070","Mixed Seasonal Flowers Arrangement","Snooflower","Vibrant hand-arranged bouquet of seasonal blooms — roses, lilies, and fillers.",1,120.00,None,4.6,True,None),
    ("snu-c071","White Orchid Potted Plant","Snooflower","Elegant white Phalaenopsis orchid in a ceramic pot. Long-lasting, sophisticated gift.",1,150.00,None,4.8,True,None),
    ("snu-c072","Premium Dates & Sweets Gift Hamper 1kg","Snooflower","Curated hamper with Khalas dates, assorted chocolates, and Arabic sweets in a decorative box.",1,95.00,None,4.8,True,None),
    ("snu-c073","Roses & Chocolate Gift Hamper","Snooflower","Six red roses paired with a premium chocolate box in an elegant gift bag.",1,180.00,None,4.7,True,None),
    ("snu-c074","Birthday Balloon Bouquet with Ribbon","Snooflower","Five large helium-filled latex balloons in assorted colours, ready to deliver.",1,45.00,None,4.5,True,None),
    ("snu-c075","Sunflower Bouquet 10 Stems","Snooflower","Bright, cheerful sunflower bouquet — a popular get-well and congratulations gift.",1,75.00,None,4.6,True,None),
    ("snu-c076","Luxury Rose & Lily Bouquet 20 Stems","Snooflower","Statement bouquet of roses and lilies in a luxury water-resistant wrap.",1,220.00,None,4.8,True,None),
    # Health & Beauty (3)
    ("snu-c077","Panadol Extra Strength 500mg 24 Tablets","GlaxoSmithKline","Fast-acting paracetamol for headaches, fever, and body aches. Qatar's most-trusted OTC pain reliever.",3,12.00,None,4.7,True,None),
    ("snu-c078","Vicks VapoRub Aromatic Ointment 50g","Procter & Gamble","Menthol, camphor, and eucalyptus oil — relieves coughs and nasal congestion.",3,15.00,None,4.7,True,None),
    ("snu-c079","Centrum Men Multivitamin 30 Tablets","Pfizer","Complete daily multivitamin formulated for men — Vitamin D, B12, Zinc, and more.",3,45.00,None,4.5,True,None),
    ("snu-c080","Vitamin C 1000mg Effervescent 30 Tablets","Redoxon","Effervescent Vitamin C — dissolves in water. Orange-flavoured, sugar-free.",3,25.00,None,4.6,True,None),
    ("snu-c081","Dove Deep Moisture Body Wash 500ml","Unilever","NutriumMoisture formula — leaves skin soft and hydrated after every shower.",3,18.00,None,4.7,True,None),
    ("snu-c082","Head & Shoulders Classic Clean Shampoo 400ml","Procter & Gamble","Clinically proven anti-dandruff shampoo. Gentle enough for everyday use.",3,22.00,None,4.6,True,None),
    ("snu-c083","Nivea Men Deep Face Wash 100ml","Beiersdorf","Deep-cleansing face wash with activated charcoal. Removes oil and impurities.",3,16.00,None,4.5,True,None),
    ("snu-c084","Colgate Total Whitening Toothpaste 150g","Colgate-Palmolive","Antibacterial protection for teeth, tongue, cheeks, and gums. Whitens in one step.",3,12.00,None,4.5,True,None),
    ("snu-c085","Garnier Micellar Cleansing Water 400ml","L'Oreal","All-in-one micellar water — cleanses, removes makeup, and refreshes. No rinse needed.",3,28.00,None,4.6,True,None),
    ("snu-c086","Neutrogena Hydro Boost Water Gel 50ml","Johnson & Johnson","Lightweight oil-free moisturiser with hyaluronic acid. Locks in hydration up to 72 hours.",3,55.00,None,4.7,True,None),
    ("snu-c087","Dettol Antibacterial Bar Soap 120g x3","Reckitt","Kills 99.9% of bacteria. Long-lasting protection — a must-have for every Qatari household.",3,9.00,None,4.5,True,None),
    ("snu-c088","Pantene Pro-V Smooth & Silky Shampoo 400ml","Procter & Gamble","Pro-V formula strengthens and smooths hair. Popular across Qatar salons and homes.",3,22.00,None,4.5,True,None),
    # Electronics (4)
    ("snu-c089","Apple AirPods Pro 2nd Generation","Apple","ANC, Adaptive Transparency, and Spatial Audio. MagSafe charging case included.",4,999.00,None,4.9,True,None),
    ("snu-c090","Samsung Galaxy Buds2 Pro True Wireless","Samsung","24-bit Hi-Fi audio, Intelligent ANC. Up to 29 hours battery with case.",4,649.00,None,4.7,True,799.00),
    ("snu-c091","JBL Flip 6 Portable Bluetooth Speaker","JBL","IP67 waterproof, 12-hour playtime, bold bass. Great for the beach and pool.",4,299.00,None,4.8,True,None),
    ("snu-c092","Anker PowerCore 20000mAh Power Bank","Anker","USB-C and USB-A ports. Charges an iPhone 15 nearly five times. Carry-on safe.",4,149.00,None,4.7,True,None),
    ("snu-c093","Sony WH-1000XM5 Wireless Headphones","Sony","Industry-leading noise cancellation, 30-hour battery, crystal-clear call quality.",4,1299.00,None,4.9,True,1499.00),
    ("snu-c094","Apple USB-C to Lightning Cable 1m","Apple","MFi-certified cable for fast charging iPhones and iPads.",4,79.00,None,4.5,True,None),
    ("snu-c095","Samsung 65 Crystal UHD 4K Smart TV","Samsung","4K UHD, Samsung Crystal Processor, HDR, Tizen OS. Near-borderless display.",4,3499.00,None,4.7,True,3999.00),
    ("snu-c096","Xiaomi Smart Band 8 Fitness Tracker","Xiaomi","1.62-inch AMOLED, heart rate, SpO2, sleep analysis. 16-day battery life.",4,149.00,None,4.5,True,None),
    ("snu-c097","JBL Charge 5 Portable Speaker","JBL","IP67 waterproof, 20-hour playtime, PowerBank function. Rich sound, deep bass.",4,449.00,None,4.8,True,None),
    # Fashion & Accessories (5)
    ("snu-c098","Ray-Ban Aviator Classic Polarized Sunglasses","Ray-Ban","Timeless Aviator with polarized lenses and gold metal frame. UV400 protection, unisex.",5,699.00,None,4.8,True,None),
    ("snu-c099","Nike Air Max 270 Men's Lifestyle Shoes","Nike","Nike's largest heel Air unit — all-day cushioning and sleek sporty profile.",5,449.00,None,4.7,True,None),
    ("snu-c100","Adidas Originals Stan Smith Sneakers","Adidas","The iconic minimalist leather tennis shoe turned streetwear classic.",5,329.00,None,4.7,True,None),
    ("snu-c101","Tommy Hilfiger Men's Slim Polo Shirt","Tommy Hilfiger","Classic slim-fit pique polo. 100% cotton — perfect for Qatar's smart-casual dress code.",5,249.00,None,4.5,True,None),
    ("snu-c102","Calvin Klein Reversible Leather Belt","Calvin Klein","Reversible black/brown leather belt with CK logo buckle.",5,179.00,None,4.4,True,None),
    ("snu-c103","Fossil Machine Stainless Steel Watch","Fossil","Three-hand dial, water-resistant to 10ATM. Popular gifting choice in Qatar.",5,899.00,None,4.6,True,1099.00),
    # Home & Garden (6)
    ("snu-c104","Tefal Expertise Non-Stick Frying Pan 28cm","Tefal","Superior non-stick, Thermo-Signal heat indicator. PFOA-free, dishwasher-safe.",6,89.00,None,4.6,True,None),
    ("snu-c105","Ariel Automatic Washing Powder 4kg","Procter & Gamble","Powerful stain-removing laundry powder for automatic washing machines.",6,38.00,None,4.6,True,45.00),
    ("snu-c106","Dettol Multi-Surface Antibacterial Spray 500ml","Reckitt","Kills 99.9% of bacteria on kitchen and bathroom surfaces. No rinsing required.",6,9.00,None,4.5,True,None),
    ("snu-c107","Glad ForceFlex Stretch Trash Bags 30L 20 Pieces","Glad","Stretchable bags that resist tears and punctures around sharp or heavy items.",6,8.50,None,4.4,True,None),
    ("snu-c108","Philips Air Purifier Series 800 AC0820","Philips","HEPA filter captures 99.97% of particles. Ideal for Doha's dusty conditions.",6,449.00,None,4.6,True,549.00),
    ("snu-c109","Oral-B Pro 1500 Electric Rechargeable Toothbrush","Oral-B","Removes up to 100% more plaque than manual. Pressure sensor, 2-min timer.",6,189.00,None,4.7,True,229.00),
    ("snu-c110","Finish Dishwasher Tablets Quantum 40 Tablets","Reckitt","All-in-one dishwasher tablets — removes tough stains, protects glass.",6,32.00,None,4.5,True,None),
    ("snu-c111","Scotch-Brite Heavy Duty Scrub Sponge 3 Pack","3M","Long-lasting scrubbing sponge — tough on grease, safe on most surfaces.",6,7.50,None,4.4,True,None),
    # Toys & Kids (7)
    ("snu-c112","LEGO Classic Creative Bricks 10696","LEGO","484 pieces in 33 colours. Open-ended building creativity for ages 4+.",7,149.00,None,4.9,True,None),
    ("snu-c113","Hot Wheels 20-Car Gift Pack","Mattel","20 die-cast Hot Wheels vehicles in assorted styles. A perennial Qatar favourite.",7,99.00,None,4.7,True,None),
    ("snu-c114","Barbie Fashionista Doll Assorted","Mattel","Barbie in a trendy outfit with accessories. Diverse doll styles, ages 3+.",7,79.00,None,4.6,True,None),
    ("snu-c115","Pampers Baby-Dry Diapers Size 4 52 Pieces","Procter & Gamble","Up to 12 hours overnight dryness. Three absorbing layers. Qatar's #1 diaper brand.",7,65.00,None,4.8,True,75.00),
    ("snu-c116","Huggies Ultra Comfort Diapers Size 4 52 Pieces","Kimberly-Clark","Soft inner layer keeps skin dry. Flexible waistband adapts to baby's movement.",7,60.00,None,4.7,True,None),
    ("snu-c117","Similac Gold Stage 1 Baby Formula 900g","Abbott","Infant formula with 2'FL HMO prebiotics. Supports immune development, 0-6 months.",7,185.00,None,4.7,True,None),
    ("snu-c118","Play-Doh 10-Color Pack","Hasbro","10 non-toxic, easy-to-play-with colours for creative fun. Ages 2+.",7,55.00,None,4.7,True,None),
    # Sports & Outdoors (8)
    ("snu-c119","Nike Dri-FIT Men's Training T-Shirt","Nike","Sweat-wicking Dri-FIT fabric. Lightweight and breathable for Qatar's intense heat.",8,149.00,None,4.6,True,None),
    ("snu-c120","Fitness Exercise Non-Slip Yoga Mat 6mm","Generic","Thick 6mm non-slip mat — cushions joints during yoga, pilates, and floor workouts.",8,79.00,None,4.4,True,None),
    ("snu-c121","MyProtein Impact Whey Protein Chocolate Brownie 1kg","MyProtein","21g protein per serving, low fat and low sugar. European-sourced whey concentrate.",8,189.00,None,4.7,True,219.00),
    ("snu-c122","Gatorade Lemon-Lime Sports Drink 600ml","PepsiCo","Electrolyte sports drink with sodium and potassium. Fuels performance and recovery.",8,6.50,None,4.5,True,None),
    ("snu-c123","Wilson Pro Staff Tennis Racket","Wilson","Professional carbon fibre racket. Advanced players' choice on Qatar's courts.",8,299.00,None,4.8,True,None),
    ("snu-c124","Adidas Ultraboost 22 Men's Running Shoes","Adidas","Enhanced BOOST cushioning, breathable Primeknit+. Maximum energy return.",8,749.00,None,4.8,True,899.00),
    # Pets (9)
    ("snu-c125","Royal Canin Indoor Adult Cat Dry Food 4kg","Royal Canin","Formulated for indoor cats — controls hairballs, manages weight, supports digestion.",9,145.00,None,4.8,True,None),
    ("snu-c126","Pedigree Adult Dry Dog Food Beef & Vegetables 3kg","Mars Petcare","Complete dry dog food. Supports healthy digestion, strong teeth, shiny coat.",9,65.00,None,4.6,True,None),
    ("snu-c127","Whiskas Adult Tuna in Jelly Wet Cat Food 12x85g","Mars Petcare","Twelve pouches of tuna in jelly. High moisture, balanced nutrition.",9,55.00,None,4.7,True,65.00),
    ("snu-c128","Kong Classic Natural Rubber Dog Toy Medium","Kong","Durable natural rubber toy. Fill with treats to keep dogs mentally stimulated.",9,55.00,None,4.8,True,None),
    ("snu-c129","Cat's Best Oko Plus Clumping Cat Litter 10L","Cat's Best","Wood-fibre clumping litter. 100% organic, biodegradable, superior odour control.",9,38.00,None,4.7,True,None),
    ("snu-c130","Royal Canin Kitten Dry Food 2kg","Royal Canin","Complete nutrition for kittens up to 12 months. Supports healthy growth and immune system.",9,89.00,None,4.8,True,None),
    ("snu-c131","Pedigree Puppy Dry Dog Food Chicken & Rice 3kg","Mars Petcare","Specially formulated for puppies. DHA from fish oil supports brain development.",9,72.00,None,4.7,True,None),
    # Market (10)
    ("snu-c132","Duracell Optimum AA Batteries 12 Pack","Duracell","Longest-lasting AA batteries — up to 13% extra life vs Duracell Plus.",10,28.00,None,4.7,True,None),
    ("snu-c133","3M Aura N95 Disposable Respirator 10 Pieces","3M","N95-rated, three-panel design for comfortable fit. Filters 95%+ of airborne particles.",10,45.00,None,4.6,True,None),
    ("snu-c134","Dettol Hand Sanitizer Instant Gel 500ml","Reckitt","Kills 99.9% of germs without water. Fast-drying, gentle on skin.",10,18.00,None,4.6,True,None),
    ("snu-c135","Scotch Magic Tape 19mm x 33m","3M","Invisible tape — writes and copies without showing. Strong adhesion, easy to hand-tear.",10,6.00,None,4.5,True,None),
    ("snu-c136","Post-it Original Notes 3x3 Assorted Colours 12 Pads","3M","12 pads of the original repositionable Post-it notes. 100 sheets per pad.",10,22.00,None,4.5,True,None),
    ("snu-c137","Energizer MAX AA Batteries 10 Pack","Energizer","Long-lasting alkaline batteries that hold power for up to 10 years in storage.",10,25.00,None,4.6,True,None),
    ("snu-c138","Pritt Stick Glue 43g","Henkel","Clean, washable glue stick — mess-free adhesive for school and office projects.",10,8.00,None,4.4,True,None),
]


def main():
    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "deploy","gcloud","db","02-seed-data.sql"
    )
    print(f"Target: {TARGET} products | Output: {out_path}", file=sys.stderr)

    seen = set()
    final = []

    # 1. Curated rows first
    for row in CURATED:
        key = row[1].lower().strip()
        if key in seen: continue
        seen.add(key)
        final.append(row)
    print(f"Curated: {len(final)}", file=sys.stderr)

    # 2. Pull from OpenFoodFacts
    searches = [
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Qatar",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Saudi Arabia",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"United Arab Emirates",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Egypt",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Jordan",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Lebanon",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Kuwait",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
        {"tagtype_0":"countries","tag_contains_0":"contains","tag_0":"Bahrain",
         "tagtype_1":"misc","tag_contains_1":"contains","tag_1":"en:complete-photo"},
    ]

    pool = []
    for params in searches:
        if len(final)+len(pool) >= TARGET+200: break
        need = TARGET - len(final) - len(pool)
        print(f"OFN: {params.get('tag_0','?')} (need ~{need} more)...", file=sys.stderr)
        batch = collect(params, max_p=min(need+100, 500))
        pool.extend(batch)
        print(f"  got {len(batch)}, pool={len(pool)}", file=sys.stderr)

    idx = 1
    for p in pool:
        if len(final) >= TARGET: break
        key = p["name"].lower().strip()
        if key in seen: continue
        if not p["img"].startswith("http"): continue
        seen.add(key)
        cat_id = guess_category(p["name"], p["brands"], p["tags"])
        price  = guess_price(cat_id, p["name"])
        cmp    = round(price*1.15, 2) if idx%5==0 else None
        rating = round(3.5+(int(hashlib.md5(p["name"].encode()).hexdigest()[:4],16)%15)/10,1)
        in_stock = (idx%20!=0)
        pid = f"snu-{idx:05d}"
        final.append((pid, p["name"], p["brands"], None, cat_id, price, p["img"],
                      rating, in_stock, cmp))
        idx += 1

    print(f"Final: {len(final)} products", file=sys.stderr)

    # 3. Write SQL
    header = """\
--
-- PostgreSQL database dump
--

\\restrict cznfCrh011aXx2WgnIIH7HXTdkggUATtzGQRUYrgN4XKaYgXVbIM2o4ZTTOZM9o

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg13+1)
-- Dumped by pg_dump version 16.14 (Debian 16.14-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: snoonu
--

INSERT INTO public.categories VALUES (1, 'Flowers & Gifting', 'flowers-gifting');
INSERT INTO public.categories VALUES (2, 'Grocery', 'grocery');
INSERT INTO public.categories VALUES (3, 'Health & Beauty', 'health-beauty');
INSERT INTO public.categories VALUES (4, 'Electronics', 'electronics');
INSERT INTO public.categories VALUES (5, 'Fashion & Accessories', 'fashion-accessories');
INSERT INTO public.categories VALUES (6, 'Home & Garden', 'home-garden');
INSERT INTO public.categories VALUES (7, 'Toys & Kids', 'toys-kids');
INSERT INTO public.categories VALUES (8, 'Sports & Outdoors', 'sports-outdoors');
INSERT INTO public.categories VALUES (9, 'Pets', 'pets');
INSERT INTO public.categories VALUES (10, 'Market', 'market');


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: snoonu
--

INSERT INTO public.cities VALUES (1, 'Doha', 25.285400, 51.531000, '{doha}');
INSERT INTO public.cities VALUES (2, 'Al Rayyan', 25.291900, 51.424400, '{rayyan}');
INSERT INTO public.cities VALUES (3, 'Al Wakrah', 25.165900, 51.603800, '{wakrah}');
INSERT INTO public.cities VALUES (4, 'Umm Salal', 25.415100, 51.397300, '{"umm salal"}');
INSERT INTO public.cities VALUES (5, 'Al Khor', 25.680400, 51.498900, '{"al khor",khor}');
INSERT INTO public.cities VALUES (6, 'Al Daayen', 25.519700, 51.492600, '{daayen}');
INSERT INTO public.cities VALUES (7, 'Al Shamal', 26.116700, 51.216700, '{"madinat shamal",shamal}');
INSERT INTO public.cities VALUES (8, 'Al Shahaniya', 25.370500, 51.196900, '{shahaniya}');


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: snoonu
-- Real Qatar/GCC products from OpenFoodFacts (openfoodfacts.org, CC-BY-SA)
-- plus curated Qatari brands (Baladna, Mazzraty, Rayyan, Doha Dates, etc.).
--

"""
    footer = """

--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: snoonu
--

SELECT pg_catalog.setval('public.categories_id_seq', 10, true);


--
-- Name: cities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: snoonu
--

SELECT pg_catalog.setval('public.cities_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

\\unrestrict cznfCrh011aXx2WgnIIH7HXTdkggUATtzGQRUYrgN4XKaYgXVbIM2o4ZTTOZM9o
"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header)
        for row in final:
            pid,name,brand,desc,cat_id,price,img,rating,in_stock,compare_at = row
            def s(v):
                if v is None: return "NULL"
                return "'"+str(v).replace("'","''")+"'"
            f.write(
                f"INSERT INTO public.products VALUES ("
                f"{s(pid)},{s(name)},{s(brand)},{s(desc)},"
                f"{cat_id},{price:.2f},'QAR',"
                f"{f'{compare_at:.2f}' if compare_at else 'NULL'},"
                f"{'true' if in_stock else 'false'},"
                f"{'\'high\'' if in_stock else '\'out_of_stock\''},"
                f"{s(img)},NULL,{rating},NULL,'{CREATED_AT}');\n"
            )
        f.write(footer)
    print("Done.", file=sys.stderr)

if __name__=="__main__":
    main()
