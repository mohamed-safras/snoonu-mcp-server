--
-- PostgreSQL database dump
--

\restrict cznfCrh011aXx2WgnIIH7HXTdkggUATtzGQRUYrgN4XKaYgXVbIM2o4ZTTOZM9o

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

INSERT INTO public.products VALUES ('snu-c001','Baladna Full Fat Fresh Milk 1L','Baladna','Farm-fresh full-fat milk — Qatar''s most-consumed fresh milk brand. Processed the same day on their farm north of Doha.',2,7.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/629/100/300/9842/front_en.3.400.jpg',NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c002','Baladna Fresh Milk 2L','Baladna','Family-size carton of full-fat fresh milk. No preservatives, locally produced.',2,12.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c003','Baladna Low Fat Fresh Milk 1L','Baladna','Fresh low-fat milk for health-conscious shoppers. Same farm-fresh quality.',2,7.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c004','Baladna Greek Style Yoghurt 4x150g','Baladna','Thick, creamy Greek-style yoghurt made from fresh Qatar milk. High protein, rich in probiotics.',2,9.75,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c005','Baladna Full Fat Yoghurt 1kg','Baladna','Smooth full-fat fresh yoghurt. Perfect with dates and honey, or as a cooking base for Gulf recipes.',2,8.50,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c006','Baladna Laban Drinking Yoghurt 1L','Baladna','Chilled laban — the classic Gulf drinking yoghurt. Light, tangy, and refreshing.',2,6.50,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c007','Baladna Laban Drinking Yoghurt 2L','Baladna','Large-format laban for family gatherings. Same refreshing taste, better value.',2,10.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c008','Baladna Custard Vanilla & Chocolate 4x110g','Baladna','Ready-to-eat custard cups in vanilla and chocolate. Made with fresh Qatar milk.',2,6.25,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c009','Mazzraty Probiotic Laban Full Fat 1L','Mazzraty','Probiotic laban from Qatar''s 100% national NGAAP-certified brand. Full-fat, creamy, great for digestion.',2,6.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c010','Mazzraty Probiotic Laban Full Fat 500ml','Mazzraty','Individual-serve laban with live probiotic cultures.',2,3.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c011','Mazzraty Fresh Full Cream Milk 1L','Mazzraty','100% Qatari full-cream fresh milk from NGAAP farms.',2,8.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c012','Almarai Fresh Milk 1L','Almarai','Fresh pasteurised full-fat milk from Almarai, the GCC''s leading dairy brand.',2,7.25,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/628/176/400/0038/front_en.12.400.jpg',NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c013','Almarai Cream Cheese 200g','Almarai','Smooth spreadable cream cheese. No artificial preservatives.',2,12.00,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c014','Lurpak Butter Slightly Salted 200g','Lurpak','The world''s most popular butter — slightly salted, made from fresh cream.',2,16.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/570/160/003/1154/front_en.34.400.jpg',NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c015','Philadelphia Original Cream Cheese 200g','Mondelez','The iconic cream cheese — rich, versatile. Perfect for cheesecakes and bagels.',2,14.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/768/901/237/0005/front_en.44.400.jpg',NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c016','Kiri Cream Cheese Portions 8x17.5g','Bel Group','Individually portioned cream cheese — ideal for lunchboxes and kids.',2,12.00,'QAR',NULL,true,'high',NULL,NULL,4.3,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c017','Rayyan Natural Mineral Water 1.5L','Rayyan','Natural mineral water from Qatar''s own aquifer 60 km north of Doha.',2,2.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c018','Rayyan Natural Mineral Water 6x1.5L','Rayyan','Six-pack of Rayyan — better value for daily hydration.',2,9.50,'QAR',11.50,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c019','Qatar Oasis Balanced Drinking Water 1.5L','Qatar Oasis','Locally produced pH-balanced drinking water.',2,1.50,'QAR',NULL,true,'high',NULL,NULL,4.2,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c020','Qatar Oasis Drinking Water 6x1.5L','Qatar Oasis','Bulk pack of Qatar Oasis water — great for households.',2,7.50,'QAR',9.00,true,'high',NULL,NULL,4.2,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c021','Aquafina Purified Drinking Water 1.5L','PepsiCo','Seven-step HydRO-7 purified drinking water. Available across all Qatar outlets.',2,2.50,'QAR',NULL,true,'high',NULL,NULL,4.3,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c022','Evian Natural Spring Water 1.5L','Danone','Alpine natural spring water, naturally filtered over 15 years through glacial rocks.',2,5.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/305/764/025/7773/front_en.343.400.jpg',NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c023','Coca-Cola Original Taste 330ml Can','Coca-Cola','The world''s favourite soft drink. Served chilled — great with meals.',2,2.50,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/544/900/021/4911/front_fr.335.400.jpg',NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c024','Coca-Cola Zero Sugar 330ml Can','Coca-Cola','Full Coca-Cola taste, zero sugar and zero calories.',2,2.50,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c025','Pepsi Cola 330ml Can','PepsiCo','Refreshing carbonated cola — Pepsi''s bold, crisp taste.',2,2.50,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c026','7UP Lemon-Lime 330ml Can','PepsiCo','Crisp lemon-lime carbonated drink. Caffeine-free, refreshingly light.',2,2.25,'QAR',NULL,true,'high',NULL,NULL,4.3,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c027','Rani Float Mango Juice with Fruit Pieces 240ml','Al Aujan','Iconic Gulf mango juice drink with real fruit pieces. A regional classic enjoyed across Qatar.',2,2.50,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/628/176/420/6028/front_en.5.400.jpg',NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c028','Rani Float Orange Juice with Fruit Pieces 240ml','Al Aujan','Orange juice drink with real fruit pieces. Refreshing tropical taste.',2,2.50,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c029','Almarai Apple & Grape Juice 1L','Almarai','100% blended apple and grape juice. No added sugar, no preservatives.',2,9.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c030','Baladna Fresh Orange Juice 1L','Baladna','Freshly squeezed-style orange juice. No artificial colours or flavours.',2,8.50,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c031','Nescafe Classic Instant Coffee 200g','Nestle','Rich roasted aroma with a smooth, full-bodied flavour. Dissolves instantly.',2,17.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/611/101/890/3161/front_fr.48.400.jpg',NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c032','Nescafe Gold Blend Instant Coffee 95g','Nestle','Premium blend of finely roasted Arabica and Robusta beans. Distinctly smooth taste.',2,26.50,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c033','Nescafe Arabiana Arabic Coffee with Cardamom 20 Sachets','Nestle','Authentic Arabic coffee with real cardamom in single-serve sachets. A beloved Qatari morning ritual.',2,13.50,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c034','Nescafe 3-in-1 Original Coffee Mix 20 Sachets','Nestle','Coffee, creamer, and sugar in one sachet — just add hot water.',2,19.50,'QAR',NULL,true,'high',NULL,NULL,4.3,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c035','Cafe Najjar Classic Ground Coffee with Cardamom 200g','Cafe Najjar','Traditional Arabic ground coffee with cardamom from Lebanon''s iconic brand.',2,16.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c036','Al Rifai Turkish Ground Coffee with Cardamom 250g','Al Rifai','Finely ground Turkish-style coffee enriched with cardamom. Bold and aromatic.',2,23.75,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c037','Lipton Yellow Label Black Tea 100 Bags','Unilever','Bright, brisk black tea — perfect with milk, lemon, or plain.',2,18.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/800/235/005/4231/front_en.21.400.jpg',NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c038','Ahmad Tea English Breakfast 100 Bags','Ahmad Tea','Premium English Breakfast blend — rich, malty, full-bodied. Popular in Qatar cafes.',2,22.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c039','Lipton Green Tea 100 Bags','Unilever','Light refreshing green tea with natural antioxidants. Great hot or chilled.',2,18.00,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c040','L''usine White Toast Bread 500g','Almarai','Soft white sliced toast bread from L''usine by Almarai. Fresh-baked, evenly sliced.',2,5.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c041','L''usine Whole Wheat Toast Bread 500g','Almarai','Whole wheat toast bread — higher in fibre, hearty flavour.',2,6.00,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c042','QBake White Sandwich Bread 500g','QBake','Locally baked white sandwich bread from Qatar''s own QBake brand.',2,4.75,'QAR',NULL,true,'high',NULL,NULL,4.3,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c043','Arabic Pita Bread 10 Pieces','Local Bakery','Freshly baked thin Arabic pita bread. Essential for shawarma, hummus, and Gulf breakfasts.',2,3.50,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c044','Nutella Hazelnut & Cocoa Spread 400g','Ferrero','The world''s favourite hazelnut spread with cocoa. Rich and creamy on toast or waffles.',2,18.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/000/008/017/6800/front_en.273.400.jpg',NULL,4.9,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c045','Doha Dates Medjool Premium 500g','Doha Dates','Plump, soft Medjool dates from Doha Dates by NAFCO — Qatar''s largest date processor.',2,16.75,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c046','Doha Dates Khalas 500g','Doha Dates','Khalas dates — considered the finest Gulf dates. Deep toffee-honey flavour. Grown in Qatar.',2,12.00,'QAR',NULL,true,'high',NULL,NULL,4.9,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c047','Doha Dates Sukkari 500g','Doha Dates','Sukkari dates — ultra-sweet, melt-in-the-mouth. A Ramadan and Eid favourite.',2,11.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c048','Bateel Kholas Premium Dates Gift Box 300g','Bateel','Luxury Kholas dates in a signature Bateel gift box. Hand-selected and elegantly presented.',2,55.00,'QAR',NULL,true,'high',NULL,NULL,4.9,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c049','Bateel Organic Assorted Dates Gift Box 500g','Bateel','Curated Bateel organic dates — Kholas, Wanan, and Segae — in a luxurious gift box.',2,89.00,'QAR',NULL,true,'high',NULL,NULL,5.0,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c050','Local Medjool Dates 1kg','Local Farm','Fresh Medjool dates from Qatari farms. Large, moist, naturally sweet.',2,30.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c051','Pringles Original Chips 165g','Kellogg''s','The iconic stackable crisp with Pringles'' signature original flavour.',2,11.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/038/000/845/5963/front_en.15.400.jpg',NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c052','Pringles Sour Cream & Onion 165g','Kellogg''s','Fan-favourite flavour — tangy, savoury, impossible to put down.',2,11.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c053','Pringles Hot & Spicy 165g','Kellogg''s','Bold, fiery kick in Pringles'' signature stackable crisp format.',2,11.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c054','Doritos Nacho Cheese 48g','PepsiCo','Boldly flavoured nacho cheese tortilla chips. A party staple across Qatar.',2,4.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c055','Doritos Cool Ranch 48g','PepsiCo','Cool, tangy ranch flavour on Doritos'' crunchy triangular chips.',2,4.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c056','Lay''s Classic Potato Chips 145g','PepsiCo','Light, crispy potato chips with a simple salted flavour. A Qatar household staple.',2,7.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c057','Lay''s BBQ Flavour 145g','PepsiCo','Smoky BBQ seasoned potato chips — rich, tangy, and perfectly balanced.',2,7.50,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c058','KitKat 4-Finger Milk Chocolate 45g','Nestle','Crispy wafer covered in smooth milk chocolate. Qatar''s best-selling chocolate bar.',2,4.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/400/009/007/5050/front_en.131.400.jpg',NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c059','Cadbury Dairy Milk 90g','Mondelez','Creamy, smooth British milk chocolate. A household name in Qatar.',2,7.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c060','Twix Caramel Chocolate Bar 58g','Mars','Crunchy biscuit, smooth caramel, and milk chocolate — the classic twin bar.',2,4.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c061','Snickers Chocolate Bar 52g','Mars','Peanuts, caramel, nougat, and milk chocolate. One of Qatar''s top confectionery bars.',2,4.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c062','M&M''s Peanut Chocolate 250g','Mars','Whole peanuts coated in milk chocolate and a colourful candy shell. Great for sharing.',2,16.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c063','Tilda Pure Basmati Rice 2kg','Tilda','The world''s finest basmati rice — long, slender, naturally aromatic grains.',2,24.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/500/030/126/8620/front_en.38.400.jpg',NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c064','Golden Sella Basmati Rice 5kg','Golden','Parboiled basmati rice ideal for biryani, kabsa, and machboos.',2,32.00,'QAR',38.00,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c065','Mazzraty Fresh Eggs Large 12 Pieces','Mazzraty','Fresh large eggs from Mazzraty''s 100% Qatari poultry farms.',2,11.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c066','Americana Chicken Breast Fillets 1kg','Americana','Boneless, skinless chicken fillets — Halal-certified, IQF frozen.',2,28.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c067','Hellmann''s Real Mayonnaise 400g','Unilever','Rich, creamy real mayonnaise. The go-to condiment for sandwiches and dips.',2,14.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c068','Heinz Tomato Ketchup 570g','Kraft Heinz','Thick, tangy, naturally sweet ketchup. Essential in every Qatari household.',2,12.00,'QAR',NULL,true,'high','https://images.openfoodfacts.org/images/products/000/001/700/7033/front_en.280.400.jpg',NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c069','Red Rose Bouquet 12 Stems','Snooflower','Twelve fresh-cut red roses wrapped in premium floral paper. Delivered same day across Doha.',1,85.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c070','Mixed Seasonal Flowers Arrangement','Snooflower','Vibrant hand-arranged bouquet of seasonal blooms — roses, lilies, and fillers.',1,120.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c071','White Orchid Potted Plant','Snooflower','Elegant white Phalaenopsis orchid in a ceramic pot. Long-lasting, sophisticated gift.',1,150.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c072','Premium Dates & Sweets Gift Hamper 1kg','Snooflower','Curated hamper with Khalas dates, assorted chocolates, and Arabic sweets in a decorative box.',1,95.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c073','Roses & Chocolate Gift Hamper','Snooflower','Six red roses paired with a premium chocolate box in an elegant gift bag.',1,180.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c074','Birthday Balloon Bouquet with Ribbon','Snooflower','Five large helium-filled latex balloons in assorted colours, ready to deliver.',1,45.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c075','Sunflower Bouquet 10 Stems','Snooflower','Bright, cheerful sunflower bouquet — a popular get-well and congratulations gift.',1,75.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c076','Luxury Rose & Lily Bouquet 20 Stems','Snooflower','Statement bouquet of roses and lilies in a luxury water-resistant wrap.',1,220.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c077','Panadol Extra Strength 500mg 24 Tablets','GlaxoSmithKline','Fast-acting paracetamol for headaches, fever, and body aches. Qatar''s most-trusted OTC pain reliever.',3,12.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c078','Vicks VapoRub Aromatic Ointment 50g','Procter & Gamble','Menthol, camphor, and eucalyptus oil — relieves coughs and nasal congestion.',3,15.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c079','Centrum Men Multivitamin 30 Tablets','Pfizer','Complete daily multivitamin formulated for men — Vitamin D, B12, Zinc, and more.',3,45.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c080','Vitamin C 1000mg Effervescent 30 Tablets','Redoxon','Effervescent Vitamin C — dissolves in water. Orange-flavoured, sugar-free.',3,25.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c081','Dove Deep Moisture Body Wash 500ml','Unilever','NutriumMoisture formula — leaves skin soft and hydrated after every shower.',3,18.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c082','Head & Shoulders Classic Clean Shampoo 400ml','Procter & Gamble','Clinically proven anti-dandruff shampoo. Gentle enough for everyday use.',3,22.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c083','Nivea Men Deep Face Wash 100ml','Beiersdorf','Deep-cleansing face wash with activated charcoal. Removes oil and impurities.',3,16.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c084','Colgate Total Whitening Toothpaste 150g','Colgate-Palmolive','Antibacterial protection for teeth, tongue, cheeks, and gums. Whitens in one step.',3,12.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c085','Garnier Micellar Cleansing Water 400ml','L''Oreal','All-in-one micellar water — cleanses, removes makeup, and refreshes. No rinse needed.',3,28.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c086','Neutrogena Hydro Boost Water Gel 50ml','Johnson & Johnson','Lightweight oil-free moisturiser with hyaluronic acid. Locks in hydration up to 72 hours.',3,55.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c087','Dettol Antibacterial Bar Soap 120g x3','Reckitt','Kills 99.9% of bacteria. Long-lasting protection — a must-have for every Qatari household.',3,9.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c088','Pantene Pro-V Smooth & Silky Shampoo 400ml','Procter & Gamble','Pro-V formula strengthens and smooths hair. Popular across Qatar salons and homes.',3,22.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c089','Apple AirPods Pro 2nd Generation','Apple','ANC, Adaptive Transparency, and Spatial Audio. MagSafe charging case included.',4,999.00,'QAR',NULL,true,'high',NULL,NULL,4.9,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c090','Samsung Galaxy Buds2 Pro True Wireless','Samsung','24-bit Hi-Fi audio, Intelligent ANC. Up to 29 hours battery with case.',4,649.00,'QAR',799.00,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c091','JBL Flip 6 Portable Bluetooth Speaker','JBL','IP67 waterproof, 12-hour playtime, bold bass. Great for the beach and pool.',4,299.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c092','Anker PowerCore 20000mAh Power Bank','Anker','USB-C and USB-A ports. Charges an iPhone 15 nearly five times. Carry-on safe.',4,149.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c093','Sony WH-1000XM5 Wireless Headphones','Sony','Industry-leading noise cancellation, 30-hour battery, crystal-clear call quality.',4,1299.00,'QAR',1499.00,true,'high',NULL,NULL,4.9,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c094','Apple USB-C to Lightning Cable 1m','Apple','MFi-certified cable for fast charging iPhones and iPads.',4,79.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c095','Samsung 65 Crystal UHD 4K Smart TV','Samsung','4K UHD, Samsung Crystal Processor, HDR, Tizen OS. Near-borderless display.',4,3499.00,'QAR',3999.00,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c096','Xiaomi Smart Band 8 Fitness Tracker','Xiaomi','1.62-inch AMOLED, heart rate, SpO2, sleep analysis. 16-day battery life.',4,149.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c097','JBL Charge 5 Portable Speaker','JBL','IP67 waterproof, 20-hour playtime, PowerBank function. Rich sound, deep bass.',4,449.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c098','Ray-Ban Aviator Classic Polarized Sunglasses','Ray-Ban','Timeless Aviator with polarized lenses and gold metal frame. UV400 protection, unisex.',5,699.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c099','Nike Air Max 270 Men''s Lifestyle Shoes','Nike','Nike''s largest heel Air unit — all-day cushioning and sleek sporty profile.',5,449.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c100','Adidas Originals Stan Smith Sneakers','Adidas','The iconic minimalist leather tennis shoe turned streetwear classic.',5,329.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c101','Tommy Hilfiger Men''s Slim Polo Shirt','Tommy Hilfiger','Classic slim-fit pique polo. 100% cotton — perfect for Qatar''s smart-casual dress code.',5,249.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c102','Calvin Klein Reversible Leather Belt','Calvin Klein','Reversible black/brown leather belt with CK logo buckle.',5,179.00,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c103','Fossil Machine Stainless Steel Watch','Fossil','Three-hand dial, water-resistant to 10ATM. Popular gifting choice in Qatar.',5,899.00,'QAR',1099.00,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c104','Tefal Expertise Non-Stick Frying Pan 28cm','Tefal','Superior non-stick, Thermo-Signal heat indicator. PFOA-free, dishwasher-safe.',6,89.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c105','Ariel Automatic Washing Powder 4kg','Procter & Gamble','Powerful stain-removing laundry powder for automatic washing machines.',6,38.00,'QAR',45.00,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c106','Dettol Multi-Surface Antibacterial Spray 500ml','Reckitt','Kills 99.9% of bacteria on kitchen and bathroom surfaces. No rinsing required.',6,9.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c107','Glad ForceFlex Stretch Trash Bags 30L 20 Pieces','Glad','Stretchable bags that resist tears and punctures around sharp or heavy items.',6,8.50,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c108','Philips Air Purifier Series 800 AC0820','Philips','HEPA filter captures 99.97% of particles. Ideal for Doha''s dusty conditions.',6,449.00,'QAR',549.00,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c109','Oral-B Pro 1500 Electric Rechargeable Toothbrush','Oral-B','Removes up to 100% more plaque than manual. Pressure sensor, 2-min timer.',6,189.00,'QAR',229.00,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c110','Finish Dishwasher Tablets Quantum 40 Tablets','Reckitt','All-in-one dishwasher tablets — removes tough stains, protects glass.',6,32.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c111','Scotch-Brite Heavy Duty Scrub Sponge 3 Pack','3M','Long-lasting scrubbing sponge — tough on grease, safe on most surfaces.',6,7.50,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c112','LEGO Classic Creative Bricks 10696','LEGO','484 pieces in 33 colours. Open-ended building creativity for ages 4+.',7,149.00,'QAR',NULL,true,'high',NULL,NULL,4.9,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c113','Hot Wheels 20-Car Gift Pack','Mattel','20 die-cast Hot Wheels vehicles in assorted styles. A perennial Qatar favourite.',7,99.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c114','Barbie Fashionista Doll Assorted','Mattel','Barbie in a trendy outfit with accessories. Diverse doll styles, ages 3+.',7,79.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c115','Pampers Baby-Dry Diapers Size 4 52 Pieces','Procter & Gamble','Up to 12 hours overnight dryness. Three absorbing layers. Qatar''s #1 diaper brand.',7,65.00,'QAR',75.00,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c116','Huggies Ultra Comfort Diapers Size 4 52 Pieces','Kimberly-Clark','Soft inner layer keeps skin dry. Flexible waistband adapts to baby''s movement.',7,60.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c117','Similac Gold Stage 1 Baby Formula 900g','Abbott','Infant formula with 2''FL HMO prebiotics. Supports immune development, 0-6 months.',7,185.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c118','Play-Doh 10-Color Pack','Hasbro','10 non-toxic, easy-to-play-with colours for creative fun. Ages 2+.',7,55.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c119','Nike Dri-FIT Men''s Training T-Shirt','Nike','Sweat-wicking Dri-FIT fabric. Lightweight and breathable for Qatar''s intense heat.',8,149.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c120','Fitness Exercise Non-Slip Yoga Mat 6mm','Generic','Thick 6mm non-slip mat — cushions joints during yoga, pilates, and floor workouts.',8,79.00,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c121','MyProtein Impact Whey Protein Chocolate Brownie 1kg','MyProtein','21g protein per serving, low fat and low sugar. European-sourced whey concentrate.',8,189.00,'QAR',219.00,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c122','Gatorade Lemon-Lime Sports Drink 600ml','PepsiCo','Electrolyte sports drink with sodium and potassium. Fuels performance and recovery.',8,6.50,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c123','Wilson Pro Staff Tennis Racket','Wilson','Professional carbon fibre racket. Advanced players'' choice on Qatar''s courts.',8,299.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c124','Adidas Ultraboost 22 Men''s Running Shoes','Adidas','Enhanced BOOST cushioning, breathable Primeknit+. Maximum energy return.',8,749.00,'QAR',899.00,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c125','Royal Canin Indoor Adult Cat Dry Food 4kg','Royal Canin','Formulated for indoor cats — controls hairballs, manages weight, supports digestion.',9,145.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c126','Pedigree Adult Dry Dog Food Beef & Vegetables 3kg','Mars Petcare','Complete dry dog food. Supports healthy digestion, strong teeth, shiny coat.',9,65.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c127','Whiskas Adult Tuna in Jelly Wet Cat Food 12x85g','Mars Petcare','Twelve pouches of tuna in jelly. High moisture, balanced nutrition.',9,55.00,'QAR',65.00,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c128','Kong Classic Natural Rubber Dog Toy Medium','Kong','Durable natural rubber toy. Fill with treats to keep dogs mentally stimulated.',9,55.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c129','Cat''s Best Oko Plus Clumping Cat Litter 10L','Cat''s Best','Wood-fibre clumping litter. 100% organic, biodegradable, superior odour control.',9,38.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c130','Royal Canin Kitten Dry Food 2kg','Royal Canin','Complete nutrition for kittens up to 12 months. Supports healthy growth and immune system.',9,89.00,'QAR',NULL,true,'high',NULL,NULL,4.8,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c131','Pedigree Puppy Dry Dog Food Chicken & Rice 3kg','Mars Petcare','Specially formulated for puppies. DHA from fish oil supports brain development.',9,72.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c132','Duracell Optimum AA Batteries 12 Pack','Duracell','Longest-lasting AA batteries — up to 13% extra life vs Duracell Plus.',10,28.00,'QAR',NULL,true,'high',NULL,NULL,4.7,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c133','3M Aura N95 Disposable Respirator 10 Pieces','3M','N95-rated, three-panel design for comfortable fit. Filters 95%+ of airborne particles.',10,45.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c134','Dettol Hand Sanitizer Instant Gel 500ml','Reckitt','Kills 99.9% of germs without water. Fast-drying, gentle on skin.',10,18.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c135','Scotch Magic Tape 19mm x 33m','3M','Invisible tape — writes and copies without showing. Strong adhesion, easy to hand-tear.',10,6.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c136','Post-it Original Notes 3x3 Assorted Colours 12 Pads','3M','12 pads of the original repositionable Post-it notes. 100 sheets per pad.',10,22.00,'QAR',NULL,true,'high',NULL,NULL,4.5,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c137','Energizer MAX AA Batteries 10 Pack','Energizer','Long-lasting alkaline batteries that hold power for up to 10 years in storage.',10,25.00,'QAR',NULL,true,'high',NULL,NULL,4.6,NULL,'2026-06-26 15:55:09.901789+00');
INSERT INTO public.products VALUES ('snu-c138','Pritt Stick Glue 43g','Henkel','Clean, washable glue stick — mess-free adhesive for school and office projects.',10,8.00,'QAR',NULL,true,'high',NULL,NULL,4.4,NULL,'2026-06-26 15:55:09.901789+00');


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

\unrestrict cznfCrh011aXx2WgnIIH7HXTdkggUATtzGQRUYrgN4XKaYgXVbIM2o4ZTTOZM9o
