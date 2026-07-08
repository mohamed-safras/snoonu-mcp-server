#!/usr/bin/env python3
"""
Fetches confirmed product image URLs via two strategies:
  1. Wikipedia pageimages API  — for brand/product articles (fast, reliable)
  2. OpenFoodFacts barcode API — for packaged foods with known EAN-13 codes

Outputs scripts/product_image_map.json  (product_id → image_url)
generate_seed.py reads this as a fallback for products with no hardcoded image.

Usage:
    python scripts/fetch_product_images.py
"""
import json
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# ─── Wikipedia page → product IDs that should use its thumbnail ──────────────
# Each entry: (wikipedia_page_title, [product_ids that share this brand image])
WIKIPEDIA_BRAND_IMAGES = [
    # Soft drinks
    ("Pepsi",           ["snu-c025", "extra-pepsi-bottle"]),
    ("7 Up",            ["snu-c026"]),
    ("Mountain Dew",    ["extra-mountain-dew"]),
    ("Fanta",           ["extra-fanta-orange", "extra-fanta-grape"]),
    ("Sprite (drink)",  ["extra-sprite"]),
    ("Schweppes",       ["extra-schweppes"]),
    ("Red Bull",        ["extra-redbull"]),
    ("Monster Energy",  ["extra-monster"]),
    ("Vimto",           ["extra-vimto"]),
    # Snacks
    ("Doritos",         ["snu-c054", "snu-c055"]),
    ("Lay's",           ["snu-c056", "snu-c057"]),
    ("Twix",            ["snu-c060"]),
    ("Snickers",        ["snu-c061"]),
    ("M&M's",           ["snu-c062"]),
    ("Bounty (chocolate bar)", ["extra-bounty"]),
    ("Galaxy (chocolate)",     ["extra-galaxy"]),
    ("After Eight",     ["extra-after-eight"]),
    ("Ferrero Rocher",  ["extra-ferrero", "snu-c183"]),
    ("Toblerone",       ["extra-toblerone"]),
    ("Kinder Bueno",    ["extra-kinder-bueno"]),
    ("Raffaello (confectionery)", ["extra-raffaello"]),
    ("Haribo",          ["extra-haribo"]),
    ("Oreo",            ["extra-oreo"]),
    ("McVitie's",       ["extra-mcvities"]),
    ("Godiva Chocolatier", ["snu-c184"]),
    # Cereals
    ("Corn Flakes",     ["extra-cornflakes"]),
    ("Kellogg's Frosties", ["extra-frosties"]),
    ("Kellogg's Special K", ["extra-special-k"]),
    ("Coco Pops",       ["extra-coco-pops"]),
    ("Weetabix",        ["extra-weetabix"]),
    ("Quaker Oats",     ["extra-quaker"]),
    ("Nature Valley",   ["extra-nature-valley"]),
    # Pasta
    ("Barilla",         ["extra-barilla-spaghetti", "extra-barilla-penne"]),
    # Condiments
    ("Tabasco sauce",   ["extra-tabasco"]),
    ("Hellmann's",      ["snu-c067", "extra-hellmanns-light"]),
    ("Kikkoman",        ["extra-kikkoman"]),
    ("Nando's",         ["extra-nandos"]),
    ("HP Sauce",        ["extra-hp-sauce"]),
    # Spreads & Sweet
    ("Biscoff",         ["extra-lotus"]),
    ("Skippy (peanut butter)", ["extra-skippy"]),
    # Dairy & Eggs
    ("Arla Foods",      ["extra-arla-organic"]),
    ("Kraft Singles",   ["extra-kraft-cheddar"]),
    # Bread & Bakery
    ("Almarai",         ["snu-c040", "snu-c041", "extra-almarai-brown-toast", "extra-brioche"]),
    ("Croissant",       ["snu-c187", "snu-c188"]),
    ("Pita bread",      ["snu-c043"]),
    # Water
    ("Volvic",          ["extra-volvic"]),
    ("Masafi",          ["extra-masafi"]),
    ("Perrier",         ["extra-perrier"]),
    ("Evian",           ["snu-c017", "snu-c018", "snu-c019", "snu-c020",
                          "extra-rayyan-spark-small", "extra-rayyan-spark-large"]),
    # Juice
    ("Tropicana (brand)", ["extra-tropicana"]),
    ("Rubicon (brand)", ["extra-rubicon"]),
    ("Minute Maid",     ["extra-minute-maid"]),
    # Rice
    ("Basmati rice",    ["snu-c064", "extra-daawat"]),
    ("Rice",            ["extra-egyptian-rice"]),
    # Lentils & legumes
    ("Lentil",          ["extra-red-lentils"]),
    ("Chickpea",        ["extra-chickpeas"]),
    ("Couscous",        ["extra-couscous"]),
    # Canned
    ("Baked beans",     ["extra-heinz-beans"]),
    ("Sardine",         ["extra-sardines"]),
    ("Sweetcorn",       ["extra-sweetcorn"]),
    # Frozen
    ("McCain Foods",    ["extra-mccain-chips"]),
    ("Chicken nuggets", ["extra-chicken-nuggets", "snu-c066"]),
    # Honey & Oil
    ("Sidr honey",      ["extra-sidr-honey"]),
    ("Extra virgin olive oil", ["extra-olive-oil"]),
    ("Sunflower oil",   ["extra-sunflower-oil"]),
    # Spices
    ("Biryani",         ["extra-shan-biryani"]),
    # Coffee
    ("Lavazza",         ["snu-c213", "snu-c214", "snu-c215", "extra-lavazza"]),
    ("Illy",            ["snu-c216", "snu-c217"]),
    ("Nespresso",       ["snu-c218", "snu-c219"]),
    ("Starbucks",       ["snu-c226", "snu-c227"]),
    ("Dolce Gusto",     ["snu-c228", "snu-c229"]),
    ("Keurig",          ["snu-c230"]),
    ("Bialetti",        ["snu-c222"]),
    ("Chemex",          ["snu-c223"]),
    ("Hario",           ["snu-c224"]),
    ("AeroPress",       ["snu-c225"]),
    ("Gooseneck kettle", ["snu-c231"]),
    ("Coffee grinder",  ["snu-c232"]),
    ("Costa Coffee",    ["snu-c235"]),
    ("Twinings",        ["snu-c234", "extra-twinings-eb", "extra-twinings-gl"]),
    ("Ahmad Tea",       ["snu-c038", "snu-c233", "extra-ahmad-earl", "extra-ahmad-green"]),
    ("Jacobs (coffee)", ["snu-c237"]),
    # Tea / Coffee add
    ("Chamomile tea",   ["extra-chamomile"]),
    ("Karak chai",      ["extra-karak-chai"]),
    # Dates (use local-style)
    ("Medjool",         ["snu-c045", "snu-c046", "snu-c047", "snu-c050"]),
    ("Bateel",          ["snu-c048", "snu-c049"]),
    # Flowers
    ("Rose",            ["snu-c069", "extra-pink-rose", "extra-white-rose",
                          "extra-yellow-rose", "extra-mixed-rose"]),
    ("Bouquet",         ["snu-c070", "snu-c075", "snu-c076"]),
    ("Orchid",          ["snu-c071", "extra-purple-orchid"]),
    ("Sunflower",       ["snu-c075"]),
    ("Tulip",           ["extra-tulip"]),
    ("Peony",           ["extra-peony"]),
    ("Succulent plant", ["extra-succulent"]),
    ("Peace lily",      ["extra-peace-lily"]),
    ("Pothos",          ["extra-money-plant"]),
    # Gift hampers
    ("Gift hamper",     ["snu-c072", "snu-c073", "extra-choc-hamper",
                          "extra-eid-hamper", "extra-ramadan-hamper"]),
    ("Balloon",         ["snu-c074", "extra-grad-balloon", "extra-foil-30"]),
    ("Scented candle",  ["extra-scented-candle"]),
    ("Baby shower",     ["extra-baby-hamper"]),
    # Health & Beauty
    ("Paracetamol",     ["snu-c077", "snu-c139"]),
    ("Ibuprofen",       ["snu-c140"]),
    ("Diclofenac",      ["snu-c141"]),
    ("Loratadine",      ["snu-c142"]),
    ("Nifuroxazide",    ["snu-c143"]),
    ("Omeprazole",      ["snu-c144"]),
    ("Betadine",        ["snu-c147"]),
    ("Thermometer",     ["snu-c150", "snu-c151"]),
    ("Blood pressure monitor", ["snu-c149"]),
    ("Vicks VapoRub",   ["snu-c078", "snu-c152"]),
    ("Dextromethorphan", ["snu-c153"]),  # cough syrup
    ("Throat lozenge",  ["snu-c154", "extra-strepsils"]),
    ("Paediatric paracetamol", ["snu-c155"]),
    ("Adhesive bandage", ["snu-c156", "extra-elastoplast-box"]),
    ("Blister (skin)",  ["snu-c157"]),
    ("Glucometer",      ["snu-c158"]),
    ("Eye drops",       ["snu-c159", "snu-c160"]),
    ("Antispasmodic",   ["snu-c161"]),
    ("Oral rehydration therapy", ["snu-c162"]),
    ("Nasal spray",     ["snu-c163"]),
    ("Vitamin C",       ["snu-c080"]),
    ("Centrum",         ["snu-c079", "extra-centrum-women"]),
    ("Dove (toiletries)", ["snu-c081", "extra-dove-body"]),
    ("Head & Shoulders", ["snu-c082"]),
    ("Nivea",           ["snu-c083", "extra-nivea-lotion"]),
    ("Colgate",         ["snu-c084", "extra-colgate-max"]),
    ("Garnier",         ["snu-c085", "extra-garnier"]),
    ("Neutrogena",      ["snu-c086", "extra-neutrogena-hand"]),
    ("Dettol",          ["snu-c087"]),
    ("Pantene",         ["snu-c088"]),
    ("CeraVe",          ["extra-cerave"]),
    ("Cetaphil",        ["extra-cetaphil"]),
    ("The Ordinary",    ["extra-ordinary-niacinamide", "extra-ordinary-ha"]),
    ("Olay",            ["extra-olay"]),
    ("Bioderma",        ["extra-bioderma"]),
    ("Vaseline",        ["extra-vaseline"]),
    ("TRESemmé",        ["extra-tresemme"]),
    ("Garnier Fructis", ["extra-garnier-fructis"]),
    ("Schwarzkopf",     ["extra-schwarzkopf"]),
    ("OGX",             ["extra-ogx"]),
    ("Sensodyne",       ["extra-sensodyne"]),
    ("Listerine",       ["extra-listerine"]),
    ("Oral-B",          ["extra-oral-b"]),
    ("Deodorant",       ["extra-dove-men-deo", "extra-rexona"]),
    ("Gillette",        ["extra-gillette"]),
    ("Veet",            ["extra-veet"]),
    ("Voltaren",        ["extra-voltaren-gel"]),
    ("Omega-3",         ["extra-omega3"]),
    ("Vitamin D",       ["extra-vitamin-d"]),
    ("Biotin",          ["extra-biotin"]),
    ("Probiotic",       ["extra-probiotic"]),
    ("Collagen",        ["extra-collagen"]),
    ("Berocca",         ["extra-berocca"]),
    ("Calcium",         ["extra-calcium"]),
    ("Melatonin",       ["extra-melatonin"]),
    ("Turmeric supplement", ["extra-turmeric"]),
    # Baby
    ("Pampers",         ["snu-c189", "snu-c190", "snu-c191", "extra-pampers-size3",
                          "snu-c192"]),
    ("Huggies",         ["snu-c193", "snu-c194", "extra-huggies-size5"]),
    ("Johnson's Baby",  ["snu-c195", "snu-c196", "snu-c197", "snu-c198"]),
    ("Aptamil",         ["snu-c199", "snu-c200", "extra-aptamil-stage1"]),
    ("Cerelac",         ["snu-c202", "snu-c203"]),
    ("Sudocrem",        ["snu-c205"]),
    ("Mustela",         ["snu-c206"]),
    ("Philips Avent",   ["snu-c207"]),
    ("Baby pacifier",   ["snu-c208"]),
    ("Baby stroller",   ["snu-c209"]),
    ("Baby carrier",    ["snu-c210"]),
    ("Swaddle",         ["snu-c211"]),
    ("Baby monitor",    ["snu-c212"]),
    ("NAN (formula)",   ["snu-c201"]),
    # Electronics
    ("Apple AirPods",   ["snu-c089"]),
    ("Samsung Galaxy Buds", ["snu-c090"]),
    ("JBL (brand)",     ["snu-c091", "snu-c097"]),
    ("Anker (company)", ["snu-c092", "extra-anker-charger", "extra-anker-powerbank"]),
    ("Sony WH-1000XM5", ["snu-c093"]),
    ("Samsung QLED",    ["snu-c095"]),
    ("Xiaomi Mi Band",  ["snu-c096"]),
    ("Dell XPS",        ["snu-c252"]),
    ("HP Spectre",      ["snu-c253"]),
    ("ASUS ROG",        ["snu-c254"]),
    ("Dell UltraSharp", ["snu-c256"]),
    ("Samsung Odyssey", ["snu-c257"]),
    ("Sony ZV-E10",     ["snu-c259"]),
    ("Keychron",        ["snu-c265"]),
    ("Samsung 870 EVO", ["snu-c267"]),
    ("Western Digital My Passport", ["snu-c268"]),
    ("TP-Link Deco",    ["snu-c269"]),
    ("Elgato Stream Deck", ["snu-c270"]),
    ("Apple AirTag",    ["snu-c271"]),
    ("DJI OM",          ["snu-c272"]),
    ("Samsung Galaxy A55", ["extra-galaxy-a55"]),
    ("Google Pixel 8",  ["extra-google-pixel8"]),
    ("OnePlus 12",      ["extra-oneplus12"]),
    ("Garmin Fenix",    ["extra-garmin-fenix"]),
    ("Fitbit Charge",   ["extra-fitbit-charge6"]),
    ("Beats Studio",    ["extra-beats-studio"]),
    ("Jabra",           ["extra-jabra"]),
    ("Shure MV7",       ["extra-shure-mv7"]),
    ("BenQ ScreenBar",  ["extra-benq-screenbar"]),
    ("Seagate Expansion", ["extra-seagate"]),
    ("SanDisk Extreme", ["extra-sandisk"]),
    ("PlayStation 5 DualSense", ["extra-dualsense-white"]),
    ("Xbox controller", ["extra-xbox-controller"]),
    ("Spigen",          ["extra-spigen"]),
    ("Belkin",          ["extra-belkin"]),
    ("Bose QuietComfort 45", ["extra-bose-qc45"]),
    ("Logitech MX Master", ["extra-mx-master"]),
    ("Logitech MX Keys", ["extra-mx-keys"]),
    ("Marshall Emberton", ["extra-marshall"]),
    ("Google Nest Mini", ["extra-nest-mini"]),
    ("Amazon Echo",     ["extra-echo-dot"]),
    ("TP-Link Tapo",    ["extra-tapo-plug"]),
    ("Philips Hue",     ["extra-philips-hue"]),
    ("Ring (doorbell)", ["extra-ring-doorbell"]),
    ("GoPro",           ["extra-gopro"]),
    ("Corsair K70",     ["extra-corsair-k70"]),
    ("Elgato",          ["extra-elgato-4k"]),
    ("Apple HomePod",   ["extra-homepod"]),
    ("Govee",           ["extra-govee"]),
    ("Razer Kraken",    ["extra-razer-kraken"]),
    ("SteelSeries",     ["extra-steelseries"]),
    ("ASUS ZenScreen",  ["extra-zenscreen"]),
    # Fashion
    ("Nike Air Force 1", ["extra-af1"]),
    ("Adidas Gazelle",  ["extra-adidas-gazelle"]),
    ("New Balance 574", ["extra-nb574"]),
    ("Converse Chuck Taylor", ["extra-converse"]),
    ("Vans Old Skool",  ["extra-vans"]),
    ("Timberland",      ["extra-timberland"]),
    ("Levi's 511",      ["extra-levis511"]),
    ("Polo shirt",      ["snu-c101", "extra-lacoste-polo", "extra-ralph-lauren-tee"]),
    ("Nike hoodie",     ["extra-nike-hoodie"]),
    ("Herschel backpack", ["extra-herschel"]),
    ("Samsonite",       ["extra-samsonite"]),
    ("Pandora bracelet", ["extra-pandora"]),
    ("Oakley Holbrook", ["extra-oakley"]),
    ("Calvin Klein belt", ["snu-c102"]),
    ("Fossil watch",    ["snu-c103", "extra-fossil-minimalist"]),
    ("Daniel Wellington", ["extra-dw-watch"]),
    ("Ray-Ban Aviator", ["snu-c098"]),
    ("Nike Air Max",    ["snu-c099"]),
    ("Adidas Stan Smith", ["snu-c100"]),
    # Home & Garden
    ("Tefal",           ["snu-c104"]),
    ("Ariel (detergent)", ["snu-c105", "extra-persil"]),
    ("Dettol spray",    ["snu-c106"]),
    ("Trash bag",       ["snu-c107"]),
    ("Air purifier",    ["snu-c108"]),
    ("Oral-B toothbrush", ["snu-c109"]),
    ("Finish (brand)",  ["snu-c110"]),
    ("Sponge",          ["snu-c111"]),
    ("Philips Airfryer", ["extra-air-fryer"]),
    ("Instant Pot",     ["extra-instant-pot"]),
    ("Vitamix",         ["extra-vitamix"]),
    ("Russell Hobbs",   ["extra-russell-hobbs"]),
    ("Smeg",            ["extra-smeg-toaster"]),
    ("Le Creuset",      ["extra-le-creuset"]),
    ("Zwilling",        ["extra-zwilling"]),
    ("OXO",             ["extra-oxo"]),
    ("Tupperware",      ["extra-tupperware"]),
    ("Comfort (fabric softener)", ["extra-comfort-blue"]),
    ("Fairy (brand)",   ["extra-fairy", "extra-fairy-lemon"]),
    ("Dyson V12",       ["extra-dyson"]),
    ("Lysol",           ["extra-lysol"]),
    ("Febreze",         ["extra-febreze"]),
    ("Yankee Candle",   ["extra-yankee"]),
    ("Miracle-Gro",     ["extra-miracle-gro"]),
    ("Terracotta pot",  ["extra-ikea-pots"]),
    # Toys
    ("LEGO",            ["snu-c112", "extra-lego-city", "extra-lego-duplo", "extra-lego-creator"]),
    ("Hot Wheels",      ["snu-c113"]),
    ("Barbie",          ["snu-c114", "extra-barbie-dreamhouse", "extra-barbie-elsa"]),
    ("Pampers (toys cat)", ["extra-pampers-size3"]),
    ("Huggies (toys cat)", ["extra-huggies-size5"]),
    ("Similac",         ["snu-c117", "extra-similac-stage2"]),
    ("Play-Doh",        ["snu-c118"]),
    ("Spider-Man",      ["extra-spiderman"]),
    ("Monopoly",        ["extra-monopoly"]),
    ("Catan",           ["extra-catan"]),
    ("Scrabble",        ["extra-scrabble"]),
    ("Jigsaw puzzle",   ["extra-jigsaw"]),
    ("Baby gym",        ["extra-fisher-price-gym"]),
    ("Nerf",            ["extra-nerf"]),
    ("Razor scooter",   ["extra-razor-scooter"]),
    ("Playmobil",       ["extra-playmobil"]),
    ("Melissa & Doug",  ["extra-melissa-doug"]),
    ("VTech",           ["extra-vtech-walker", "snu-c212"]),
    # Sports
    ("Football",        ["extra-adidas-ball", "extra-nike-ball"]),
    ("Basketball",      ["extra-spalding"]),
    ("Running shoes",   ["extra-brooks-ghost"]),
    ("Garmin Forerunner", ["extra-garmin-forerunner"]),
    ("Whey protein",    ["snu-c121", "extra-on-gold-standard"]),
    ("BSN Syntha",      ["extra-bsn-syntha"]),
    ("Protein bar",     ["extra-quest-bars"]),
    ("Yoga mat",        ["snu-c120", "extra-manduka"]),
    ("Swimming goggles", ["extra-speedo"]),
    ("Tennis ball",     ["extra-wilson-balls"]),
    ("TRX Training",    ["extra-trx"]),
    ("Adjustable dumbbell", ["extra-bowflex"]),
    ("Gatorade",        ["snu-c122", "extra-gatorade-orange"]),
    ("Clif Bar",        ["extra-clif-bar"]),
    ("Snorkel set",     ["extra-cressi"]),
    ("Compression socks", ["extra-2xu-socks"]),
    ("Camping tent",    ["extra-msr-tent"]),
    ("Nike training shirt", ["snu-c119"]),
    ("Adidas Ultraboost", ["snu-c124"]),
    ("Wilson tennis racket", ["snu-c123"]),
    # Pets
    ("Royal Canin",     ["snu-c125", "snu-c130", "extra-royal-canin-persian"]),
    ("Pedigree (pet food)", ["snu-c126", "snu-c131"]),
    ("Whiskas",         ["snu-c127"]),
    ("Kong (dog toy)",  ["snu-c128", "extra-kong-extreme"]),
    ("Cat litter",      ["snu-c129"]),
    ("Hill's Science Diet", ["extra-hills-cat", "extra-hills-dog"]),
    ("Sheba (cat food)", ["extra-sheba"]),
    ("Temptations (pet food)", ["extra-temptations"]),
    ("Catit",           ["extra-catit"]),
    ("PetSafe",         ["extra-petsafe"]),
    ("Purina Pro Plan", ["extra-purina-salmon"]),
    ("Dentastix",       ["extra-dentastix"]),
    ("Ruffwear",        ["extra-ruffwear"]),
    ("FURminator",      ["extra-furminator"]),
    ("Aquarium",        ["extra-tetra-aquarium"]),
    ("Fish tank test kit", ["extra-api-test"]),
    ("Hamster food",    ["extra-kaytee"]),
    # Market / Office
    ("Pilot G2 pen",    ["extra-pilot-g2"]),
    ("Stabilo",         ["extra-stabilo"]),
    ("Sharpie",         ["extra-sharpie"]),
    ("Moleskine",       ["extra-moleskine"]),
    ("Leuchtturm1917",  ["extra-leuchtturm"]),
    ("Watercolor pencils", ["extra-arteza"]),
    ("Faber-Castell",   ["extra-faber"]),
    ("Bic Cristal",     ["extra-bic"]),
    ("LED light bulb",  ["extra-philips-led", "extra-osram"]),
    ("First aid kit",   ["extra-jj-first-aid"]),
    ("Bleach",          ["extra-domestos"]),
    ("Command strips",  ["extra-command-strips"]),
    ("Velcro",          ["extra-velcro"]),
    ("Whiteboard",      ["extra-whiteboard"]),
    ("Duracell",        ["snu-c132", "extra-duracell-procell"]),
    ("Energizer",       ["snu-c137", "extra-energizer-lithium"]),
    ("3M (company)",    ["snu-c133", "snu-c135", "snu-c136", "extra-command-strips"]),
    ("Dettol hand sanitizer", ["snu-c134"]),
    ("Pritt stick",     ["snu-c138"]),
    # Arabic Sweets — use food/dessert articles
    ("Kunafa",          ["snu-c164", "snu-c165"]),
    ("Luqaimat",        ["snu-c166"]),
    ("Baklava",         ["snu-c167"]),
    ("Maamoul",         ["snu-c168", "snu-c169"]),
    ("Basbousa",        ["snu-c170"]),
    ("Om Ali",          ["snu-c171"]),
    ("Muhallebi",       ["snu-c172"]),
    ("Halva",           ["snu-c173", "snu-c177"]),
    ("Turkish delight", ["snu-c174"]),
    ("Qatayef",         ["snu-c175"]),
    ("Bird's nest baklava", ["snu-c176"]),
    ("Sfouf",           ["snu-c178"]),
    ("Petit four",      ["snu-c179"]),
    ("Ghraybe",         ["snu-c180"]),
    ("Kaak",            ["snu-c181"]),
    ("Harees",          ["snu-c182"]),
    ("Eid gift",        ["snu-c186"]),
    ("Croissant",       ["snu-c187", "snu-c188"]),
]


# ─── Direct OpenFoodFacts barcode lookups (EAN-13, confirmed international) ──
# Format: (product_id, barcode)
OFF_BARCODE_LOOKUPS = [
    # Grocery / Drinks
    ("snu-c025",  "5449000003041"),  # Pepsi 330ml EU
    ("snu-c026",  "5449000020963"),  # 7UP 330ml EU
    ("extra-fanta-orange", "5449000214676"),  # Fanta Orange EU
    ("extra-sprite", "5449000131935"),  # Sprite EU
    ("extra-redbull", "9002490200070"),  # Red Bull 250ml
    ("extra-monster", "070847814535"),  # Monster Original 500ml
    ("snu-c054",  "028400090827"),  # Doritos Nacho Cheese
    ("snu-c055",  "028400516310"),  # Doritos Cool Ranch
    ("snu-c056",  "028400028059"),  # Lay's Classic
    ("snu-c057",  "028400098427"),  # Lay's BBQ
    ("snu-c060",  "040000001430"),  # Twix
    ("snu-c061",  "040000001409"),  # Snickers
    ("snu-c062",  "040000001386"),  # M&Ms Peanut
    ("extra-bounty", "5000159390101"),  # Bounty
    ("extra-after-eight", "7613036985765"),  # After Eight 200g
    ("extra-ferrero", "8000500136713"),  # Ferrero Rocher 16
    ("extra-toblerone", "7622210951403"),  # Toblerone 100g
    ("extra-kinder-bueno", "8000500019443"),  # Kinder Bueno
    ("extra-raffaello", "8000500148655"),  # Raffaello 150g
    ("extra-haribo", "4001686300107"),  # Haribo Gold Bears
    ("extra-oreo", "044000030506"),  # Oreo 154g
    ("extra-cornflakes", "038000199066"),  # Kellogg's Corn Flakes
    ("extra-quaker", "030000010181"),  # Quaker Oats
    ("extra-weetabix", "5000116101013"),  # Weetabix Original
    ("extra-barilla-spaghetti", "076808000012"),  # Barilla Spaghetti
    ("extra-tabasco", "011210000048"),  # Tabasco Original
    ("snu-c067",  "048001009191"),  # Hellmann's Real Mayo
    ("snu-c088",  "030772013588"),  # Pantene Pro-V Smooth
    ("snu-c082",  "030772011683"),  # Head & Shoulders
    ("snu-c084",  "8714789787809"),  # Colgate Total 150g
    ("snu-c078",  "3014260104498"),  # Vicks VapoRub 50g
    ("snu-c081",  "8717644007243"),  # Dove Body Wash 500ml
    # Baby
    ("snu-c195",  "381370013784"),  # Johnson's Baby Shampoo
    # Coffee
    ("snu-c213",  "8000070011267"),  # Lavazza Qualità Rossa
    ("snu-c216",  "8003753000060"),  # illy Classico Ground 250g
    ("snu-c218",  "7630039648673"),  # Nespresso Ristretto
    ("snu-c226",  "762111490005"),  # Starbucks House Blend
    # Grocery extras
    ("extra-lotus", "5410126020071"),  # Lotus Biscoff Spread
    ("extra-skippy", "037600329484"),  # Skippy Peanut Butter Smooth
    ("extra-coco-pops", "5059319004734"),  # Coco Pops
    ("extra-kikkoman", "4100840001008"),  # Kikkoman Soy Sauce
]


def fetch_wikipedia_thumbnail(page_title: str) -> str | None:
    """Return thumbnail URL for a Wikipedia article (English)."""
    encoded_title = urllib.parse.quote(page_title)
    api_url = (
        "https://en.wikipedia.org/w/api.php"
        "?action=query"
        f"&titles={encoded_title}"
        "&prop=pageimages"
        "&pithumbsize=400"
        "&format=json"
        "&redirects=1"
    )
    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "snoonu-seed-image-fetcher/1.0 (demo project)"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            thumbnail = page.get("thumbnail", {})
            source_url = thumbnail.get("source")
            if source_url:
                return source_url
    except Exception as error:
        print(f"  wiki error [{page_title}]: {error}", file=sys.stderr)
    return None


def fetch_off_barcode(product_id: str, barcode: str) -> tuple[str, str | None]:
    """Look up a product image from OpenFoodFacts by EAN barcode."""
    # Format barcode path: last 4 digits separate, preceding in groups of 3
    barcode_str = barcode.zfill(13)  # pad to 13 digits
    path = f"{barcode_str[:3]}/{barcode_str[3:6]}/{barcode_str[6:9]}/{barcode_str[9:]}"
    candidate_url = f"https://images.openfoodfacts.org/images/products/{path}/1.400.jpg"

    try:
        req = urllib.request.Request(
            candidate_url,
            method="HEAD",
            headers={"User-Agent": "snoonu-seed-verify/1.0"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                return product_id, candidate_url
    except Exception:
        pass

    # Also try the OFF product API to find the actual image
    api_url = (
        f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        "?fields=image_front_url,image_url"
    )
    try:
        req = urllib.request.Request(
            api_url,
            headers={"User-Agent": "snoonu-seed-image-fetcher/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        product_data = data.get("product", {})
        image_url = product_data.get("image_front_url") or product_data.get("image_url")
        if image_url and image_url.startswith("https://"):
            # Convert to raw stable format
            if "/images/products/" in image_url and "front_" in image_url:
                image_url = image_url.rsplit("/", 1)[0] + "/1.400.jpg"
            return product_id, image_url
    except Exception as error:
        print(f"  off error [{product_id} / {barcode}]: {error}", file=sys.stderr)

    return product_id, None


def main() -> None:
    output_path = SCRIPT_DIR / "product_image_map.json"

    existing_map: dict[str, str] = {}
    if output_path.exists():
        existing_map = json.loads(output_path.read_text(encoding="utf-8"))
        print(f"Loaded {len(existing_map)} existing entries", file=sys.stderr)

    confirmed_map: dict[str, str] = dict(existing_map)

    # ── Step 1: Wikipedia thumbnails (fast, parallel) ────────────────────────
    wiki_lookups_needed = [
        (title, product_ids)
        for title, product_ids in WIKIPEDIA_BRAND_IMAGES
        if any(pid not in confirmed_map for pid in product_ids)
    ]
    print(f"\nFetching {len(wiki_lookups_needed)} Wikipedia brand images…", file=sys.stderr)

    for title, product_ids in wiki_lookups_needed:
        thumbnail_url = fetch_wikipedia_thumbnail(title)
        if thumbnail_url:
            for product_id in product_ids:
                if product_id not in confirmed_map:
                    confirmed_map[product_id] = thumbnail_url
            print(f"  ✓ [{title}] → {len(product_ids)} products", file=sys.stderr)
        else:
            print(f"  ✗ [{title}]", file=sys.stderr)
        time.sleep(0.3)  # stay under Wikipedia's rate limit

    # ── Step 2: OpenFoodFacts barcode lookups (sequential, polite) ───────────
    off_needed = [
        (pid, barcode)
        for pid, barcode in OFF_BARCODE_LOOKUPS
        if pid not in confirmed_map
    ]
    print(f"\nLooking up {len(off_needed)} OFF barcodes…", file=sys.stderr)

    for product_id, barcode in off_needed:
        pid_result, url_result = fetch_off_barcode(product_id, barcode)
        if url_result:
            confirmed_map[pid_result] = url_result
            print(f"  ✓ {pid_result} ({barcode})", file=sys.stderr)
        else:
            print(f"  ✗ {pid_result} ({barcode})", file=sys.stderr)
        time.sleep(0.3)  # be polite to OFF API

    # ── Save ─────────────────────────────────────────────────────────────────
    output_path.write_text(
        json.dumps(confirmed_map, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nSaved {len(confirmed_map)} entries to {output_path.name}", file=sys.stderr)
    new_count = len(confirmed_map) - len(existing_map)
    print(f"New entries this run: {new_count}", file=sys.stderr)


if __name__ == "__main__":
    main()
