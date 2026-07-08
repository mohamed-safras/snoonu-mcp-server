"""
Generates deploy/gcloud/db/02-seed-data.sql with 500+ real Qatar/GCC products.
Self-contained: no external API calls.

Usage:
    python scripts/generate_seed.py
    python scripts/generate_seed.py --count 500
"""
import os, sys

CREATED_AT = "2026-06-26 15:55:09.901789+00"
RESTRICT_KEY = "cznfCrh011aXx2WgnIIH7HXTdkggUATtzGQRUYrgN4XKaYgXVbIM2o4ZTTOZM9o"

IMG = {
    # OpenFoodFacts CDN — use low revision numbers (3-25) which are earliest uploads
    # and rarely deleted. High revisions (100+) rotate when contributors upload better photos.
    "nescafe":    "https://images.openfoodfacts.org/images/products/611/101/890/3161/front_fr.3.400.jpg",
    "coca_cola":  "https://images.openfoodfacts.org/images/products/544/900/021/4911/front_fr.3.400.jpg",
    "coke_zero":  "https://images.openfoodfacts.org/images/products/544/900/021/4799/front_en.3.400.jpg",
    "evian":      "https://images.openfoodfacts.org/images/products/305/764/025/7773/front_en.3.400.jpg",
    "pellegrino": "https://images.openfoodfacts.org/images/products/800/227/001/4901/front_en.3.400.jpg",
    "rani":       "https://images.openfoodfacts.org/images/products/628/176/420/6028/front_en.5.400.jpg",
    "almarai":    "https://images.openfoodfacts.org/images/products/628/176/400/0038/front_en.3.400.jpg",
    "pringles":   "https://images.openfoodfacts.org/images/products/038/000/845/5963/front_en.3.400.jpg",
    "kitkat":     "https://images.openfoodfacts.org/images/products/500/015/946/1122/front_en.3.400.jpg",
    "cadbury":    "https://images.openfoodfacts.org/images/products/762/221/044/9283/front_en.3.400.jpg",
    "nutella":    "https://images.openfoodfacts.org/images/products/000/008/017/6800/front_en.3.400.jpg",
    "heinz":      "https://images.openfoodfacts.org/images/products/000/001/700/7033/front_en.3.400.jpg",
    "lurpak":     "https://images.openfoodfacts.org/images/products/570/160/003/1154/front_en.3.400.jpg",
    "philly":     "https://images.openfoodfacts.org/images/products/768/901/237/0005/front_en.3.400.jpg",
    "tilda":      "https://images.openfoodfacts.org/images/products/500/030/126/8620/front_en.3.400.jpg",
    "lipton":     "https://images.openfoodfacts.org/images/products/800/235/005/4231/front_en.3.400.jpg",
    "aquafina":   "https://images.openfoodfacts.org/images/products/611/125/242/1575/front_fr.3.400.jpg",
    "cappy":      "https://images.openfoodfacts.org/images/products/544/900/014/7417/front_en.3.400.jpg",
    "lindt70":    "https://images.openfoodfacts.org/images/products/304/692/002/2651/front_en.3.400.jpg",
    "lindt85":    "https://images.openfoodfacts.org/images/products/304/692/002/2606/front_en.3.400.jpg",
    "tuc":        "https://images.openfoodfacts.org/images/products/541/004/100/1204/front_en.3.400.jpg",
    "wasa":       "https://images.openfoodfacts.org/images/products/730/040/048/1595/front_fr.3.400.jpg",
    "nesquik":    "https://images.openfoodfacts.org/images/products/844/529/013/3403/front_en.3.400.jpg",
    # Electronics — Wikimedia Commons Special:FilePath (redirect-stable, never stale)
    "ps5":        "https://commons.wikimedia.org/wiki/Special:FilePath/PlayStation-5-wDualSense-Consoles.jpg?width=400",
    "switch_oled":"https://commons.wikimedia.org/wiki/Special:FilePath/Nintendo-Switch-OLED-wJoy-Con.jpg?width=400",
    "iphone15pro":"https://commons.wikimedia.org/wiki/Special:FilePath/IPhone_15_Pro_Models.jpg?width=400",
    "macair_m2":  "https://commons.wikimedia.org/wiki/Special:FilePath/2022_MacBook_Air_M2.jpg?width=400",
    "macpro_m3":  "https://commons.wikimedia.org/wiki/Special:FilePath/Apple_MacBook_Pro_M3_2023.jpg?width=400",
    "apple_watch":"https://commons.wikimedia.org/wiki/Special:FilePath/Apple_Watch_Series_9.jpg?width=400",
    "ipad_air":   "https://commons.wikimedia.org/wiki/Special:FilePath/IPad_Air_5th_generation.jpg?width=400",
    "galaxy_s24": "https://commons.wikimedia.org/wiki/Special:FilePath/Samsung_Galaxy_S24_Ultra_front.jpg?width=400",
    "galaxy_w6":  "https://commons.wikimedia.org/wiki/Special:FilePath/Samsung_Galaxy_Watch_6_Classic.jpg?width=400",
    "dji_mini4":  "https://commons.wikimedia.org/wiki/Special:FilePath/DJI_Mini_4_Pro_drone.jpg?width=400",
    "xbox_s":     "https://commons.wikimedia.org/wiki/Special:FilePath/Xbox-Series-S-Console-Set.jpg?width=400",
    "canon_r50":  "https://commons.wikimedia.org/wiki/Special:FilePath/Canon_EOS_R50.jpg?width=400",
    "lg_monitor": "https://commons.wikimedia.org/wiki/Special:FilePath/LG_27GP850-B_monitor.jpg?width=400",
    "razer_mouse":"https://commons.wikimedia.org/wiki/Special:FilePath/Razer_DeathAdder_V3.jpg?width=400",
    "logitech_wc":"https://commons.wikimedia.org/wiki/Special:FilePath/Logitech_Brio_4K_webcam.jpg?width=400",
    # New category images (low revision numbers for stability)
    "lavazza":    "https://images.openfoodfacts.org/images/products/800/007/001/1985/front_en.4.400.jpg",
    "illy":       "https://images.openfoodfacts.org/images/products/800/375/385/0115/front_en.3.400.jpg",
    "nespresso":  "https://images.openfoodfacts.org/images/products/763/003/940/0135/front_en.3.400.jpg",
    "starbucks":  "https://images.openfoodfacts.org/images/products/762/111/490/5050/front_en.5.400.jpg",
    "pampers_p":  "https://images.openfoodfacts.org/images/products/401/540/043/7055/front_en.3.400.jpg",
    "huggies_p":  "https://images.openfoodfacts.org/images/products/003/600/041/3350/front_en.3.400.jpg",
    "johnsons":   "https://images.openfoodfacts.org/images/products/357/466/143/3424/front_en.4.400.jpg",
    "aptamil":    "https://images.openfoodfacts.org/images/products/800/030/019/3306/front_en.3.400.jpg",
    "cerelac":    "https://images.openfoodfacts.org/images/products/628/102/302/4415/front_en.3.400.jpg",
    "bepanthen":  "https://images.openfoodfacts.org/images/products/401/060/203/2015/front_en.3.400.jpg",
    "dettol_ant": "https://images.openfoodfacts.org/images/products/628/064/603/8018/front_en.3.400.jpg",
    "gaviscon":   "https://images.openfoodfacts.org/images/products/500/049/412/7965/front_en.3.400.jpg",
    "rennie":     "https://images.openfoodfacts.org/images/products/400/399/041/8006/front_en.3.400.jpg",
}

# ── Curated products (id, name, brand, desc, cat_id, price, img_key_or_url, rating, in_stock, compare_at) ──
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
    ("snu-c012","Almarai Fresh Milk 1L","Almarai","Fresh pasteurised full-fat milk from Almarai, the GCC's leading dairy brand.",2,7.25,"almarai",4.5,True,None),
    ("snu-c013","Almarai Cream Cheese 200g","Almarai","Smooth spreadable cream cheese. No artificial preservatives.",2,12.00,None,4.4,True,None),
    ("snu-c014","Lurpak Butter Slightly Salted 200g","Lurpak","The world's most popular butter — slightly salted, made from fresh cream.",2,16.00,"lurpak",4.7,True,None),
    ("snu-c015","Philadelphia Original Cream Cheese 200g","Mondelez","The iconic cream cheese — rich, versatile. Perfect for cheesecakes and bagels.",2,14.00,"philly",4.6,True,None),
    ("snu-c016","Kiri Cream Cheese Portions 8x17.5g","Bel Group","Individually portioned cream cheese — ideal for lunchboxes and kids.",2,12.00,None,4.3,True,None),
    ("snu-c017","Rayyan Natural Mineral Water 1.5L","Rayyan","Natural mineral water from Qatar's own aquifer 60 km north of Doha.",2,2.00,None,4.6,True,None),
    ("snu-c018","Rayyan Natural Mineral Water 6x1.5L","Rayyan","Six-pack of Rayyan — better value for daily hydration.",2,9.50,None,4.6,True,11.50),
    ("snu-c019","Qatar Oasis Balanced Drinking Water 1.5L","Qatar Oasis","Locally produced pH-balanced drinking water.",2,1.50,None,4.2,True,None),
    ("snu-c020","Qatar Oasis Drinking Water 6x1.5L","Qatar Oasis","Bulk pack of Qatar Oasis water — great for households.",2,7.50,None,4.2,True,9.00),
    ("snu-c021","Aquafina Purified Drinking Water 1.5L","PepsiCo","Seven-step HydRO-7 purified drinking water. Available across all Qatar outlets.",2,2.50,"aquafina",4.3,True,None),
    ("snu-c022","Evian Natural Spring Water 1.5L","Danone","Alpine natural spring water, naturally filtered over 15 years through glacial rocks.",2,5.00,"evian",4.5,True,None),
    ("snu-c023","Coca-Cola Original Taste 330ml Can","Coca-Cola","The world's favourite soft drink. Served chilled — great with meals.",2,2.50,"coca_cola",4.5,True,None),
    ("snu-c024","Coca-Cola Zero Sugar 330ml Can","Coca-Cola","Full Coca-Cola taste, zero sugar and zero calories.",2,2.50,"coke_zero",4.4,True,None),
    ("snu-c025","Pepsi Cola 330ml Can","PepsiCo","Refreshing carbonated cola — Pepsi's bold, crisp taste.",2,2.50,None,4.4,True,None),
    ("snu-c026","7UP Lemon-Lime 330ml Can","PepsiCo","Crisp lemon-lime carbonated drink. Caffeine-free, refreshingly light.",2,2.25,None,4.3,True,None),
    ("snu-c027","Rani Float Mango Juice with Fruit Pieces 240ml","Al Aujan","Iconic Gulf mango juice drink with real fruit pieces. A regional classic enjoyed across Qatar.",2,2.50,"rani",4.7,True,None),
    ("snu-c028","Rani Float Orange Juice with Fruit Pieces 240ml","Al Aujan","Orange juice drink with real fruit pieces. Refreshing tropical taste.",2,2.50,None,4.6,True,None),
    ("snu-c029","Almarai Apple & Grape Juice 1L","Almarai","100% blended apple and grape juice. No added sugar, no preservatives.",2,9.50,None,4.5,True,None),
    ("snu-c030","Baladna Fresh Orange Juice 1L","Baladna","Freshly squeezed-style orange juice. No artificial colours or flavours.",2,8.50,None,4.6,True,None),
    ("snu-c031","Nescafe Classic Instant Coffee 200g","Nestle","Rich roasted aroma with a smooth, full-bodied flavour. Dissolves instantly.",2,17.00,"nescafe",4.5,True,None),
    ("snu-c032","Nescafe Gold Blend Instant Coffee 95g","Nestle","Premium blend of finely roasted Arabica and Robusta beans. Distinctly smooth taste.",2,26.50,None,4.7,True,None),
    ("snu-c033","Nescafe Arabiana Arabic Coffee with Cardamom 20 Sachets","Nestle","Authentic Arabic coffee with real cardamom in single-serve sachets. A beloved Qatari morning ritual.",2,13.50,None,4.8,True,None),
    ("snu-c034","Nescafe 3-in-1 Original Coffee Mix 20 Sachets","Nestle","Coffee, creamer, and sugar in one sachet — just add hot water.",2,19.50,None,4.3,True,None),
    ("snu-c035","Cafe Najjar Classic Ground Coffee with Cardamom 200g","Cafe Najjar","Traditional Arabic ground coffee with cardamom from Lebanon's iconic brand.",2,16.00,None,4.7,True,None),
    ("snu-c036","Al Rifai Turkish Ground Coffee with Cardamom 250g","Al Rifai","Finely ground Turkish-style coffee enriched with cardamom. Bold and aromatic.",2,23.75,None,4.6,True,None),
    ("snu-c037","Lipton Yellow Label Black Tea 100 Bags","Unilever","Bright, brisk black tea — perfect with milk, lemon, or plain.",2,18.00,"lipton",4.6,True,None),
    ("snu-c038","Ahmad Tea English Breakfast 100 Bags","Ahmad Tea","Premium English Breakfast blend — rich, malty, full-bodied. Popular in Qatar cafes.",2,22.00,None,4.7,True,None),
    ("snu-c039","Lipton Green Tea 100 Bags","Unilever","Light refreshing green tea with natural antioxidants. Great hot or chilled.",2,18.00,None,4.4,True,None),
    ("snu-c040","L'usine White Toast Bread 500g","Almarai","Soft white sliced toast bread from L'usine by Almarai. Fresh-baked, evenly sliced.",2,5.50,None,4.5,True,None),
    ("snu-c041","L'usine Whole Wheat Toast Bread 500g","Almarai","Whole wheat toast bread — higher in fibre, hearty flavour.",2,6.00,None,4.4,True,None),
    ("snu-c042","QBake White Sandwich Bread 500g","QBake","Locally baked white sandwich bread from Qatar's own QBake brand.",2,4.75,None,4.3,True,None),
    ("snu-c043","Arabic Pita Bread 10 Pieces","Local Bakery","Freshly baked thin Arabic pita bread. Essential for shawarma, hummus, and Gulf breakfasts.",2,3.50,None,4.6,True,None),
    ("snu-c044","Nutella Hazelnut & Cocoa Spread 400g","Ferrero","The world's favourite hazelnut spread with cocoa. Rich and creamy on toast or waffles.",2,18.00,"nutella",4.9,True,None),
    ("snu-c045","Doha Dates Medjool Premium 500g","Doha Dates","Plump, soft Medjool dates from Doha Dates by NAFCO — Qatar's largest date processor.",2,16.75,None,4.8,True,None),
    ("snu-c046","Doha Dates Khalas 500g","Doha Dates","Khalas dates — considered the finest Gulf dates. Deep toffee-honey flavour. Grown in Qatar.",2,12.00,None,4.9,True,None),
    ("snu-c047","Doha Dates Sukkari 500g","Doha Dates","Sukkari dates — ultra-sweet, melt-in-the-mouth. A Ramadan and Eid favourite.",2,11.00,None,4.8,True,None),
    ("snu-c048","Bateel Kholas Premium Dates Gift Box 300g","Bateel","Luxury Kholas dates in a signature Bateel gift box. Hand-selected and elegantly presented.",2,55.00,None,4.9,True,None),
    ("snu-c049","Bateel Organic Assorted Dates Gift Box 500g","Bateel","Curated Bateel organic dates — Kholas, Wanan, and Segae — in a luxurious gift box.",2,89.00,None,5.0,True,None),
    ("snu-c050","Local Medjool Dates 1kg","Local Farm","Fresh Medjool dates from Qatari farms. Large, moist, naturally sweet.",2,30.00,None,4.7,True,None),
    ("snu-c051","Pringles Original Chips 165g","Kellogg's","The iconic stackable crisp with Pringles' signature original flavour.",2,11.00,"pringles",4.6,True,None),
    ("snu-c052","Pringles Sour Cream & Onion 165g","Kellogg's","Fan-favourite flavour — tangy, savoury, impossible to put down.",2,11.00,None,4.7,True,None),
    ("snu-c053","Pringles Hot & Spicy 165g","Kellogg's","Bold, fiery kick in Pringles' signature stackable crisp format.",2,11.00,None,4.5,True,None),
    ("snu-c054","Doritos Nacho Cheese 48g","PepsiCo","Boldly flavoured nacho cheese tortilla chips. A party staple across Qatar.",2,4.50,None,4.5,True,None),
    ("snu-c055","Doritos Cool Ranch 48g","PepsiCo","Cool, tangy ranch flavour on Doritos' crunchy triangular chips.",2,4.50,None,4.5,True,None),
    ("snu-c056","Lay's Classic Potato Chips 145g","PepsiCo","Light, crispy potato chips with a simple salted flavour. A Qatar household staple.",2,7.50,None,4.5,True,None),
    ("snu-c057","Lay's BBQ Flavour 145g","PepsiCo","Smoky BBQ seasoned potato chips — rich, tangy, and perfectly balanced.",2,7.50,None,4.4,True,None),
    ("snu-c058","KitKat 4-Finger Milk Chocolate 45g","Nestle","Crispy wafer covered in smooth milk chocolate. Qatar's best-selling chocolate bar.",2,4.00,"kitkat",4.7,True,None),
    ("snu-c059","Cadbury Dairy Milk 90g","Mondelez","Creamy, smooth British milk chocolate. A household name in Qatar.",2,7.00,"cadbury",4.7,True,None),
    ("snu-c060","Twix Caramel Chocolate Bar 58g","Mars","Crunchy biscuit, smooth caramel, and milk chocolate — the classic twin bar.",2,4.00,None,4.6,True,None),
    ("snu-c061","Snickers Chocolate Bar 52g","Mars","Peanuts, caramel, nougat, and milk chocolate. One of Qatar's top confectionery bars.",2,4.00,None,4.6,True,None),
    ("snu-c062","M&M's Peanut Chocolate 250g","Mars","Whole peanuts coated in milk chocolate and a colourful candy shell. Great for sharing.",2,16.00,None,4.7,True,None),
    ("snu-c063","Tilda Pure Basmati Rice 2kg","Tilda","The world's finest basmati rice — long, slender, naturally aromatic grains.",2,24.00,"tilda",4.8,True,None),
    ("snu-c064","Golden Sella Basmati Rice 5kg","Golden","Parboiled basmati rice ideal for biryani, kabsa, and machboos.",2,32.00,None,4.6,True,38.00),
    ("snu-c065","Mazzraty Fresh Eggs Large 12 Pieces","Mazzraty","Fresh large eggs from Mazzraty's 100% Qatari poultry farms.",2,11.00,None,4.7,True,None),
    ("snu-c066","Americana Chicken Breast Fillets 1kg","Americana","Boneless, skinless chicken fillets — Halal-certified, IQF frozen.",2,28.00,None,4.5,True,None),
    ("snu-c067","Hellmann's Real Mayonnaise 400g","Unilever","Rich, creamy real mayonnaise. The go-to condiment for sandwiches and dips.",2,14.00,None,4.6,True,None),
    ("snu-c068","Heinz Tomato Ketchup 570g","Kraft Heinz","Thick, tangy, naturally sweet ketchup. Essential in every Qatari household.",2,12.00,"heinz",4.7,True,None),
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
    # ── Pharmacy (11) ──────────────────────────────────────────────────────────
    ("snu-c139","Panadol Advance 500mg Paracetamol 24 Tablets","GlaxoSmithKline","Fast-acting paracetamol for pain and fever. Qatar's most trusted OTC medicine.",11,14.00,None,4.8,True,None),
    ("snu-c140","Brufen 400mg Ibuprofen 24 Tablets","Abbott","Anti-inflammatory pain relief for headaches, muscle aches, and mild fever.",11,16.00,None,4.7,True,None),
    ("snu-c141","Voltaren Rapid 25mg Diclofenac 20 Tablets","Haleon","Fast-absorbing diclofenac for targeted pain relief. Works in 30 minutes.",11,22.00,None,4.6,True,None),
    ("snu-c142","Clarityn 10mg Loratadine Allergy 10 Tablets","Bayer","Non-drowsy 24-hour allergy relief — for hay fever, dust, and pet allergies.",11,18.00,None,4.7,True,None),
    ("snu-c143","Antinal 200mg Nifuroxazide 12 Capsules","Sanofi","Intestinal antiseptic for traveller's diarrhoea — widely prescribed in Qatar.",11,28.00,None,4.8,True,None),
    ("snu-c144","Omeprazole 20mg Gastro-Resistant 14 Capsules","Generic","Proton pump inhibitor — relieves acid reflux and heartburn for 24 hours.",11,15.00,None,4.6,True,None),
    ("snu-c145","Gaviscon Advance Peppermint Liquid 150ml","Reckitt","Sodium alginate raft — forms a protective layer on stomach acid. Fast relief.",11,28.00,"gaviscon",4.7,True,None),
    ("snu-c146","Rennie Antacid Spearmint 48 Tablets","Bayer","Calcium carbonate antacid — fast heartburn and indigestion relief.",11,16.00,"rennie",4.6,True,None),
    ("snu-c147","Betadine Povidone Iodine Antiseptic Solution 120ml","Mundipharma","Broad-spectrum antiseptic for wound cleaning — hospital-grade formula.",11,18.00,None,4.7,True,None),
    ("snu-c148","Dettol Antiseptic Disinfectant Liquid 500ml","Reckitt","Multi-purpose antiseptic — dilute to clean wounds, skin, or household surfaces.",11,22.00,"dettol_ant",4.6,True,None),
    ("snu-c149","Omron M2 Basic Blood Pressure Monitor","Omron","Validated clinically accurate upper-arm BP monitor — popular in Qatar clinics.",11,149.00,None,4.7,True,None),
    ("snu-c150","Microlife Digital Thermometer MT 550","Microlife","Oral/axillary/rectal measurement. 60-second reading, memory function.",11,29.00,None,4.6,True,None),
    ("snu-c151","Beurer FT 78 Infrared Non-Contact Thermometer","Beurer","Instant 1-second temperature reading. Hygienic, no-touch design for babies.",11,85.00,None,4.7,True,None),
    ("snu-c152","Vicks VapoRub Soothing Ointment 100g","Procter & Gamble","Menthol, camphor, and eucalyptus — relieves blocked nose and chesty cough.",11,22.00,None,4.7,True,None),
    ("snu-c153","Benylin Chesty Cough Syrup 150ml","Johnson & Johnson","Guaifenesin expectorant — loosens and expels chest mucus for easier breathing.",11,24.00,None,4.5,True,None),
    ("snu-c154","Strepsils Honey & Lemon Lozenges 24 Pack","Reckitt","Soothing antibacterial lozenges for sore throat pain and irritation.",11,14.00,None,4.6,True,None),
    ("snu-c155","Calpol Paracetamol Infant Suspension 120mg 100ml","Johnson & Johnson","Paediatric paracetamol suspension for children from 2 months. Strawberry flavour.",11,28.00,None,4.8,True,None),
    ("snu-c156","Band-Aid Flexible Fabric Assorted Bandages 30 Pack","Johnson & Johnson","Flexible fabric that moves with the skin. Individually wrapped, sterile.",11,14.00,None,4.6,True,None),
    ("snu-c157","Elastoplast SOS Blister Plasters 8 Pack","Beiersdorf","Hydrocolloid blister plasters — cushion and protect blisters instantly.",11,19.00,None,4.7,True,None),
    ("snu-c158","FreeStyle Lite Blood Glucose Meter Kit","Abbott","Compact glucose meter. No coding, tiny 0.3μL sample. Fast 5-second result.",11,89.00,None,4.7,True,None),
    ("snu-c159","Visine Classic Redness Eye Drops 15ml","Johnson & Johnson","Tetrahydrozoline drops for red-eye relief in minutes.",11,16.00,None,4.5,True,None),
    ("snu-c160","Optrex Refreshing Eye Drops 10ml","Reckitt","Soothes dry and tired eyes — ideal for screen users and air-conditioned offices.",11,18.00,None,4.5,True,None),
    ("snu-c161","Buscopan 10mg Hyoscine 20 Tablets","Sanofi","Antispasmodic for stomach cramps, IBS, and period pain.",11,20.00,None,4.6,True,None),
    ("snu-c162","Dioralyte Oral Rehydration Blackcurrant 20 Sachets","Reckitt","Electrolyte sachets for dehydration from diarrhoea, vomiting, or heat.",11,32.00,None,4.7,True,None),
    ("snu-c163","Nose Clip & Saline Spray Sterimar 100ml","Sterimar","Isotonic sea water nasal spray — daily nasal hygiene and decongestion.",11,22.00,None,4.6,True,None),
    # ── Arabic Sweets & Bakery (12) ──────────────────────────────────────────
    ("snu-c164","Kunafa with Ashta Cream 500g","Al Khaima","Traditional shredded-pastry kunafa filled with thick ashta cream. Served warm.",12,25.00,None,4.9,True,None),
    ("snu-c165","Kunafa with Mozzarella Cheese 1kg","Al Khaima","Classic cheese kunafa in orange kataifi pastry, drenched in rose-water syrup.",12,45.00,None,4.9,True,None),
    ("snu-c166","Luqaimat Honey & Sesame 500g","Local Kitchen","Bite-sized fried dough balls with date syrup, sesame, and saffron. Qatari street food.",12,18.00,None,4.8,True,None),
    ("snu-c167","Baklava Assorted Pistachio & Walnut 500g","Al Reef","Flaky filo pastry layers with pistachio and walnut, soaked in honey syrup.",12,38.00,None,4.8,True,None),
    ("snu-c168","Maamoul Date-Filled Shortbread Cookies 500g","Gandour","Semolina shortbread filled with Medjool dates. A Eid and Ramadan staple.",12,32.00,None,4.8,True,None),
    ("snu-c169","Maamoul Pistachio-Filled Cookies 500g","Gandour","Rose-water shortbread filled with sweet pistachio paste.",12,38.00,None,4.7,True,None),
    ("snu-c170","Basbousa Semolina Cake with Cream 500g","Hallab","Moist semolina cake soaked in syrup and topped with thick ashta.",12,22.00,None,4.7,True,None),
    ("snu-c171","Um Ali Egyptian Bread Pudding 500g","Al Khaima","Puff pastry bread pudding with cream, nuts, and coconut — a Gulf classic.",12,24.00,None,4.8,True,None),
    ("snu-c172","Mahalabiya Rose Water Milk Pudding 4 Cups","Local Kitchen","Chilled milk pudding with rose water, pistachios, and a hint of cardamom.",12,20.00,None,4.7,True,None),
    ("snu-c173","Sesame Halwa with Pistachio 400g","Al Reef","Rich sesame paste halwa studded with whole pistachios. A Levantine confection.",12,28.00,None,4.7,True,None),
    ("snu-c174","Mixed Turkish Delight Lokum 400g","Hazer Baba","Rose, pistachio, and lemon lokum dusted in icing sugar. Premium quality.",12,32.00,None,4.6,True,None),
    ("snu-c175","Qatayef Cream-Filled Pancakes 8 Pieces","Local Kitchen","Folded mini pancakes filled with ashta cream and fried golden — a Ramadan night treat.",12,24.00,None,4.9,True,None),
    ("snu-c176","Pistachio Bird's Nest Baklava 250g","Al Reef","Delicate nest-shaped kataifi pastry filled with whole pistachios and orange blossom.",12,35.00,None,4.8,True,None),
    ("snu-c177","Date & Walnut Halawa Fingers 400g","Local Kitchen","Soft date paste rolled with walnuts — a popular healthy Qatari sweet.",12,26.00,None,4.7,True,None),
    ("snu-c178","Sfouf Anise & Turmeric Cake 500g","Local Kitchen","Lebanese-style anise and turmeric semolina cake with pine nuts and sesame.",12,20.00,None,4.6,True,None),
    ("snu-c179","Assorted Petits Fours Gift Box 500g","Hallab","Lebanese confectionery assortment — namoura, barazek, and ghraybeh.",12,55.00,None,4.8,True,None),
    ("snu-c180","Ghraybeh Shortbread Cookies 400g","Gandour","Melt-in-the-mouth butter shortbread with a pistachio on top. A Levantine classic.",12,28.00,None,4.7,True,None),
    ("snu-c181","Kaak Sesame Ring Bread 500g","Local Bakery","Crunchy sesame-coated ring biscuit — a popular street snack across Qatar.",12,12.00,None,4.5,True,None),
    ("snu-c182","Harees Qatari Wheat & Chicken Pudding 500g","Al Khaima","Slow-cooked wheat and chicken blended to a smooth porridge. A National Day classic.",12,28.00,None,4.8,True,None),
    ("snu-c183","Ferrero Rocher Premium Selection Box 24 Pieces","Ferrero","Mixed Ferrero Rocher, Raffaello, and Rondnoir — a luxury Doha gift box.",12,55.00,"nutella",4.9,True,None),
    ("snu-c184","Godiva Belgian Chocolate Assorted 250g","Godiva","Premium Belgian milk, dark, and white chocolates in a signature gold gift box.",12,89.00,None,4.9,True,None),
    ("snu-c185","Lindt Swiss Classic Milk Chocolate Bar 300g","Lindt & Sprungli","Family-size creamy Swiss milk chocolate. A Qatar gifting favourite.",12,28.00,"lindt70",4.8,True,None),
    ("snu-c186","Eid Gift Sweets Assorted Tray 1kg","Hallab","Assorted Arabic sweets for Eid gifting — kunafa, baklava, and halwa in a tray.",12,65.00,None,4.9,True,None),
    ("snu-c187","Croissant Butter Classic 6 Pack","La Boulangerie","Flaky, all-butter classic croissants baked fresh. Available at Doha outlets.",12,14.00,None,4.6,True,None),
    ("snu-c188","Pain au Chocolat 6 Pack","La Boulangerie","Buttery laminated pastry with dark Belgian chocolate fill.",12,16.00,None,4.7,True,None),
    # ── Baby & Infant (13) ───────────────────────────────────────────────────
    ("snu-c189","Pampers Premium Care Newborn Size 1 54 Pieces","Procter & Gamble","Ultra-soft inner layer for delicate newborn skin. Up to 12 hours dryness.",13,65.00,"pampers_p",4.9,True,75.00),
    ("snu-c190","Pampers Premium Care Size 2 Mini 46 Pieces","Procter & Gamble","Whisper-soft layer for sensitive skin. Flexible waistband for 3-8kg babies.",13,65.00,"pampers_p",4.8,True,None),
    ("snu-c191","Pampers Premium Care Size 3 Midi 60 Pieces","Procter & Gamble","Outstanding softness — the #1 recommended newborn diaper in Qatar.",13,75.00,"pampers_p",4.8,True,85.00),
    ("snu-c192","Pampers Sensitive Baby Wipes 80 Sheets x3 Pack","Procter & Gamble","Alcohol-free, fragrance-free wipes — 3x more gentle than cloth. Triple pack.",13,38.00,None,4.8,True,None),
    ("snu-c193","Huggies Natural Care Baby Wipes 56 Sheets x4 Pack","Kimberly-Clark","Pure water formula — 99% water on biodegradable cotton cloth.",13,36.00,"huggies_p",4.7,True,None),
    ("snu-c194","Huggies Ultra Comfort Size 3 56 Pieces","Kimberly-Clark","Soft non-woven inner layer with DryTouch lining for comfortable fit.",13,65.00,"huggies_p",4.7,True,75.00),
    ("snu-c195","Johnson's Baby Shampoo No More Tears 300ml","Johnson & Johnson","Clinically proven to be as gentle as pure water. No-tear formula.",13,18.00,"johnsons",4.8,True,None),
    ("snu-c196","Johnson's Baby Wash & Shampoo 2-in-1 300ml","Johnson & Johnson","Gentle 2-in-1 cleanser — hypoallergenic, dermatologist-tested.",13,20.00,"johnsons",4.8,True,None),
    ("snu-c197","Johnson's Baby Oil 200ml","Johnson & Johnson","Pure mineral oil for baby massage — locks in moisture, gentle on sensitive skin.",13,14.00,"johnsons",4.7,True,None),
    ("snu-c198","Johnson's Baby Powder Classic 200g","Johnson & Johnson","Pure, mild talc-free powder — absorbs moisture and keeps baby comfortable.",13,12.00,"johnsons",4.6,True,None),
    ("snu-c199","Aptamil Gold+ Stage 1 First Infant Formula 900g","Nutricia","Dual prebiotic formula for gut immunity and DHA for brain development. 0-6 months.",13,195.00,"aptamil",4.8,True,None),
    ("snu-c200","Aptamil Gold+ Stage 2 Follow On Formula 900g","Nutricia","Follow-on formula with iron and DHA for babies 6-12 months.",13,185.00,"aptamil",4.7,True,None),
    ("snu-c201","NAN Supreme Pro 1 Infant Formula 800g","Nestlé","2'FL and LNnT prebiotics identical to those in breast milk. 0-6 months.",13,185.00,None,4.7,True,None),
    ("snu-c202","Cerelac Wheat with Milk Baby Cereal 250g","Nestlé","Iron-fortified first cereal for babies from 4 months. Quick dissolve texture.",13,22.00,"cerelac",4.7,True,None),
    ("snu-c203","Cerelac Rice 3 Cereals with Milk 250g","Nestlé","Multi-grain baby cereal with milk for 6-month+ babies. Smooth, easy to digest.",13,22.00,"cerelac",4.7,True,None),
    ("snu-c204","Bepanthen Nappy Care Ointment 100g","Bayer","Dexpanthenol ointment — prevents and heals nappy rash with every change.",13,32.00,"bepanthen",4.8,True,None),
    ("snu-c205","Sudocrem Antiseptic Healing Cream 250g","Forest Tosara","Zinc oxide cream for nappy rash, eczema, and minor cuts. Baby-safe formula.",13,25.00,None,4.7,True,None),
    ("snu-c206","Mustela Dermo-Cleansing Baby Wash 500ml","Mustela","No-rinse cleanser for baby's body and hair — hypoallergenic, with Avocado Perseose.",13,55.00,None,4.7,True,None),
    ("snu-c207","Philips Avent Natural Baby Bottle 260ml","Philips","Anti-colic air hole in teat. Wide breast-shaped teat for easy latch.",13,45.00,None,4.7,True,None),
    ("snu-c208","Chicco Physio Comfort Baby Soother 0-6m 2 Pack","Artsana","Orthodontic shape supports natural oral development. BPA-free silicone.",13,22.00,None,4.6,True,None),
    ("snu-c209","Graco DuoRider Tandem Pushchair Grey","Graco","Lie-flat recline, UV sun canopy, one-hand fold. Suitable from birth.",13,699.00,None,4.6,True,799.00),
    ("snu-c210","Ergobaby Adapt Soft-Structured Baby Carrier","Ergobaby","Ergonomic newborn carrier — no insert needed, three carry positions.",13,450.00,None,4.8,True,None),
    ("snu-c211","Summer Infant SwaddleMe Original Swaddle 3 Pack","Kids Line","Velcro swaddle wraps — secure and snug for newborn sleep comfort.",13,65.00,None,4.7,True,None),
    ("snu-c212","VTech Safe & Sound Baby Monitor VM3254","VTech","300m range, night vision, temperature sensor, and two-way talk.",13,199.00,None,4.6,True,None),
    # ── Coffee & Café (14) ──────────────────────────────────────────────────
    ("snu-c213","Lavazza Qualità Rossa Ground Coffee 250g","Lavazza","A balanced blend of Arabica and Robusta — full-bodied, velvety crema.",14,28.00,"lavazza",4.7,True,None),
    ("snu-c214","Lavazza Qualità Oro Ground Coffee 250g","Lavazza","100% Arabica — delicate, aromatic espresso with notes of dried fruit.",14,35.00,"lavazza",4.8,True,None),
    ("snu-c215","Lavazza Super Crema Espresso Whole Beans 1kg","Lavazza","Rich Arabica-Robusta blend — silky crema and long-lasting flavour.",14,75.00,"lavazza",4.8,True,None),
    ("snu-c216","illy Classico Espresso Ground Coffee 250g","illy","Nine single-origin Arabica beans blended perfectly. Medium roast, balanced.",14,42.00,"illy",4.8,True,None),
    ("snu-c217","illy Intenso Dark Roast Ground Coffee 250g","illy","Bold 100% Arabica blend — deep, rich espresso with chocolate and wood notes.",14,42.00,"illy",4.7,True,None),
    ("snu-c218","Nespresso Ristretto Intenso Capsules 10 Pack","Nestlé","Intense, roasted espresso with long, persistent bitterness. Intensity 10.",14,38.00,"nespresso",4.7,True,None),
    ("snu-c219","Nespresso Arpeggio Capsules 10 Pack","Nestlé","Intense and creamy espresso with notes of dark roasted cereals. Intensity 9.",14,38.00,"nespresso",4.7,True,None),
    ("snu-c220","Nespresso Vertuo Evoluo Coffee Machine Chrome","Nestlé","Centrifusion brewing for espresso to 414ml Alto. One-button simplicity.",14,699.00,None,4.7,True,799.00),
    ("snu-c221","De'Longhi Dedica Style EC685M Espresso Machine Silver","De'Longhi","15-bar pressure, steam wand, compact 15cm-wide design for Doha countertops.",14,799.00,None,4.7,True,899.00),
    ("snu-c222","Bialetti Moka Express 6-Cup Stovetop Coffee Maker","Bialetti","The iconic Italian stovetop espresso maker. Works on all hob types.",14,65.00,None,4.8,True,None),
    ("snu-c223","Chemex 6-Cup Classic Pour-Over Coffee Maker","Chemex","Hourglass borosilicate glass — produces clean, bright, sediment-free coffee.",14,165.00,None,4.8,True,None),
    ("snu-c224","Hario V60 Ceramic Pour Over Coffee Dripper White","Hario","Conical dripper with spiral ridges for even extraction — the barista's choice.",14,85.00,None,4.8,True,None),
    ("snu-c225","AeroPress Coffee & Espresso Maker","AeroPress","Pressure-brewed coffee in 30 seconds — versatile, easy to clean, travel-friendly.",14,120.00,None,4.9,True,None),
    ("snu-c226","Starbucks House Blend Medium Roast Ground Coffee 340g","Starbucks","Smooth, balanced, and lively — Starbucks' everyday medium roast.",14,65.00,"starbucks",4.6,True,None),
    ("snu-c227","Starbucks Pike Place Medium Roast Whole Bean 453g","Starbucks","Smooth, classic medium roast for everyday brewing.",14,75.00,"starbucks",4.7,True,None),
    ("snu-c228","Dolce Gusto Espresso Intenso 16 Pods","Nestlé","Bold espresso with a rich crema for Dolce Gusto machines.",14,35.00,"nescafe",4.5,True,None),
    ("snu-c229","Dolce Gusto Cappuccino 8 Servings 16 Pods","Nestlé","Espresso and milk foam pods — perfect frothy cappuccino at home.",14,35.00,"nescafe",4.5,True,None),
    ("snu-c230","Keurig K-Mini Single-Serve Coffee Maker Black","Keurig","Brews any K-Cup pod into 6-12 oz. Compact design, 12oz reservoir.",14,349.00,None,4.5,True,None),
    ("snu-c231","Fellow Stagg EKG Electric Gooseneck Kettle 0.9L","Fellow","Precision temperature control and stopwatch. The barista's pour-over kettle.",14,499.00,None,4.8,True,None),
    ("snu-c232","Porlex Mini II Hand Coffee Grinder","Porlex","Ceramic burrs, 18 grind settings, compact stainless body. Travel-ready.",14,195.00,None,4.7,True,None),
    ("snu-c233","Ahmad Tea Cardamom Flavoured Black Tea 100 Bags","Ahmad Tea","Black tea with real cardamom — the essential Gulf karak base.",14,25.00,"lipton",4.8,True,None),
    ("snu-c234","Twinings Jasmine Green Tea 50 Bags","Twinings","Delicate green tea scented with fresh jasmine flowers.",14,18.00,None,4.6,True,None),
    ("snu-c235","Costa Coffee Latte Ready to Drink 250ml Can","Costa","Barista-crafted latte in a can — milk, espresso, and a smooth finish.",14,8.00,None,4.5,True,None),
    ("snu-c236","Pokka Café Latte Ready to Drink 240ml","Pokka","Mild, creamy ready-to-drink latte — widely available across Qatar outlets.",14,5.00,None,4.4,True,None),
    ("snu-c237","Jacobs Kronung Aroma Filter Ground Coffee 500g","Jacobs","Smooth, mild German-style filter coffee — great for drip machines.",14,32.00,None,4.6,True,None),
    ("snu-c238","Melitta Caffè Crema Whole Bean Coffee 1kg","Melitta","Full-bodied crema coffee blend for bean-to-cup machines.",14,65.00,None,4.6,True,None),
    # ── Electronics – Phones & Tablets (4) ──────────────────────────────────
    ("snu-c239","Apple iPhone 15 Pro 256GB Natural Titanium","Apple","A17 Pro chip, 48MP main camera, titanium design, Action Button, USB-C.",4,4299.00,"iphone15pro",4.9,True,None),
    ("snu-c240","Apple iPhone 15 Pro Max 256GB Black Titanium","Apple","6.7-inch Super Retina XDR, 5x optical zoom, ProRes video, titanium frame.",4,4799.00,"iphone15pro",4.9,True,None),
    ("snu-c241","Samsung Galaxy S24 Ultra 256GB Titanium Black","Samsung","200MP camera, S Pen, Snapdragon 8 Gen 3, 7 years of OS updates.",4,4499.00,"galaxy_s24",4.9,True,None),
    ("snu-c242","Samsung Galaxy S24 256GB Onyx Black","Samsung","Snapdragon 8 Gen 3, 50MP ProVisual Engine, 7 years of OS updates.",4,2999.00,"galaxy_s24",4.8,True,None),
    ("snu-c243","Apple iPad Air 11-inch M2 128GB WiFi Starlight","Apple","M2 chip, Liquid Retina display, compatible with Apple Pencil Pro.",4,2299.00,"ipad_air",4.8,True,None),
    ("snu-c244","Apple iPad Mini 6th Gen 64GB WiFi Purple","Apple","8.3-inch Liquid Retina, A15 Bionic, USB-C, Centre Stage camera.",4,1899.00,"ipad_air",4.8,True,None),
    ("snu-c245","Samsung Galaxy Tab S9 FE 256GB WiFi Mint","Samsung","10.9-inch display, S Pen included, IP68 water resistant, Samsung DeX.",4,1499.00,None,4.6,True,1699.00),
    # ── Electronics – Wearables (4) ─────────────────────────────────────────
    ("snu-c246","Apple Watch Series 9 45mm GPS Midnight Aluminium","Apple","S9 chip, Double Tap gesture, Always-On Retina display, crash detection.",4,1699.00,"apple_watch",4.8,True,None),
    ("snu-c247","Apple Watch Ultra 2 49mm Titanium","Apple","Precision GPS, 60-hour battery, siren and depth gauge — built for extremes.",4,2999.00,"apple_watch",4.9,True,None),
    ("snu-c248","Samsung Galaxy Watch 7 44mm Graphite","Samsung","Advanced health monitoring, BioActive Sensor, Exynos W1000 chip.",4,1099.00,"galaxy_w6",4.7,True,None),
    # ── Electronics – Laptops (4) ────────────────────────────────────────────
    ("snu-c249","Apple MacBook Air 13-inch M3 8GB 256GB Midnight","Apple","M3 chip, 18-hour battery, fanless design, 1080p FaceTime camera.",4,4299.00,"macair_m2",4.9,True,None),
    ("snu-c250","Apple MacBook Air 15-inch M3 8GB 256GB Starlight","Apple","Biggest MacBook Air ever — M3 chip, 15.3-inch Liquid Retina display.",4,4799.00,"macair_m2",4.8,True,None),
    ("snu-c251","Apple MacBook Pro 14-inch M3 Pro 18GB 512GB","Apple","M3 Pro chip, mini-LED ProMotion display, 18-hour battery, Space Black.",4,7499.00,"macpro_m3",4.9,True,None),
    ("snu-c252","Dell XPS 14 9440 Intel Core Ultra 7 1TB","Dell","OLED 2.8K touch display, NPU AI chip, slim 1.64kg aluminium chassis.",4,5499.00,None,4.7,True,None),
    ("snu-c253","HP Spectre x360 14 2-in-1 Intel Evo 1TB","HP","OLED 2.8K touchscreen, 360° hinge, Intel Core Ultra 7, 17-hour battery.",4,5299.00,None,4.7,True,None),
    ("snu-c254","ASUS ROG Zephyrus G14 AMD Ryzen 9 RTX 4060","ASUS","Ryzen 9 7940HS, 16GB, 1TB, 165Hz OLED, 1.65kg gaming powerhouse.",4,5799.00,None,4.8,True,None),
    # ── Electronics – Monitors & Displays (4) ──────────────────────────────
    ("snu-c255","LG 27GP850-B 27-inch QHD 165Hz Gaming Monitor","LG","Nano IPS, 1ms response, G-Sync compatible, USB-C, ideal for Qatar gaming.",4,899.00,"lg_monitor",4.8,True,999.00),
    ("snu-c256","Dell UltraSharp U2723DE 27-inch 4K USB-C Hub Monitor","Dell","IPS Black panel, USB-C 90W PD, built-in KVM, outstanding colour accuracy.",4,1299.00,None,4.8,True,None),
    ("snu-c257","Samsung Odyssey G7 32-inch 4K 144Hz Gaming Monitor","Samsung","VA curved panel, QLED colour, 1ms response — high-refresh 4K gaming.",4,1699.00,None,4.7,True,1899.00),
    # ── Electronics – Cameras (4) ────────────────────────────────────────────
    ("snu-c258","Canon EOS R50 Mirrorless Camera Body White","Canon","24.2MP APS-C, 4K video, Dual Pixel AF, lightweight 375g — beginner-friendly.",4,2299.00,"canon_r50",4.7,True,None),
    ("snu-c259","Sony ZV-E10 Mirrorless Vlog Camera 16-50mm Kit","Sony","24.2MP, real-time Eye AF, product showcase mode — the vlogger's camera.",4,2299.00,None,4.7,True,None),
    ("snu-c260","DJI Mini 4 Pro Drone with RC-N2 Controller","DJI","4K/60fps, omnidirectional obstacle sensing, 34-min flight time, 249g.",4,1899.00,"dji_mini4",4.8,True,None),
    # ── Electronics – Gaming (4) ─────────────────────────────────────────────
    ("snu-c261","PlayStation 5 Slim Disc Edition White","Sony","GPU 10.3 TFLOPS, 3D audio, SSD 825GB, ray tracing — the Doha gamer's choice.",4,1899.00,"ps5",4.9,True,None),
    ("snu-c262","Nintendo Switch OLED White with Joy-Con","Nintendo","7-inch OLED screen, 64GB storage, enhanced audio, adjustable stand.",4,1349.00,"switch_oled",4.9,True,None),
    ("snu-c263","Xbox Series S 512GB Carbon Black","Microsoft","1440p, 120fps, Xbox Velocity Architecture, Game Pass ready.",4,999.00,"xbox_s",4.7,True,None),
    # ── Electronics – Peripherals & Accessories (4) ─────────────────────────
    ("snu-c264","Razer DeathAdder V3 Pro Wireless Gaming Mouse","Razer","Focus Pro 30K optical sensor, 90-hour battery, HyperSpeed wireless.",4,399.00,"razer_mouse",4.8,True,None),
    ("snu-c265","Keychron Q1 Pro 75% Wireless Mechanical Keyboard","Keychron","Gasket-mount, QMK/Via programmable, Gateron G Pro switches, aluminium body.",4,549.00,None,4.8,True,None),
    ("snu-c266","Logitech BRIO 4K Ultra HD Webcam","Logitech","4K 30fps or 1080p 60fps, RightLight 3 HDR, dual omnidirectional mics.",4,549.00,"logitech_wc",4.7,True,None),
    ("snu-c267","Samsung 870 EVO 1TB 2.5-inch SATA SSD","Samsung","560MB/s sequential read, reliable MLC NAND, 5-year warranty.",4,299.00,None,4.8,True,None),
    ("snu-c268","WD My Passport 4TB Ultra USB-C Portable HDD","WD","Auto-backup software, hardware encryption, bus-powered, black.",4,219.00,None,4.6,True,None),
    ("snu-c269","TP-Link Deco XE75 WiFi 6E Mesh System 3-Pack","TP-Link","Tri-band 6E, covers 680m², 4800Mbps, seamless whole-home coverage.",4,799.00,None,4.7,True,None),
    ("snu-c270","Elgato Stream Deck MK.2 15-Button","Elgato","Fully customisable LCD keys — for streaming, editing, and automation workflows.",4,549.00,None,4.7,True,None),
    ("snu-c271","Apple AirTag 4-Pack","Apple","Precision Finding with Ultra-Wideband, Bluetooth 5.0, 1-year battery life.",4,299.00,None,4.7,True,None),
    ("snu-c272","DJI OM 6 Smartphone Gimbal Stabiliser","DJI","3-axis stabilisation, ActiveTrack 6.0, magnetic quick-release, foldable.",4,349.00,None,4.7,True,None),
]

# ── Extra products (name, brand, desc, cat_id, price, img_key_or_None, rating, in_stock, compare_at) ──
EXTRA = [
    # ── Flowers & Gifting (1) ─────────────────────────────────────────────────
    ("Pink Rose Bouquet 12 Stems","Snooflower","Soft pink roses for birthdays and romantic occasions. Wrapped in premium paper, same-day Doha delivery.",1,85.00,None,4.6,True,None),
    ("White Rose Bouquet 10 Stems","Snooflower","Pure white roses symbolising elegance and new beginnings. Perfect for weddings and anniversaries.",1,80.00,None,4.7,True,None),
    ("Yellow Rose Bouquet 12 Stems","Snooflower","Cheerful yellow roses — perfect for friendship and congratulations.",1,75.00,None,4.5,True,None),
    ("Mixed Rose Bouquet 20 Stems","Snooflower","Twenty mixed-colour roses in a luxury water-resistant wrap.",1,110.00,None,4.7,True,None),
    ("Luxury Rose Hat Box 25 Stems","Snooflower","Roses arranged in a signature hat box — ideal for premium gifting in Doha.",1,195.00,None,4.8,True,None),
    ("Preserved Rose Box 16 Stems","Snooflower","Preserved roses in a luxury velvet box — lasts up to a year without water.",1,320.00,None,4.9,True,None),
    ("Garden Tulip Bouquet 15 Stems","Snooflower","Vibrant mixed tulips in spring colours. Long stems, fresh cut daily.",1,90.00,None,4.7,True,None),
    ("Peony Bouquet 8 Stems","Snooflower","Lush, full peony blooms in blush pink — a luxury gifting choice for special occasions.",1,145.00,None,4.8,True,None),
    ("Purple Orchid Potted Plant","Snooflower","Elegant purple Phalaenopsis orchid in a decorative ceramic pot.",1,170.00,None,4.8,True,None),
    ("Money Plant in Ceramic Pot","Snooflower","Lucky money plant (Epipremnum) — indoor air purifier, easy to maintain.",1,55.00,None,4.5,True,None),
    ("Peace Lily Potted Plant","Snooflower","Elegant peace lily — thrives indoors, air-purifying, and long-lasting.",1,65.00,None,4.6,True,None),
    ("Rose & Ferrero Rocher Gift Box","Snooflower","Six red roses with a 16-piece Ferrero Rocher box in a luxury bag.",1,145.00,None,4.8,True,None),
    ("Premium Chocolate & Flower Hamper","Snooflower","Roses paired with Godiva and Lindt chocolates in a signature gift box.",1,220.00,None,4.8,True,None),
    ("Eid Mubarak Flower & Dates Hamper","Snooflower","Curated Eid gift — mixed flowers, Khalas dates, and Arabic sweets.",1,185.00,None,4.9,True,None),
    ("Graduation Balloon Bouquet with Bear","Snooflower","Five graduation balloons and a plush teddy bear — same-day delivery in Doha.",1,85.00,None,4.6,True,None),
    ("Giant Foil Number Balloons 30th Birthday","Snooflower","Gold foil number '30' balloons with matching star accents.",1,75.00,None,4.6,True,None),
    ("Luxury Scented Candle Rose & Oud 200g","Luxury Home","Premium rose and oud scented soy wax candle. Burns for 50+ hours.",1,195.00,None,4.8,True,None),
    ("Ramadan Kareem Luxury Gift Hamper","Snooflower","Dates, Arabic sweets, oud incense, and prayer beads in a luxury box.",1,250.00,None,4.9,True,None),
    ("Baby Welcome Hamper","Snooflower","Newborn hamper with plush toy, muslin wrap, and baby care essentials.",1,150.00,None,4.8,True,None),
    ("Succulent Plant Set 3 Mini Pots","Snooflower","Three mini succulents in terracotta pots — low-maintenance and charming.",1,45.00,None,4.6,True,None),
    # ── Grocery – Dairy (2) ───────────────────────────────────────────────────
    ("Baladna Chocolate Flavoured Milk 200ml","Baladna","Ready-to-drink chocolate milk made from fresh Qatar milk. A lunchbox favourite.",2,2.50,None,4.6,True,None),
    ("Baladna Strawberry Flavoured Milk 200ml","Baladna","Fresh strawberry-flavoured milk — kids love it, parents trust Baladna quality.",2,2.50,None,4.6,True,None),
    ("Baladna Labneh 250g","Baladna","Strained yoghurt cheese with olive oil — a Levantine breakfast staple.",2,9.00,None,4.7,True,None),
    ("Mazzraty Ayran Drinking Yoghurt 330ml","Mazzraty","Chilled Ayran — the salted Turkish-style drinking yoghurt popular across the Gulf.",2,3.50,None,4.5,True,None),
    ("Mazzraty Labneh Full Fat 500g","Mazzraty","Premium strained labneh from Qatar's own NGAAP dairy farm.",2,14.00,None,4.7,True,None),
    ("Puck Cream Cheese Spread 240g","Savola","Smooth cream cheese widely used in Arabic breakfasts across Qatar.",2,12.00,"philly",4.5,True,None),
    ("Almarai Feta Cheese Crumbled 200g","Almarai","Crumbled Greek-style feta in brine — ideal for salads and fattoush.",2,14.50,None,4.5,True,None),
    ("Almarai Gouda Cheese Slices 200g","Almarai","Semi-hard Gouda slices — popular in sandwiches and manaesh across Qatar.",2,16.00,None,4.4,True,None),
    ("President Butter Unsalted 250g","Lactalis","French-style unsalted butter from President — preferred by chefs and bakers.",2,18.00,"lurpak",4.6,True,None),
    ("Lurpak Spreadable 400g","Arla","Soft spreadable version of Lurpak — directly from the fridge onto your bread.",2,20.00,"lurpak",4.6,True,None),
    ("Almarai UHT Full Fat Milk 1L","Almarai","Long-life UHT milk — great for pantry stocking with a 6-month shelf life.",2,5.50,"almarai",4.4,True,None),
    ("Almarai UHT Low Fat Milk 1L","Almarai","UHT low-fat milk — same great Almarai quality, less fat.",2,5.25,"almarai",4.3,True,None),
    ("Kraft Cheddar Cheese Slices 400g","Kraft","Individually wrapped Cheddar slices — melts perfectly on burgers.",2,22.00,None,4.5,True,None),
    ("Almarai Double Cream 250ml","Almarai","Rich, thick double cream — ideal for desserts and cooking sauces.",2,8.00,"almarai",4.5,True,None),
    ("Mazzraty Fresh Eggs Large 30 Pieces","Mazzraty","Bulk tray of 30 large fresh eggs from Qatar's own NGAAP poultry farms.",2,24.00,None,4.7,True,None),
    ("Arla Organic Full Fat Milk 1L","Arla","Certified organic whole milk — grass-fed cows, no antibiotics.",2,9.50,"almarai",4.6,True,None),
    # ── Grocery – Waters & Soft Drinks (2) ───────────────────────────────────
    ("Rayyan Sparkling Mineral Water 330ml","Rayyan","Lightly sparkling Qatar mineral water — refreshing and locally produced.",2,2.00,None,4.5,True,None),
    ("Rayyan Sparkling Mineral Water 1.5L","Rayyan","Large sparkling water from Qatar's own Rayyan brand.",2,5.00,None,4.5,True,None),
    ("S.Pellegrino Sparkling Natural Water 750ml","Nestlé","Italy's iconic sparkling mineral water. A premium table water choice in Doha.",2,8.00,"pellegrino",4.6,True,None),
    ("Perrier Sparkling Natural Water 330ml Can","Nestlé","Crisp, refreshing French sparkling water with natural carbonation.",2,4.50,None,4.5,True,None),
    ("Evian Natural Spring Water 500ml","Danone","Alpine spring water in a convenient 500ml bottle.",2,4.00,"evian",4.5,True,None),
    ("Aquafina Purified Water 500ml","PepsiCo","HydRO-7 purified drinking water in a handy 500ml bottle.",2,2.00,"aquafina",4.3,True,None),
    ("Volvic Natural Mineral Water 1.5L","Danone","Volcanic mineral water from Auvergne, France — smooth and mineral-rich.",2,5.50,None,4.4,True,None),
    ("Masafi Natural Mineral Water 1.5L","Masafi","UAE's No.1 mineral water brand — popular across all Qatar supermarkets.",2,2.50,None,4.3,True,None),
    ("Fanta Orange 330ml Can","Coca-Cola","Fruity, fizzy orange soft drink from the house of Coca-Cola.",2,2.50,None,4.3,True,None),
    ("Fanta Grape 330ml Can","Coca-Cola","Sweet and fizzy grape flavour — a popular Gulf market choice.",2,2.50,None,4.3,True,None),
    ("Sprite Lemon-Lime 330ml Can","Coca-Cola","Crisp, clean lemon-lime carbonated soft drink. Caffeine-free.",2,2.50,None,4.3,True,None),
    ("Mountain Dew 330ml Can","PepsiCo","Bold citrus-flavoured carbonated soft drink — intensely refreshing.",2,2.50,None,4.3,True,None),
    ("Red Bull Energy Drink 250ml","Red Bull GmbH","Vitalises body and mind. Caffeine, taurine, and B-vitamins in a single can.",2,6.00,None,4.4,True,None),
    ("Monster Energy Original Green 500ml","Monster Beverage","Triple filtered, lightly carbonated energy drink — the classic green can.",2,9.00,None,4.3,True,None),
    ("Mirinda Orange 330ml Can","PepsiCo","Sweet orange carbonated soft drink — a kids' party staple across Qatar.",2,2.25,None,4.2,True,None),
    ("Coca-Cola Original 1.5L Bottle","Coca-Cola","The classic Coca-Cola in a family-size bottle for home occasions.",2,5.50,"coca_cola",4.5,True,None),
    ("Pepsi Cola 1.5L Bottle","PepsiCo","Bold Pepsi taste in a large bottle — ideal for gatherings.",2,5.00,None,4.4,True,None),
    ("Schweppes Tonic Water 330ml Can","Coca-Cola","The original mixer — crisp quinine tonic perfect with gin.",2,4.00,None,4.4,True,None),
    ("Vimto Fruit Cordial Squash 250ml","Nichols","Beloved British-origin fruit squash — extremely popular in Qatar and GCC.",2,3.50,None,4.5,True,None),
    # ── Grocery – Juices (2) ─────────────────────────────────────────────────
    ("Almarai Orange Juice 1L","Almarai","100% not-from-concentrate orange juice. No added sugar or preservatives.",2,9.50,None,4.6,True,None),
    ("Almarai Mango Juice 1L","Almarai","Tropical mango juice drink — rich, sweet, and beloved across Qatar.",2,9.00,None,4.6,True,None),
    ("Almarai Mixed Fruit Juice 1L","Almarai","A blend of tropical fruits — guava, mango, and passion fruit.",2,9.00,None,4.5,True,None),
    ("Cappy Orange Juice 1L","Coca-Cola","Refreshing orange juice drink from Coca-Cola's Cappy brand.",2,7.50,"cappy",4.4,True,None),
    ("Rani Float Strawberry 240ml","Al Aujan","Strawberry juice drink with real fruit pieces. A Gulf classic.",2,2.50,None,4.6,True,None),
    ("Rani Float Lychee 240ml","Al Aujan","Exotic lychee juice with real fruit pieces. Light, sweet, and tropical.",2,2.50,"rani",4.6,True,None),
    ("Tropicana Orange Juice No Pulp 1L","PepsiCo","Premium squeezed orange juice — smooth, no pulp, no added sugar.",2,12.00,None,4.7,True,None),
    ("Rubicon Mango Juice Drink 288ml","Cott Beverages","Mango juice with a tropical twist — popular in Qatar's South Asian community.",2,3.00,None,4.5,True,None),
    ("Minute Maid Pulpy Orange 300ml","Coca-Cola","Orange juice with real pulp for a freshly-squeezed experience.",2,3.50,None,4.4,True,None),
    # ── Grocery – Coffee & Tea (2) ────────────────────────────────────────────
    ("Ahmad Tea Earl Grey 100 Bags","Ahmad Tea","Fragrant Earl Grey blend with bergamot oil — a Qatari café favourite.",2,22.00,"lipton",4.6,True,None),
    ("Ahmad Tea Green Tea 100 Bags","Ahmad Tea","Delicate green tea with a light, refreshing flavour. Rich in antioxidants.",2,20.00,None,4.5,True,None),
    ("Twinings English Breakfast 50 Bags","Twinings","Classic English Breakfast blend — bold, full-bodied, great with milk.",2,18.00,None,4.5,True,None),
    ("Twinings Green Tea & Lemon 50 Bags","Twinings","Refreshing green tea with a zesty lemon lift.",2,18.00,None,4.4,True,None),
    ("Lipton Chamomile Herbal Tea 20 Bags","Unilever","Soothing chamomile tea for calm evenings. Naturally caffeine-free.",2,9.50,"lipton",4.5,True,None),
    ("Nescafe Gold Espresso 12 Pods","Nestle","Intense espresso capsules compatible with Dolce Gusto machines.",2,22.00,"nescafe",4.6,True,None),
    ("Lavazza Espresso Italiano Ground Coffee 250g","Lavazza","A rich blend of Arabica and Robusta — Italy's No.1 espresso coffee.",2,28.00,None,4.7,True,None),
    ("Milo Energy Chocolate Drink Powder 400g","Nestle","Chocolate malt drink for growing kids — packed with energy and vitamins.",2,16.00,"nesquik",4.6,True,None),
    ("Nesquik Chocolate Powder 400g","Nestle","Instant chocolate milk powder — add to milk for a delicious drink.",2,14.50,"nesquik",4.5,True,None),
    ("Karak Chai Masala Spiced Tea 250g","Local Brand","Aromatic spiced tea blend — cardamom, ginger, and cloves. The Gulf's favourite morning drink.",2,12.00,None,4.8,True,None),
    # ── Grocery – Bread & Bakery (2) ─────────────────────────────────────────
    ("L'usine Brioche Rolls 6 Pack","Almarai","Soft, buttery brioche rolls — ideal for sliders and breakfast.",2,8.00,None,4.5,True,None),
    ("Almarai Brown Toast Bread 500g","Almarai","Wholegrain brown toast bread — fibre-rich and nutritious.",2,6.00,None,4.5,True,None),
    ("Sesame Arabic Bread Kaak 250g","Local Bakery","Crunchy sesame ring bread — a Levantine snack enjoyed across Qatar.",2,4.00,None,4.4,True,None),
    # ── Grocery – Breakfast & Cereals (2) ────────────────────────────────────
    ("Kellogg's Corn Flakes 500g","Kellogg's","The original breakfast cereal — crunchy, light, and great with cold milk.",2,12.00,None,4.5,True,None),
    ("Kellogg's Frosties 375g","Kellogg's","Sugar-frosted corn flakes — the sweet breakfast favourite for kids.",2,12.00,None,4.5,True,None),
    ("Quaker Oats Original 1kg","PepsiCo","100% whole grain rolled oats — a nutritious, filling breakfast.",2,14.00,None,4.6,True,None),
    ("Kellogg's Special K Red Berries 375g","Kellogg's","Light and crispy cereal with dried strawberries — a balanced breakfast choice.",2,14.00,None,4.5,True,None),
    ("Weetabix Original 24 Biscuits","Weetabix","Whole grain wheat biscuits — a high-fibre UK classic loved across Qatar.",2,12.00,None,4.5,True,None),
    ("Kellogg's Coco Pops 375g","Kellogg's","Chocolate puffed rice cereal that turns your milk chocolatey.",2,12.00,None,4.6,True,None),
    ("Alpen Original Muesli 750g","Weetabix","Rolled oats with nuts, dried fruit, and wheatflakes — a nutritious start.",2,16.00,None,4.5,True,None),
    ("Nature Valley Crunchy Oats & Honey 5 Bars","General Mills","Crunchy granola bars with whole grain oats and pure honey.",2,8.50,None,4.5,True,None),
    # ── Grocery – Condiments & Sauces (2) ────────────────────────────────────
    ("Maggi Chicken Stock Cubes 20 Pack","Nestle","Essential kitchen stock cubes — adds deep, savoury chicken flavour instantly.",2,5.50,None,4.5,True,None),
    ("Tabasco Red Pepper Sauce 150ml","McIlhenny","The original Louisiana hot sauce — tangy, spicy, and all-natural.",2,12.00,None,4.6,True,None),
    ("Nando's Peri-Peri Sauce Medium 275g","Nando's","The famous medium peri-peri sauce from Nando's. Great as a marinade or dip.",2,14.00,None,4.7,True,None),
    ("Hellmann's Light Mayonnaise 400g","Unilever","All the creaminess of Hellmann's with less fat. Ideal for health-conscious eaters.",2,13.00,None,4.5,True,None),
    ("Lee Kum Kee Oyster Sauce 255ml","Lee Kum Kee","Premium Chinese oyster sauce — adds rich umami depth to stir-fries.",2,7.50,None,4.6,True,None),
    ("Kikkoman Naturally Brewed Soy Sauce 150ml","Kikkoman","Japan's finest naturally brewed soy sauce — smooth, deep flavour.",2,8.00,None,4.7,True,None),
    ("Emirates Tahini Sesame Paste 400g","Emirates","Pure roasted sesame paste — essential for hummus, salad dressings, and dips.",2,10.00,None,4.6,True,None),
    ("Mina Harissa Paste 135g","Mina","Authentic Moroccan harissa — smoky chilli paste with olive oil and spices.",2,8.00,None,4.5,True,None),
    ("Al Alali Tomato Paste 135g","Al Alali","Concentrated tomato paste — rich, deep flavour for sauces and stews.",2,3.00,None,4.4,True,None),
    ("HP Brown Sauce 425g","H.J. Heinz","The classic British brown sauce — tangy, spiced, and loved in Qatar's expat community.",2,10.00,"heinz",4.5,True,None),
    # ── Grocery – Rice, Pasta & Grains (2) ───────────────────────────────────
    ("Daawat Super Basmati Rice 5kg","Daawat","Long-grain aromatic basmati from India's premier rice brand. Perfect for machboos.",2,32.00,"tilda",4.7,True,None),
    ("Spaghetti Barilla No.5 500g","Barilla","Italy's best-selling pasta — durum wheat semolina, perfectly textured.",2,5.00,None,4.6,True,None),
    ("Penne Rigate Pasta Barilla 500g","Barilla","Classic ridged penne — holds sauces beautifully. Al dente every time.",2,5.00,None,4.5,True,None),
    ("Fusilli Pasta Barilla 500g","Barilla","Spiral pasta that traps chunky sauces. Great for pasta salads.",2,5.00,None,4.5,True,None),
    ("Egyptian Short Grain Rice 5kg","Local Brand","Short-grain rice ideal for stuffed vegetables and Middle Eastern dishes.",2,22.00,None,4.4,True,None),
    ("Red Lentils 1kg","Local Brand","Split red lentils — cook quickly, perfect for dal and lentil soup.",2,6.00,None,4.5,True,None),
    ("Chickpeas Dried 1kg","Local Brand","Dried chickpeas — the base for hummus, falafel, and fatteh.",2,7.00,None,4.4,True,None),
    ("Couscous Medium Grain 500g","Local Brand","Quick-cook medium couscous — ready in 5 minutes, great with tagines.",2,8.00,None,4.4,True,None),
    # ── Grocery – Canned & Packaged (2) ──────────────────────────────────────
    ("Heinz Baked Beans in Tomato Sauce 415g","Kraft Heinz","Classic British baked beans — a quick, protein-rich meal on toast.",2,6.00,"heinz",4.5,True,None),
    ("John West Tuna in Springwater 185g","Thai Union","Sustainably sourced tuna fillet in spring water. High protein, low fat.",2,7.50,None,4.5,True,None),
    ("Al Alali Sardines in Tomato Sauce 125g","Al Alali","Tender sardines in rich tomato sauce — a Gulf pantry staple.",2,4.00,None,4.3,True,None),
    ("Cirio Crushed Tomatoes 400g","Cirio","Premium Italian crushed tomatoes — sun-ripened, for pasta sauces.",2,5.00,None,4.5,True,None),
    ("Green Giant Sweetcorn 340g Can","General Mills","Tender whole kernel sweetcorn — great for salads, soups, and sides.",2,4.50,None,4.4,True,None),
    ("Eagle Brand Sweetened Condensed Milk 397g","Borden","Rich condensed milk — essential for desserts, karak tea, and Arabic sweets.",2,6.00,None,4.6,True,None),
    # ── Grocery – Frozen Foods (2) ────────────────────────────────────────────
    ("McCain Crinkle Cut Oven Chips 750g","McCain","Easy oven-baked crinkle cut chips — crispy outside, fluffy inside.",2,14.00,None,4.5,True,None),
    ("Americana Chicken Nuggets 400g","Americana","Juicy Halal chicken nuggets — kids' all-time favourite. Oven or air-fryer ready.",2,18.00,None,4.6,True,None),
    ("Sadia Chicken Wings Frozen 1kg","Sadia","Halal-certified IQF chicken wings — perfect for grilling or air-frying.",2,22.00,None,4.5,True,None),
    ("Birds Eye Garden Peas 900g","Nomad Foods","Sweet garden peas — picked at peak freshness and frozen within hours.",2,10.00,None,4.4,True,None),
    ("Al Kabeer Beef Burger Patties 8 Pack","Al Kabeer","Juicy Halal beef burgers — ready in minutes on the grill or pan.",2,28.00,None,4.5,True,None),
    ("Americana Beef Kofta Frozen 400g","Americana","Spiced minced beef kofta — grill or bake for a quick Middle Eastern dinner.",2,18.00,None,4.5,True,None),
    # ── Grocery – Chocolate & Confectionery (2) ───────────────────────────────
    ("Lindt Excellence Dark 70% 100g","Lindt & Sprungli","Intense dark chocolate with deep cocoa notes. Smooth Swiss finish.",2,12.00,"lindt70",4.8,True,None),
    ("Lindt Excellence Dark 85% 100g","Lindt & Sprungli","Extra-dark 85% cocoa — rich, bittersweet, and deeply satisfying.",2,12.00,"lindt85",4.7,True,None),
    ("Bounty Coconut & Chocolate Bar 57g","Mars","Creamy coconut covered in smooth milk chocolate. A Gulf classic.",2,4.00,None,4.5,True,None),
    ("Galaxy Milk Chocolate Bar 42g","Mars","Exceptionally smooth milk chocolate with a velvety melt. Popular in Qatar.",2,4.00,None,4.6,True,None),
    ("After Eight Mint Chocolate Thins 200g","Nestle","Crisp mint fondant in dark chocolate. The iconic after-dinner treat.",2,18.00,None,4.7,True,None),
    ("Ferrero Rocher Assorted 16 Pieces","Ferrero","Hazelnut chocolate spheres in a classic gold box — the ultimate Qatar gift.",2,32.00,None,4.9,True,None),
    ("Toblerone Milk Chocolate 100g","Mondelez","Iconic Swiss milk chocolate with honey-almond nougat. Triangular peaks.",2,10.00,None,4.7,True,None),
    ("Kinder Bueno Milk Chocolate Wafer 2 Bars","Ferrero","Light, crispy wafer with a creamy hazelnut filling, dipped in chocolate.",2,4.50,None,4.7,True,None),
    ("Raffaello White Coconut Balls 150g","Ferrero","Delicate coconut-almond confections — a popular Qatar gifting choice.",2,18.00,None,4.7,True,None),
    ("Haribo Gold Bears 100g","Haribo","The world's most famous gummy bears — fruity, chewy, and fun for all ages.",2,5.00,None,4.5,True,None),
    ("Oreo Original Sandwich Cookies 154g","Mondelez","The classic twist, lick, and dunk cookie. Crispy cocoa wafers with vanilla cream.",2,7.00,None,4.7,True,None),
    ("McVitie's Digestive Biscuits Original 250g","Pladis","Wholesome wheat biscuits with a slightly sweet, nutty flavour.",2,8.00,None,4.5,True,None),
    ("Bahlsen Hit Chocolate Sandwich Biscuits 220g","Bahlsen","Buttery biscuits sandwiched with smooth chocolate cream.",2,9.00,"tuc",4.5,True,None),
    ("Ritz Crackers Original 200g","Mondelez","Light, buttery crackers — great with cheese, dips, or plain.",2,8.00,"tuc",4.6,True,None),
    # ── Grocery – Chips & Snacks (2) ─────────────────────────────────────────
    ("Doritos Flamin' Hot 260g","PepsiCo","Fiery Flamin' Hot flavour on Doritos' iconic tortilla chips.",2,12.00,None,4.4,True,None),
    ("Cheetos Flamin' Hot 227g","PepsiCo","Dangerously cheesy — intensely flavoured puffed corn snacks.",2,10.00,"pringles",4.4,True,None),
    ("Lay's Sour Cream & Onion 45g","PepsiCo","Small snack bag of tangy sour cream and onion crisps — perfect for on the go.",2,3.50,None,4.4,True,None),
    ("Pringles BBQ 165g","Kellogg's","Sweet and smoky BBQ seasoning on Pringles' signature stackable chip.",2,11.00,"pringles",4.5,True,None),
    ("Wasa Crispy Rye Bread 260g","Barilla","Light, crispy rye crispbread — great with labneh, cheese, or avocado.",2,12.00,"wasa",4.5,True,None),
    ("Tuc Original Butter Biscuits 100g","Mondelez","Light, savoury crackers with a buttery taste. A popular Qatar snack.",2,4.50,"tuc",4.4,True,None),
    # ── Grocery – Spreads & Cooking (2) ──────────────────────────────────────
    ("Smucker's Strawberry Jam 350g","Smucker's","Made from sun-ripened strawberries — no high-fructose corn syrup.",2,12.00,None,4.6,True,None),
    ("Bonne Maman Raspberry Jam 370g","Bonne Maman","Artisan-style French raspberry jam with whole fruit pieces.",2,15.00,None,4.7,True,None),
    ("Skippy Peanut Butter Smooth 340g","Hormel","Smooth and creamy peanut butter — great on toast, in smoothies, or with dates.",2,12.00,None,4.6,True,None),
    ("Lotus Biscoff Spread Smooth 380g","Lotus","The iconic Belgian cookie butter spread — unique caramelised biscuit flavour.",2,18.00,None,4.8,True,None),
    ("Nutella Hazelnut Spread 750g","Ferrero","Large jar of the world's favourite spread — for generous portions.",2,32.00,"nutella",4.9,True,None),
    ("Pure Sidr Honey 500g","Local Farm","Raw Sidr honey from Yemen — one of the world's finest honeys.",2,65.00,None,4.9,True,None),
    ("Al Shifa Natural Honey 500g","Al Shifa","Premium natural honey from Saudi Arabia — a Qatar pantry staple.",2,28.00,None,4.7,True,None),
    ("Bertolli Extra Virgin Olive Oil 500ml","Bertolli","Cold-pressed extra virgin olive oil from sun-ripened Italian olives.",2,22.00,None,4.6,True,None),
    ("Afia Sunflower Oil 1.5L","Savola","Refined sunflower oil — light, neutral flavour for everyday cooking.",2,8.50,None,4.4,True,None),
    ("Shan Biryani Masala 60g","Shan","Authentic biryani spice mix — brings the flavour of South Asian kitchens to Doha.",2,5.00,None,4.6,True,None),
    # ── Health & Beauty (3) ───────────────────────────────────────────────────
    ("Omega-3 Fish Oil 1000mg 60 Softgels","Holland & Barrett","Supports heart, brain, and joint health. Odourless softgels.",3,35.00,None,4.6,True,None),
    ("Vitamin D3 5000 IU 60 Softgels","NOW Foods","Bone, immune, and mood support — especially important in Qatar's indoor lifestyle.",3,28.00,None,4.7,True,None),
    ("Biotin 10000mcg Hair & Nail Vitamins 60 Capsules","Sports Research","High-potency biotin — promotes hair growth, strong nails, and glowing skin.",3,38.00,None,4.6,True,None),
    ("Probiotics 50 Billion CFU 30 Capsules","Garden of Life","Ten probiotic strains — supports gut health and immune balance.",3,55.00,None,4.7,True,None),
    ("Collagen Type 1 & 3 1000mg 60 Tablets","Neocell","Marine collagen for skin elasticity, joint support, and anti-ageing.",3,55.00,None,4.6,True,None),
    ("Centrum Women Multivitamin 30 Tablets","Pfizer","Complete daily multivitamin for women — iron, folic acid, and 23 nutrients.",3,45.00,None,4.5,True,None),
    ("Berocca Performance B-Vitamins 15 Effervescent","Bayer","B-vitamins, Vitamin C, and minerals for energy and mental sharpness.",3,28.00,None,4.5,True,None),
    ("Calcium + Vitamin D3 1200mg 60 Tablets","Nature Made","Supports strong bones and teeth. Essential for Qatar's sun-limited indoor workers.",3,32.00,None,4.6,True,None),
    ("Turmeric Curcumin 500mg 60 Capsules","Solgar","Anti-inflammatory turmeric with black pepper for maximum absorption.",3,45.00,None,4.6,True,None),
    ("Melatonin 5mg Sleep Support 60 Tablets","Natrol","Hormone-free sleep aid — helps regulate sleep cycle for shift workers and travellers.",3,28.00,None,4.5,True,None),
    ("CeraVe Moisturising Cream 177g","L'Oreal","Dermatologist-recommended ceramide moisturiser for dry and sensitive skin.",3,55.00,None,4.8,True,None),
    ("Cetaphil Gentle Skin Cleanser 500ml","Galderma","Soap-free, fragrance-free cleanser for sensitive skin. Dermatologist trusted.",3,38.00,None,4.7,True,None),
    ("The Ordinary Niacinamide 10% + Zinc 1% 30ml","DECIEM","Minimises pores, balances sebum, and reduces blemishes.",3,19.00,None,4.7,True,None),
    ("The Ordinary Hyaluronic Acid 2% + B5 30ml","DECIEM","Multi-depth hydration serum with hyaluronic acid and vitamin B5.",3,19.00,None,4.7,True,None),
    ("Olay Regenerist Retinol24 Day Cream SPF30 50g","P&G","Retinol-powered anti-ageing moisturiser with broad-spectrum SPF30.",3,65.00,None,4.6,True,None),
    ("Nivea Body Lotion Shea Butter 400ml","Beiersdorf","48-hour moisture with rich shea butter. Absorbs quickly, non-greasy.",3,15.00,None,4.6,True,None),
    ("Palmer's Cocoa Butter Formula Lotion 250ml","Palmer's","Pure cocoa butter with vitamin E — repairs dry, rough skin.",3,14.00,None,4.5,True,None),
    ("Bioderma Sensibio H2O Micellar Water 500ml","Naos","France's No.1 micellar water — gentle make-up remover for sensitive skin.",3,38.00,None,4.8,True,None),
    ("Neutrogena Norwegian Formula Hand Cream 75g","J&J","Clinically proven to heal very dry hands overnight. Fragrance-free.",3,18.00,None,4.7,True,None),
    ("Vaseline Intensive Care Lotion 400ml","Unilever","Microdroplets of Vaseline Jelly penetrate 5 skin layers for deep healing.",3,12.00,None,4.6,True,None),
    ("TRESemmé Keratin Smooth Shampoo 400ml","Unilever","Keratin-infused formula for frizz-free, smooth hair in Qatar's humidity.",3,18.00,None,4.5,True,None),
    ("Garnier Fructis Strengthening Shampoo 400ml","L'Oreal","Caffeine and plant protein strengthen brittle hair from root to tip.",3,16.00,None,4.5,True,None),
    ("Schwarzkopf Gliss Hair Repair Conditioner 400ml","Henkel","Liquid keratin repair conditioner — instant smoothness, reduced breakage.",3,18.00,None,4.5,True,None),
    ("OGX Coconut Milk Shampoo 385ml","Johnson Products","Coconut milk and coconut oil — deeply nourishes dry, frizzy hair.",3,22.00,None,4.6,True,None),
    ("Elvive Extraordinary Oil Shampoo 400ml","L'Oreal","Six precious oils for radiant, silky hair without weighing it down.",3,18.00,None,4.5,True,None),
    ("Sensodyne Pronamel Whitening Toothpaste 75ml","GSK","Protects against acid erosion while gently whitening sensitive teeth.",3,19.00,None,4.7,True,None),
    ("Colgate MaxFresh Toothpaste 125g","Colgate-Palmolive","Micro-whitening crystals for a cool, fresh breath sensation.",3,9.00,None,4.5,True,None),
    ("Listerine Total Care Mouthwash 500ml","J&J","Kills 99.9% of germs, freshens breath, and strengthens enamel.",3,18.00,None,4.6,True,None),
    ("Oral-B Advantage Toothbrush 3 Pack","P&G","Indicator bristles show when it's time to replace. Soft for sensitive gums.",3,18.00,None,4.5,True,None),
    ("Dove Men+Care Clean Comfort Deodorant 150ml","Unilever","48-hour protection with moisturising cream. Non-irritating formula.",3,14.00,None,4.6,True,None),
    ("Rexona Men Motionsense Active Deodorant 200ml","Unilever","Motion-activated freshness — keeps you dry through Qatar's summer heat.",3,14.00,None,4.5,True,None),
    ("Gillette Mach3 Sensitive Razor","P&G","Three-blade razor with comfort guard — gentle on sensitive skin.",3,22.00,None,4.6,True,None),
    ("Veet Suprem Essence Hair Removal Cream 200ml","Reckitt","Fast-acting hair removal for the body. Visible results in 5 minutes.",3,18.00,None,4.3,True,None),
    ("Johnsons Baby Oil 300ml","J&J","Pure mineral baby oil — gentle enough for babies, loved by adults for skin care.",3,12.00,None,4.6,True,None),
    ("Strepsils Sore Throat Lozenge Honey & Lemon 24 Pack","Reckitt","Soothing honey and lemon lozenges for sore throat relief.",3,12.00,None,4.5,True,None),
    ("Voltaren Emulgel 1.16% Pain Relief Gel 100g","Haleon","Deep-penetrating NSAID gel for targeted joint and muscle pain relief.",3,28.00,None,4.7,True,None),
    # ── Electronics (4) ───────────────────────────────────────────────────────
    ("Samsung Galaxy S24 256GB Phantom Black","Samsung","Snapdragon 8 Gen 3, 50MP ProVisual camera, 7 years of OS updates.",4,2999.00,None,4.8,True,None),
    ("Apple iPhone 16 128GB Black","Apple","A18 chip, Camera Control button, and improved low-light photography.",4,3499.00,None,4.9,True,None),
    ("Xiaomi 14 Ultra 512GB White","Xiaomi","Leica optics, Snapdragon 8 Gen 3, 90W HyperCharge. Premium flagship.",4,3299.00,None,4.7,True,None),
    ("Apple iPad Air 11-inch M2 128GB","Apple","M2 chip, 11-inch Liquid Retina display, compatible with Apple Pencil Pro.",4,2299.00,None,4.8,True,None),
    ("Samsung Galaxy Tab S9 FE 128GB","Samsung","6GB RAM, 10.9-inch display, S Pen included. Samsung DeX support.",4,1299.00,None,4.6,True,1499.00),
    ("Bose QuietComfort 45 Wireless Headphones","Bose","World-class noise cancellation with 24-hour battery life.",4,1299.00,None,4.8,True,1499.00),
    ("Logitech MX Master 3S Mouse","Logitech","8000 DPI sensor, MagSpeed scroll wheel, works on any surface.",4,299.00,None,4.8,True,None),
    ("Logitech MX Keys Advanced Wireless Keyboard","Logitech","Smart illuminated keys, perfect stroke depth, multi-device connection.",4,399.00,None,4.7,True,None),
    ("Marshall Emberton II Portable Speaker","Marshall","IP67 waterproof, 30-hour playtime, 360-degree sound.",4,499.00,None,4.8,True,None),
    ("Google Nest Mini 2nd Gen Smart Speaker","Google","Compact smart speaker with Google Assistant — controls smart home with voice.",4,149.00,None,4.5,True,None),
    ("Amazon Echo Dot 5th Gen Smart Speaker","Amazon","Alexa voice control, improved sound, smart home hub built-in.",4,149.00,None,4.5,True,None),
    ("TP-Link Tapo Smart WiFi Plug 4 Pack","TP-Link","Control devices via app or voice. Schedule timers and monitor energy use.",4,89.00,None,4.6,True,None),
    ("Philips Hue White Smart Bulb E27 Starter Kit","Signify","3 smart LED bulbs + Hue Bridge — full white ambiance control.",4,249.00,None,4.7,True,None),
    ("Ring Video Doorbell Wired","Amazon","1080p HD video doorbell with live view and motion detection.",4,299.00,None,4.6,True,None),
    ("GoPro HERO12 Black Action Camera","GoPro","5.3K video, HyperSmooth 6.0 stabilisation, 27m waterproof.",4,1399.00,None,4.8,True,None),
    ("Anker 65W USB-C GaN Compact Charger","Anker","Powers a laptop and two devices simultaneously from one compact plug.",4,89.00,None,4.7,True,None),
    ("Anker 737 Power Bank 140W 24000mAh","Anker","Laptop-grade power bank — charges MacBook Pro from 0% to 50% in 43 minutes.",4,299.00,None,4.7,True,None),
    ("Kingston DataTraveler 64GB USB 3.2 Flash Drive","Kingston","Fast 200MB/s read speeds, durable metal casing, compact design.",4,29.00,None,4.5,True,None),
    ("PlayStation 5 DualSense Controller White","Sony","Haptic feedback, adaptive triggers, built-in microphone for PS5.",4,279.00,None,4.8,True,None),
    ("Xbox Wireless Controller Carbon Black","Microsoft","Textured grip, Bluetooth 5.2, USB-C charging, 40-hour battery life.",4,229.00,None,4.7,True,None),
    ("Spigen Rugged Armor Case iPhone 16","Spigen","Military-grade drop protection with carbon fibre design.",4,59.00,None,4.7,True,None),
    ("Belkin Boost Up Charge 15W Wireless Pad","Belkin","15W fast wireless charging for iPhone 15 and MagSafe compatible cases.",4,89.00,None,4.5,True,None),
    # ── Fashion & Accessories (5) ─────────────────────────────────────────────
    ("Nike Air Force 1 Low White","Nike","The timeless AF1 in triple white — the most iconic sneaker in Qatar.",5,349.00,None,4.8,True,None),
    ("Adidas Gazelle Navy Blue","Adidas","The classic Adidas Gazelle suede trainer — minimalist, versatile, retro.",5,289.00,None,4.7,True,None),
    ("New Balance 574 Grey","New Balance","Heritage runner with EVA foam cushioning — comfort meets street style.",5,299.00,None,4.6,True,None),
    ("Converse Chuck Taylor All Star Hi White","Converse","The all-time classic high-top canvas sneaker. Pairs with everything.",5,219.00,None,4.7,True,None),
    ("Vans Old Skool Classic Black White","Vans","The skate-born classic with signature side stripe. Iconic and durable.",5,229.00,None,4.7,True,None),
    ("Timberland 6-Inch Premium Wheat Boots","Timberland","Waterproof nubuck leather, padded collar, rubber lug sole — built to last.",5,599.00,None,4.7,True,None),
    ("Levi's 511 Slim Fit Jeans Dark Blue","Levi's","The perfect slim — sits below waist, slim through thigh and leg.",5,299.00,None,4.7,True,None),
    ("Ralph Lauren Polo Classic Fit T-Shirt White","Ralph Lauren","Iconic pony-embroidered soft cotton jersey tee. A Doha wardrobe essential.",5,149.00,None,4.7,True,None),
    ("Lacoste Regular Fit Polo Shirt White","Lacoste","The classic petit piqué cotton polo — timeless style from the crocodile brand.",5,299.00,None,4.7,True,None),
    ("Nike Sportswear Club Fleece Hoodie Grey","Nike","Heavyweight fleece for cool Gulf evenings. Kangaroo pocket and drawcord hood.",5,219.00,None,4.6,True,None),
    ("Herschel Classic Backpack 25L Navy","Herschel","Laptop sleeve, organiser pocket, and retro styling in durable fabric.",5,249.00,None,4.6,True,None),
    ("Samsonite Spinner Trolley 68cm Graphite","Samsonite","4-wheel spinner trolley with TSA lock. Hardshell, lightweight.",5,849.00,None,4.7,True,None),
    ("Fossil Minimalist Slim Watch Rose Gold","Fossil","Three-hand date display, rose gold-tone stainless steel bracelet.",5,699.00,None,4.5,True,None),
    ("Daniel Wellington Classic Petite Watch Rose Gold","Daniel Wellington","Ultra-slim Scandinavian design with interchangeable NATO strap.",5,599.00,None,4.6,True,None),
    ("Pandora Moments Curb Chain Bracelet Silver","Pandora","Sterling silver curb chain bracelet — pairs with all Pandora charms.",5,199.00,None,4.7,True,None),
    ("Oakley Holbrook Polarized Sunglasses","Oakley","High-Definition Optics, Plutonite lens, O-Matter frame. UV protection.",5,649.00,None,4.8,True,None),
    # ── Home & Garden (6) ────────────────────────────────────────────────────
    ("Philips Air Fryer Essential 4.1L","Philips","Rapid Air technology — fry, bake, grill, and roast with little to no oil.",6,299.00,None,4.7,True,349.00),
    ("Instant Pot Duo 7-in-1 6L Pressure Cooker","Instant Brands","Pressure cooker, slow cooker, rice cooker, steamer — all in one.",6,449.00,None,4.8,True,None),
    ("Nespresso Vertuo Next Coffee Machine","Nestle","Centrifusion technology brews coffee and espresso with one button.",6,499.00,None,4.7,True,None),
    ("Vitamix E310 Explorian Blender","Vitamix","Professional-grade blending — soups, smoothies, and nut butters in seconds.",6,899.00,None,4.8,True,None),
    ("Russell Hobbs Heritage Kettle 1.7L Black","Russell Hobbs","Rapid boil technology — boils one cup in 45 seconds.",6,89.00,None,4.5,True,None),
    ("Smeg 50s Style 4-Slice Toaster Cream","Smeg","Retro design, six browning settings, extra-wide slots for thick bread.",6,399.00,None,4.6,True,None),
    ("Le Creuset Signature Casserole 24cm Volcanic","Le Creuset","Enamelled cast iron — even heat distribution, lifetime guarantee.",6,699.00,None,4.9,True,None),
    ("Zwilling Pro Chef Knife 20cm","Zwilling","Precision-forged from single piece of steel. The kitchen workhorse.",6,299.00,None,4.8,True,None),
    ("OXO Good Grips Non-Stick Pro Skillet 30cm","OXO","Textured surface for better searing, German Whitford non-stick coating.",6,149.00,None,4.7,True,None),
    ("Tupperware Modular Mates Set 5 Pcs","Tupperware","Airtight pantry storage containers — keeps grains and spices fresh.",6,99.00,None,4.6,True,None),
    ("Persil Automatic Washing Liquid 3L","Henkel","Powerful stain removal in cold water. Formulated for Gulf hard water.",6,38.00,None,4.6,True,45.00),
    ("Comfort Blue Sky Fabric Conditioner 3L","Unilever","Long-lasting fragrance, softens fabrics, and reduces ironing time.",6,22.00,None,4.5,True,None),
    ("Fairy Original Washing Up Liquid 1L","P&G","Powerful grease-cutting formula — the UK's No.1 washing up liquid.",6,8.50,None,4.7,True,None),
    ("Dyson V12 Detect Slim Cordless Vacuum","Dyson","Laser reveals microscopic dust. 60-minute runtime, LCD screen.",6,2299.00,None,4.8,True,2599.00),
    ("Philips HR2157 Hand Blender 700W","Philips","Stainless steel shaft, 21-speed settings, splash control bell.",6,149.00,None,4.6,True,None),
    ("Lysol Disinfectant Spray Crisp Linen 450g","Reckitt","Kills 99.9% of viruses and bacteria on hard and soft surfaces.",6,22.00,None,4.6,True,None),
    ("Febreze Fabric Refresher Extra Strength 500ml","P&G","Eliminates deep-set odours from fabrics — sofas, curtains, carpets.",6,14.00,None,4.5,True,None),
    ("Yankee Candle Clean Cotton Large Jar 623g","Yankee Candle","Classic clean, linen-fresh fragrance. 110-150 hours burn time.",6,89.00,None,4.7,True,None),
    ("Miracle-Gro All Purpose Plant Food 2kg","Scotts","Feeds plants instantly — for flowers, vegetables, and trees.",6,28.00,None,4.5,True,None),
    ("IKEA SOCKER Plant Pot Set 3 Pcs White","IKEA","Simple terracotta pots with saucers — ideal for small indoor plants.",6,25.00,None,4.4,True,None),
    # ── Toys & Kids (7) ──────────────────────────────────────────────────────
    ("LEGO City Police Station 60316","LEGO","668 pieces, multiple minifigures, detailed police station build. Ages 6+.",7,199.00,None,4.8,True,None),
    ("LEGO Duplo Classic Brick Box 10913","LEGO","80 DUPLO bricks in bright colours — open-ended creative play for toddlers.",7,119.00,None,4.8,True,None),
    ("LEGO Creator 3-in-1 Cute Dog 31137","LEGO","Builds into a dog, cat, or rabbit — 3 models from one set. Ages 6+.",7,69.00,None,4.7,True,None),
    ("Marvel Spider-Man 30cm Titan Hero Figure","Hasbro","Large-scale articulated action figure with web-shooting accessory.",7,69.00,None,4.6,True,None),
    ("Barbie Dreamhouse 3-Story Dollhouse","Mattel","70+ accessories, pool with slide, working elevator. The ultimate Barbie home.",7,599.00,None,4.8,True,None),
    ("Frozen II Elsa Fashion Doll with Dress","Mattel","Elsa doll in her iconic ice-blue dress from Frozen II.",7,69.00,None,4.7,True,None),
    ("Monopoly Classic Board Game","Hasbro","The world's most beloved property trading game — the classic edition.",7,75.00,None,4.6,True,None),
    ("Catan Base Board Game","Catan Studio","Strategic settlement-building game for 3-4 players. Ages 10+.",7,89.00,None,4.8,True,None),
    ("Scrabble Original Classic Word Game","Mattel","The timeless word game — 100 premium tiles, rotating board.",7,69.00,None,4.6,True,None),
    ("1000-Piece Jigsaw Puzzle Doha Skyline","Ravensburger","Striking Doha skyline puzzle — 1000 pieces for teens and adults.",7,55.00,None,4.5,True,None),
    ("Fisher-Price Brilliant Basics Baby Gym","Mattel","Colourful activity gym with hanging toys — encourages early motor skills.",7,95.00,None,4.7,True,None),
    ("Pampers Baby-Dry Diapers Size 3 70 Pieces","P&G","Extra-large pack of Pampers — up to 12 hours dryness for babies 4-9kg.",7,70.00,None,4.8,True,None),
    ("Huggies Ultra Comfort Diapers Size 5 44 Pieces","Kimberly-Clark","Comfortable fit with DryTouch lining — ideal for active babies.",7,65.00,None,4.7,True,None),
    ("Similac Gold Stage 2 Baby Formula 900g","Abbott","Follow-on formula for babies 6-12 months. HMO prebiotics.",7,175.00,None,4.7,True,None),
    ("Aptamil Gold+ Stage 1 Infant Formula 900g","Nutricia","Expert-level nutrition with DHA and ARA — supports brain development.",7,195.00,None,4.7,True,None),
    ("Nerf Elite 2.0 Blaster Commander","Hasbro","8-dart rotating drum, foldable stock, tactical rail. Accuracy and power.",7,75.00,None,4.7,True,None),
    ("Razor A2 Kick Scooter Red","Razor","Lightweight aluminium scooter, rear fender brake, folding T-bar. Ages 5+.",7,149.00,None,4.6,True,None),
    ("Playmobil City Life School 71328","Playmobil","Detailed school set with 3 figures, classroom, and outdoor area. Ages 4+.",7,149.00,None,4.7,True,None),
    ("Melissa & Doug Wooden Puzzle Set 6 Pack","Melissa & Doug","Six chunky wooden puzzles — animals, shapes, and numbers for toddlers.",7,65.00,None,4.7,True,None),
    ("VTech Baby Musical Learning Walker","VTech","Interactive walking toy with music, lights, and learning activities.",7,89.00,None,4.6,True,None),
    # ── Sports & Outdoors (8) ─────────────────────────────────────────────────
    ("Adidas Al Rihla Pro FIFA Quality Football","Adidas","Official match ball of the FIFA World Cup Qatar 2022. Size 5.",8,199.00,None,4.9,True,None),
    ("Nike Premier League Strike Football","Nike","Durable match ball with high-visibility graphics. Size 5.",8,99.00,None,4.6,True,None),
    ("Spalding NBA Official Game Basketball Size 7","Spalding","Full-grain leather, deep channel design — the ball of the NBA.",8,299.00,None,4.7,True,None),
    ("Brooks Ghost 15 Men's Running Shoes","Brooks","Plush cushioning, balanced ride — Qatar runners' top choice.",8,549.00,None,4.8,True,None),
    ("Garmin Forerunner 265 GPS Running Watch","Garmin","AMOLED display, advanced training metrics, 13-day battery life.",8,1299.00,None,4.8,True,None),
    ("Optimum Nutrition Gold Standard Whey 2.27kg","Optimum Nutrition","24g protein per serving, low fat and carbs. 5g BCAAs, 4g glutamine.",8,199.00,None,4.8,True,219.00),
    ("BSN Syntha-6 Protein Powder Chocolate 2.27kg","BSN","Multi-functional protein matrix — great taste, sustained release.",8,189.00,None,4.6,True,None),
    ("Quest Protein Bars Chocolate Chip Cookie 12 Pack","Quest Nutrition","21g protein, 1g sugar, 150 calories — Qatar's favourite protein bar.",8,89.00,None,4.7,True,None),
    ("Manduka PRO Yoga Mat 6mm Black","Manduka","Dense, non-slip lifetime-guarantee yoga mat — loved by Qatar's yoga community.",8,399.00,None,4.8,True,None),
    ("Speedo Futura Classic Swim Goggles","Speedo","Anti-fog, UV protection, comfortable rubber seal — ideal for Doha's pools.",8,45.00,None,4.6,True,None),
    ("Wilson US Open Tennis Balls 3 Pack","Wilson","Official ball of the US Open — consistent bounce, durable felt.",8,22.00,None,4.6,True,None),
    ("TRX All-in-One Suspension Training System","TRX","Full-body workout with a single anchor point — used by Qatar's personal trainers.",8,349.00,None,4.7,True,None),
    ("Bowflex SelectTech 552 Adjustable Dumbbell","Bowflex","Replaces 15 pairs of dumbbells — 2.5kg to 24kg in one dumbbell.",8,1299.00,None,4.7,True,None),
    ("Gatorade Sports Drink Orange 600ml","PepsiCo","Electrolyte sports drink — fuels performance in Qatar's extreme heat.",8,6.50,None,4.5,True,None),
    ("Clif Bar Energy Bar Chocolate Brownie 12 Pack","Clif","Organic oats, 9g protein — sustained energy for training sessions.",8,79.00,None,4.6,True,None),
    ("Cressi Clio Mask & Finn Snorkel Set","Cressi","Crystal-clear lens, Italian-made silicone seal — for Qatar's sea activities.",8,89.00,None,4.6,True,None),
    ("Compression Running Socks Calf High 3 Pack","2XU","Graduated compression for improved circulation and faster recovery.",8,45.00,None,4.5,True,None),
    ("MSR Hubba Hubba NX 2-Person Tent","MSR","Ultra-light 1.72kg, freestanding, fully seam-taped — for Qatar camping.",8,1199.00,None,4.8,True,None),
    # ── Pets (9) ──────────────────────────────────────────────────────────────
    ("Royal Canin Persian Adult Dry Cat Food 2kg","Royal Canin","Specifically shaped kibble for Persian cats' flat face and jaw structure.",9,119.00,None,4.8,True,None),
    ("Hill's Science Diet Adult Indoor Cat Food 3.6kg","Hill's","Clinically proven nutrition — reduces hairballs and maintains lean muscle.",9,145.00,None,4.7,True,None),
    ("Sheba Perfect Portions Tuna & Salmon 24 Pack","Mars Petcare","Single-serve premium wet cat food — no preservatives, no artificial flavours.",9,85.00,None,4.8,True,None),
    ("Temptations Classic Chicken Cat Treats 85g","Mars Petcare","Crunchy outside, soft inside. Cats go crazy for these in Qatar.",9,15.00,None,4.7,True,None),
    ("Catit Pixi Smart Automatic Feeder","Catit","WiFi-connected smart feeder — schedule meals from your phone.",9,199.00,None,4.6,True,None),
    ("PetSafe ScoopFree Automatic Litter Box","PetSafe","Self-cleaning crystal litter box — removes waste automatically.",9,599.00,None,4.7,True,None),
    ("Hill's Science Diet Large Breed Dry Dog Food 15kg","Hill's","Natural ingredients with vitamins and minerals for large breed dogs.",9,285.00,None,4.7,True,None),
    ("Purina Pro Plan Sensitive Salmon Dog Food 14kg","Nestle","Salmon-based formula for dogs with food sensitivities.",9,265.00,None,4.7,True,None),
    ("Dentastix Daily Oral Care Treats Large 28 Pack","Mars Petcare","Reduces tartar build-up by up to 80%. Vets recommend daily use.",9,55.00,None,4.7,True,None),
    ("KONG Extreme Dog Toy Large Black","Kong","Ultra-durable black KONG for power chewers — stuffable with treats.",9,75.00,None,4.8,True,None),
    ("Ruffwear Front Range Padded Dog Harness","Ruffwear","Padded chest and belly panel — distributes pressure for active dogs.",9,189.00,None,4.8,True,None),
    ("Furminator deShedding Tool Long Hair Medium","Furminator","Reduces shedding by up to 90% — popular with dog owners in Qatar.",9,95.00,None,4.7,True,None),
    ("Tetra AquaArt Aquarium Starter Set 60L","Tetra","Complete aquarium kit with filter, heater, and LED lighting.",9,299.00,None,4.6,True,None),
    ("API Freshwater Master Test Kit","API","800 tests — monitors ammonia, nitrite, nitrate, and pH in fish tanks.",9,65.00,None,4.7,True,None),
    ("Kaytee Forti-Diet Hamster & Gerbil Food 1kg","Kaytee","Complete nutrition with seeds, grains, and fortified pellets.",9,25.00,None,4.5,True,None),
    # ── Market (10) ───────────────────────────────────────────────────────────
    ("Pilot G2 Retractable Gel Pens Black 10 Pack","Pilot","Smooth-writing retractable gel pens — the office staple across Qatar.",10,18.00,None,4.7,True,None),
    ("Stabilo Boss Highlighters Assorted 8 Pack","Stabilo","Vivid fluorescent ink, chisel tip, won't bleed through most paper.",10,22.00,None,4.7,True,None),
    ("Sharpie Permanent Markers Assorted 12 Pack","Sharpie","Permanent marks on virtually any surface. Fast-drying, fade-resistant.",10,28.00,None,4.6,True,None),
    ("Moleskine Classic Ruled Notebook A5","Moleskine","192 pages, acid-free paper, bookmark ribbon. The writer's notebook.",10,45.00,None,4.7,True,None),
    ("Leuchtturm1917 Bullet Journal A5 Dotted","Leuchtturm1917","240 numbered pages, dotted grid, pocket, and ink-proof paper.",10,55.00,None,4.8,True,None),
    ("Arteza Watercolor Pencils 48 Pack","Arteza","Professional-grade pencils — vibrant, water-soluble, and blendable.",10,65.00,None,4.6,True,None),
    ("Faber-Castell 9000 Graphite Pencils 12 Pack","Faber-Castell","The world's most trusted pencil — B to H grades, break-resistant.",10,25.00,None,4.8,True,None),
    ("Bic Cristal Ballpoint Pens Black 10 Pack","Bic","The world's most sold pen — smooth ink flow, durable tungsten ball.",10,9.00,None,4.5,True,None),
    ("Philips LED Classic Bulb E27 8W 3 Pack","Philips","Equivalent to 60W, 806 lumen warm white LED bulbs.",10,18.00,None,4.6,True,None),
    ("Osram LED Star Bulb GU10 5W 3 Pack","Osram","Downlight replacement — 350 lumen, 2700K warm white, 15,000 hours.",10,16.00,None,4.5,True,None),
    ("Johnson & Johnson First Aid Kit 140 Pieces","J&J","Comprehensive first aid kit — bandages, gauze, antiseptic, and more.",10,55.00,None,4.6,True,None),
    ("Elastoplast Assorted Fabric Plasters 100 Pack","Beiersdorf","Flexible fabric plasters that move with your skin. Water-resistant.",10,18.00,None,4.5,True,None),
    ("Domestos Multipurpose Thick Bleach 750ml","Unilever","Kills 99.9% of germs including viruses. Works in 1 minute.",10,7.50,None,4.5,True,None),
    ("Fairy Original Dish Soap Lemon 1L","P&G","Powerful grease removal even in cold water — long-lasting formula.",10,8.50,None,4.6,True,None),
    ("Method All-Purpose Cleaner Pink Grapefruit 828ml","Method","Plant-powered formula, 99% naturally derived ingredients.",10,18.00,None,4.5,True,None),
    ("3M Command Large Damage-Free Hanging Strips 12 Pack","3M","Hang without nails — holds up to 3.6kg, removes cleanly.",10,22.00,None,4.6,True,None),
    ("Velcro Brand Sticky Back Tape 2m Roll","Velcro","Self-adhesive hook and loop tape — strong, reusable, repositionable.",10,12.00,None,4.4,True,None),
    ("Energizer Lithium AA Batteries 8 Pack","Energizer","33% lighter than alkaline, 9x power in extreme temperatures.",10,32.00,None,4.7,True,None),
    ("Duracell Procell AA Batteries 20 Pack","Duracell","Professional-grade alkaline batteries — reliable power for office devices.",10,45.00,None,4.6,True,None),
    ("Nobo Classic Steel Magnetic Whiteboard 60x90cm","Nobo","Steel surface for magnets, smooth writing and easy erasing.",10,155.00,None,4.6,True,None),
    # ── Electronics extras (4) ────────────────────────────────────────────────
    ("Apple iPhone 15 128GB Blue","Apple","A16 Bionic, 48MP main camera, Dynamic Island, USB-C, Emergency SOS via satellite.",4,3599.00,"iphone15pro",4.8,True,None),
    ("Samsung Galaxy A55 5G 128GB Awesome Navy","Samsung","50MP OIS camera, 6.6-inch Super AMOLED, IP67, 5000mAh — great mid-range value.",4,1199.00,None,4.6,True,None),
    ("Google Pixel 8 128GB Obsidian","Google","Google Tensor G3, 7 years of updates, AI-powered camera — clean Android experience.",4,2799.00,None,4.7,True,None),
    ("OnePlus 12 256GB Flowy Emerald","OnePlus","Snapdragon 8 Gen 3, 100W SUPERVOOC charging, Hasselblad-tuned cameras.",4,2799.00,None,4.7,True,None),
    ("Apple iPad 10th Gen 64GB WiFi Blue","Apple","A14 Bionic, 10.9-inch Liquid Retina, USB-C, 12MP Ultra Wide front camera.",4,1599.00,"ipad_air",4.7,True,None),
    ("Garmin Fenix 7 Solar Sapphire GPS Watch","Garmin","Multi-band GPS, solar charging, 37-day battery, AMOLED — ultra-endurance sports watch.",4,2399.00,None,4.8,True,None),
    ("Fitbit Charge 6 Health & Fitness Tracker","Google","ECG, SpO2, 7-day battery, Google Maps and Wallet on your wrist.",4,649.00,None,4.5,True,None),
    ("Beats Studio Pro Wireless Headphones Black","Apple","60-hour battery, custom acoustic platform, USB-C, ANC and Transparency mode.",4,1099.00,None,4.7,True,None),
    ("Jabra Evolve2 85 ANC Business Headset","GN Audio","Dual ANC, 37-hour battery, 10-mic voice isolation — Qatar's favourite office headset.",4,1299.00,None,4.7,True,1499.00),
    ("Shure MV7 USB/XLR Podcast Microphone","Shure","Dual-output USB + XLR, built-in headphone monitoring, cardioid dynamic capsule.",4,699.00,None,4.8,True,None),
    ("ASUS ZenScreen 15.6-inch Portable Monitor","ASUS","Full HD IPS, USB-C, 10-point multi-touch, foldable cover stand — for laptop users.",4,699.00,None,4.6,True,None),
    ("BenQ ScreenBar Plus Monitor Light E45","BenQ","Asymmetric optical design, auto-dimming sensor, wireless control dial.",4,499.00,None,4.7,True,None),
    ("Seagate Expansion 2TB Desktop External HDD","Seagate","USB 3.0, plug-and-play, works with PC and Mac. No power adapter needed.",4,189.00,None,4.5,True,None),
    ("SanDisk Extreme Pro 256GB MicroSD V30","SanDisk","200MB/s read, A2 app performance, shock/water/X-ray proof.",4,99.00,None,4.7,True,None),
    ("Sony DualSense Midnight Black PS5 Controller","Sony","Haptic feedback, adaptive triggers, built-in microphone. Midnight Black edition.",4,279.00,"ps5",4.8,True,None),
    ("Nintendo Switch Sports Game","Nintendo","Six sports — volleyball, football, tennis, bowling, badminton, chambara. For all ages.",4,199.00,"switch_oled",4.7,True,None),
    ("Razer Kraken V3 X USB Gaming Headset","Razer","THX Spatial Audio, TriForce 40mm drivers, HyperClear microphone.",4,249.00,"razer_mouse",4.6,True,None),
    ("SteelSeries Arctis Nova 7 Wireless Headset","SteelSeries","38-hour battery, 360° Spatial Audio, ClearCast AI mic, PC and PlayStation.",4,699.00,None,4.7,True,None),
    ("Corsair K70 RGB Pro TKL Mechanical Keyboard","Corsair","Cherry MX Speed switches, PBT double-shot keycaps, per-key RGB, compact TKL.",4,449.00,None,4.7,True,None),
    ("Elgato 4K60 Pro MK.2 Capture Card","Elgato","4K60 HDR capture, VRR support, zero-lag passthrough — for console content creators.",4,699.00,None,4.7,True,None),
    ("Govee Lyra RGBICWW Floor Lamp","Govee","Alexa & Google, 16M colours, music sync, Matter support — smart home ambient.",4,349.00,None,4.5,True,None),
    ("Apple HomePod 2nd Gen Midnight","Apple","Spatial Audio, room sensing, Home Hub, S7 chip — the best smart speaker for iPhone.",4,999.00,None,4.7,True,None),
    ("Anker 555 USB Hub 8-in-1","Anker","4K HDMI, 100W pass-through, SD, 3x USB-A, USB-C — the desk hub for MacBook.",4,149.00,None,4.7,True,None),
    ("Belkin MagSafe 3-in-1 Wireless Charger","Belkin","Simultaneously charges iPhone, Apple Watch, and AirPods — MagSafe 15W.",4,329.00,None,4.6,True,None),
    ("OtterBox Commuter Series iPhone 15 Pro Case","OtterBox","Two-layer drop protection, port covers, slim profile, MagSafe compatible.",4,89.00,None,4.7,True,None),
    # ── Pharmacy extras (11) ─────────────────────────────────────────────────
    ("Panadol Night Pain Reliever 500mg 24 Tablets","GlaxoSmithKline","Paracetamol + diphenhydramine — eases pain and aids restful sleep.",11,18.00,None,4.6,True,None),
    ("Nexium 20mg Esomeprazole 14 Capsules","AstraZeneca","Proton pump inhibitor for GERD — reduces stomach acid production effectively.",11,32.00,None,4.6,True,None),
    ("Aspirin 75mg Cardio Enteric-Coated 100 Tablets","Bayer","Low-dose aspirin for cardiovascular protection — daily cardio use.",11,18.00,None,4.5,True,None),
    ("Loperamide 2mg Anti-Diarrhoeal 12 Capsules","Generic","Fast-acting diarrhoea relief — reduces frequency of loose stools.",11,14.00,None,4.5,True,None),
    ("Maalox Antacid Suspension 200ml","Sanofi","Liquid antacid for quick heartburn and indigestion relief.",11,16.00,None,4.5,True,None),
    ("Voltaren Emulgel 1.16% Diclofenac 100g","Haleon","Targeted topical NSAID gel — penetrates deep for joint and muscle relief.",11,28.00,None,4.7,True,None),
    ("Flixonase Aqueous Nasal Spray 150 Doses","Haleon","Fluticasone propionate — reduces nasal congestion in hay fever and rhinitis.",11,45.00,None,4.6,True,None),
    ("Otrivin 0.1% Xylometazoline Nasal Spray 10ml","Haleon","Fast-acting nasal decongestant — clears blocked nose in minutes.",11,16.00,None,4.6,True,None),
    ("Refresh Tears Lubricant Eye Drops 15ml","Allergan","Artificial tears for dry eye relief — preservative-free formula.",11,22.00,None,4.7,True,None),
    ("Imodium Plus Comfort 12 Tablets","Johnson & Johnson","Loperamide + simethicone — stops diarrhoea and relieves bloating.",11,24.00,None,4.5,True,None),
    ("Vitamin D3 1000 IU 30 Tablets","Solgar","Bone and immune health support — essential for Qatar's indoor lifestyle.",11,22.00,None,4.7,True,None),
    ("Zinc 15mg Immune Support 60 Tablets","Solgar","Promotes immune function, skin health, and wound healing.",11,28.00,None,4.6,True,None),
    ("Magnesium 250mg Glycinate 60 Tablets","NOW Foods","Supports muscle relaxation, sleep quality, and nerve function.",11,35.00,None,4.7,True,None),
    # ── Arabic Sweets extras (12) ─────────────────────────────────────────────
    ("Warbat Cream Pastry 6 Pieces","Al Khaima","Flaky filo triangles filled with thick ashta and drizzled with syrup.",12,22.00,None,4.7,True,None),
    ("Asabi Zainab Lady Fingers Pastry 250g","Al Reef","Cylindrical filo fingers stuffed with cream and pistachio.",12,28.00,None,4.7,True,None),
    ("Namoura Semolina Syrup Cake 500g","Hallab","Moist diamond-cut semolina cake soaked in sugar syrup.",12,20.00,None,4.6,True,None),
    ("Caramel Custard Flan 4 Cups","Local Kitchen","Smooth vanilla custard with caramel sauce — chilled ready to eat.",12,18.00,None,4.7,True,None),
    ("Knafeh Bil Jibn Doha Street Style 1kg","Al Khaima","Original Doha-style kunafa — string pastry with cheese, orange blossom water.",12,48.00,None,4.9,True,None),
    ("Assorted Arabic Candy Mix 1kg","Gandour","Mixed Arabic hard candies, soft sweets, and sesame brittle.",12,22.00,None,4.4,True,None),
    ("Sesame Brittle Simsimiya 300g","Local Kitchen","Roasted sesame seeds in golden caramel. A Qatari coastal sweet tradition.",12,16.00,None,4.7,True,None),
    ("Pistachio Nougat with Rose Water 300g","Al Reef","Light nougat with whole pistachios and a delicate rose-water aroma.",12,32.00,None,4.6,True,None),
    ("Chocolate-Coated Dates Assorted 250g","Bateel","Finest Khalas dates coated in dark, milk, and white Belgian chocolate.",12,65.00,None,4.9,True,None),
    ("Cardamom-Spiced Arabic Coffee 250g","Najjar","Finely ground Arabic coffee with cardamom — the classic Gulf reception drink.",12,18.00,None,4.8,True,None),
    ("Fraisier Fresh Strawberry Cake 6-Inch","La Boulangerie","French-style strawberry cream cake — made fresh, ideal for Doha celebrations.",12,95.00,None,4.8,True,None),
    ("Chocolate Fondant Lava Cake 4 Pieces","La Boulangerie","Warm Belgian chocolate cakes with liquid chocolate centre.",12,48.00,None,4.8,True,None),
    # ── Baby & Infant extras (13) ─────────────────────────────────────────────
    ("Molfix Comfort Diapers Size 4 68 Pieces","Hayat","Soft stretch sides and a wetness indicator. Popular budget-friendly choice in Qatar.",13,45.00,None,4.5,True,None),
    ("Libero Comfort Diapers Size 5 42 Pieces","SCA","Swedish diaper brand — gentle non-woven inner, stretchy waistband.",13,55.00,None,4.5,True,None),
    ("WaterWipes Original Baby Wipes 60 Sheets x3","WaterWipes","99.9% water, 0.1% grapefruit seed extract — the purest wipes available.",13,45.00,None,4.8,True,None),
    ("Pigeon SofTouch Baby Bottle 160ml","Pigeon","Ultra-soft teat closely mimics natural breastfeeding latch.",13,35.00,None,4.6,True,None),
    ("Bebeconfort Emotion+ Anti-Colic Baby Bottle 150ml","Bebeconfort","Four-vent system virtually eliminates air intake and colic.",13,38.00,None,4.6,True,None),
    ("MAM Easy Start Anti-Colic Bottle 160ml","MAM","Patented base venting system reduces colic — self-sterilising in microwave.",13,45.00,None,4.7,True,None),
    ("Weleda Calendula Baby Cream 75ml","Weleda","Certified organic calendula cream — soothes, protects, and moisturises baby skin.",13,28.00,None,4.7,True,None),
    ("La Roche-Posay Lipikar Baby AP+ Body Cream 400ml","L'Oreal","Dermatologist-tested barrier cream for eczema-prone infant skin.",13,85.00,None,4.8,True,None),
    ("Chicco Meal Set Weaning Bowl + Spoon 4m+","Artsana","Suction bowl and soft-tip spoon set — BPA-free, dishwasher safe.",13,35.00,None,4.5,True,None),
    ("Infantino Twist and Fold Activity Gym","Infantino","Tummy time mat with arch toys, mirror, and sensory textures for newborns.",13,95.00,None,4.6,True,None),
    ("Graco Snuggle Me Infant Lounger","Graco","Organic cotton lounger with padded sides — for supervised awake-time lounging.",13,149.00,None,4.6,True,None),
    ("BABYBJÖRN Baby Carrier Mini Cotton","BABYBJÖRN","Newborn carrier from 3.5kg — adjustable, machine-washable organic cotton.",13,295.00,None,4.8,True,None),
    # ── Coffee & Café extras (14) ─────────────────────────────────────────────
    ("Ethiopian Yirgacheffe Light Roast Whole Beans 250g","Origin Coffee","Single-origin Ethiopian — floral, citrus notes with a tea-like body.",14,45.00,None,4.8,True,None),
    ("Colombian Supremo Medium Roast Whole Beans 250g","Origin Coffee","Bright acidity, caramel sweetness, and a smooth walnut finish.",14,42.00,None,4.7,True,None),
    ("Brazil Santos Natural Whole Beans 250g","Origin Coffee","Full body, low acidity — chocolate and almond notes. Great for espresso.",14,38.00,None,4.7,True,None),
    ("Nespresso Vertuo Altissio Espresso Capsules 10 Pack","Nestlé","Bold, creamy espresso with a rich, lingering intensity. Vertuo system.",14,42.00,"nespresso",4.7,True,None),
    ("Illy Classico Easy Serving Pods 18 Pods","illy","Unique Paper pods compatible with ESE-standard machines.",14,38.00,"illy",4.7,True,None),
    ("Bodum Chambord 8-Cup French Press Coffee Maker","Bodum","Stainless steel plunger, heat-resistant borosilicate glass. Classic design.",14,95.00,None,4.8,True,None),
    ("OXO Brew 9-Cup Pour-Over Coffee Maker","OXO","Built-in shower head ensures even saturation — consistent extraction every time.",14,249.00,None,4.7,True,None),
    ("Fellow Atmos Vacuum Canister 0.4L","Fellow","Stainless steel vacuum canister — extends coffee freshness up to 2 weeks.",14,85.00,None,4.7,True,None),
    ("Timemore Chestnut X Manual Coffee Grinder","Timemore","Stainless steel burrs, 36-step grind adjustment. Barista-quality home grinder.",14,275.00,None,4.8,True,None),
    ("Brewista Smart Scale II Coffee Scale","Brewista","0.1g precision, built-in timer, auto-tare — for precision pour-over.",14,149.00,None,4.7,True,None),
    ("Monin Vanilla Syrup 700ml","Monin","Premium French flavouring syrup — café-grade vanilla for lattes and cold brew.",14,28.00,None,4.6,True,None),
    ("Monin Caramel Syrup 700ml","Monin","Rich caramel syrup — the barista's go-to for caramel macchiatos.",14,28.00,None,4.6,True,None),
    ("Oatly Barista Edition Oat Milk 1L","Oatly","Specially formulated to froth and steam like dairy — for plant-based lattes.",14,18.00,None,4.7,True,None),
]


HEADER = """\
--
-- PostgreSQL database dump
--

\\restrict {key}

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
INSERT INTO public.categories VALUES (11, 'Pharmacy', 'pharmacy');
INSERT INTO public.categories VALUES (12, 'Arabic Sweets & Bakery', 'arabic-sweets-bakery');
INSERT INTO public.categories VALUES (13, 'Baby & Infant', 'baby-infant');
INSERT INTO public.categories VALUES (14, 'Coffee & Café', 'coffee-cafe');


--
-- Data for Name: cities; Type: TABLE DATA; Schema: public; Owner: snoonu
--

INSERT INTO public.cities VALUES (1, 'Doha', 25.285400, 51.531000, '{{doha}}');
INSERT INTO public.cities VALUES (2, 'Al Rayyan', 25.291900, 51.424400, '{{rayyan}}');
INSERT INTO public.cities VALUES (3, 'Al Wakrah', 25.165900, 51.603800, '{{wakrah}}');
INSERT INTO public.cities VALUES (4, 'Umm Salal', 25.415100, 51.397300, '{{"umm salal"}}');
INSERT INTO public.cities VALUES (5, 'Al Khor', 25.680400, 51.498900, '{{"al khor",khor}}');
INSERT INTO public.cities VALUES (6, 'Al Daayen', 25.519700, 51.492600, '{{daayen}}');
INSERT INTO public.cities VALUES (7, 'Al Shamal', 26.116700, 51.216700, '{{"madinat shamal",shamal}}');
INSERT INTO public.cities VALUES (8, 'Al Shahaniya', 25.370500, 51.196900, '{{shahaniya}}');


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: snoonu
-- Real Qatar/GCC products — curated Qatari brands (Baladna, Mazzraty, Rayyan, Doha Dates, etc.)
-- plus international brands widely available in Qatar.
--
""".format(key=RESTRICT_KEY)

FOOTER = """

--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: snoonu
--

SELECT pg_catalog.setval('public.categories_id_seq', 14, true);


--
-- Name: cities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: snoonu
--

SELECT pg_catalog.setval('public.cities_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

\\unrestrict {key}""".format(key=RESTRICT_KEY)


def esc(s):
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"


def resolve_img(key_or_url):
    if not key_or_url:
        return "NULL"
    if key_or_url.startswith("http"):
        return esc(key_or_url)
    return esc(IMG[key_or_url]) if key_or_url in IMG else "NULL"


def curated_sql(row):
    pid, name, brand, desc, cat_id, price, img, rating, in_stock, compare_at = row
    stock = "high" if in_stock else "low"
    bool_s = "true" if in_stock else "false"
    img_s = resolve_img(img)
    cmp_s = f"{compare_at:.2f}" if compare_at else "NULL"
    return (
        f"INSERT INTO public.products VALUES ({esc(pid)},{esc(name)},{esc(brand)},"
        f"{esc(desc)},{cat_id},{price:.2f},'QAR',{cmp_s},{bool_s},{esc(stock)},"
        f"{img_s},NULL,{rating},NULL,'{CREATED_AT}');"
    )


def extra_sql(idx, row):
    name, brand, desc, cat_id, price, img, rating, in_stock, compare_at = row
    pid = f"snu-x{idx:04d}"
    stock = "high" if in_stock else "low"
    bool_s = "true" if in_stock else "false"
    img_s = resolve_img(img)
    cmp_s = f"{compare_at:.2f}" if compare_at else "NULL"
    return (
        f"INSERT INTO public.products VALUES ({esc(pid)},{esc(name)},{esc(brand)},"
        f"{esc(desc)},{cat_id},{price:.2f},'QAR',{cmp_s},{bool_s},{esc(stock)},"
        f"{img_s},NULL,{rating},NULL,'{CREATED_AT}');"
    )


def main():
    out_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "deploy", "gcloud", "db", "02-seed-data.sql"
    )

    lines = [HEADER]

    seen_names = set()
    count = 0

    for row in CURATED:
        name_key = row[1].lower().strip()
        if name_key in seen_names:
            continue
        seen_names.add(name_key)
        lines.append(curated_sql(row))
        count += 1

    idx = 1
    for row in EXTRA:
        name_key = row[0].lower().strip()
        if name_key in seen_names:
            continue
        seen_names.add(name_key)
        lines.append(extra_sql(idx, row))
        idx += 1
        count += 1

    lines.append(FOOTER)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Done: {count} products → {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
