import csv, random, uuid, datetime
from pathlib import Path

random.seed(2025)
output_dir = Path('.')

first_names = [
    "Ava","Liam","Noah","Emma","Olivia","Mason","Sophia","Isabella","Mia","Charlotte",
    "Ethan","Logan","Lucas","Amelia","Harper","Henry","Evelyn","Abigail","Elijah","James",
    "Sebastian","Daniel","Grace","Chloe","Aria","Layla","Zoe","Luna","Mila","Aiden",
    "Wyatt","Jack","Levi","Ella","Scarlett","Nora","Hannah","Lily","Aurora","Violet",
    "Penelope","Camila","Paisley","Hazel","Eleanor","Riley","Savannah","Brooklyn","Elena","Madison"
]
last_names = [
    "Smith","Johnson","Brown","Taylor","Anderson","Martinez","Lee","Garcia","Davis","Rodriguez",
    "Clark","Lewis","Walker","Hall","Allen","Young","Hernandez","King","Wright","Lopez",
    "Hill","Scott","Green","Adams","Baker","Nelson","Carter","Mitchell","Perez","Roberts",
    "Turner","Phillips","Campbell","Parker","Evans","Edwards","Collins","Stewart","Sanchez","Morris",
    "Rogers","Reed","Cook","Morgan","Bell","Murphy","Bailey","Rivera","Cooper","Richardson"
]

genders = ["female","male","non-binary"]
prime_bias = [True]*3 + [False]*2

country_details = [
    ("United States", "+1"),
    ("Canada", "+1"),
    ("United Kingdom", "+44"),
    ("Germany", "+49"),
    ("France", "+33"),
    ("Australia", "+61"),
    ("India", "+91"),
    ("Singapore", "+65"),
    ("United Arab Emirates", "+971"),
    ("Brazil", "+55")
]

def random_date(start, end):
    delta = end - start
    rand_days = random.randint(0, delta.days)
    rand_seconds = random.randint(0, 86399)
    return start + datetime.timedelta(days=rand_days, seconds=rand_seconds)

start_date = datetime.datetime(2024,1,1)
end_date = datetime.datetime(2025,11,1)

users = []
used_emails = set()
for _ in range(50):
    first = random.choice(first_names)
    last = random.choice(last_names)
    full_name = f"{first} {last}"
    base_email = f"{first}.{last}".lower()
    suffix = random.randint(10,99)
    email = f"{base_email}{suffix}@shopmail.com"
    while email in used_emails:
        suffix = random.randint(100,999)
        email = f"{base_email}{suffix}@shopmail.com"
    used_emails.add(email)
    country, dial = random.choice(country_details)
    phone = f"{dial}-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"
    created_at = random_date(start_date, end_date).isoformat()
    gender = random.choice(genders)
    age = random.randint(18,68)
    is_prime = random.choice(prime_bias)
    user = {
        "user_id": str(uuid.uuid4()),
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "created_at": created_at,
        "country": country,
        "gender": gender,
        "age": age,
        "is_prime_member": str(is_prime).lower()
    }
    users.append(user)

categories = {
    "Electronics": ["Smartphones","Laptops","Tablets","Wearables","Audio"],
    "Home": ["Kitchen","Furniture","Decor","Cleaning"],
    "Beauty": ["Skincare","Makeup","Haircare"],
    "Fashion": ["Footwear","Apparel","Bags","Outerwear"],
    "Fitness": ["Equipment","Athleisure","Supplements"],
    "Accessories": ["Watches","Jewelry","Travel","Smart Home"]
}

brands = {
    "Electronics": ["PulseTech","OrbitOne","NovaSound","AeroLink"],
    "Home": ["CasaPure","UrbanNest","BrightHive"],
    "Beauty": ["LuxeGlow","PureBloom","EvoDerm"],
    "Fashion": ["MetroThread","AtlasWear","VelvetLine"],
    "Fitness": ["CoreFlex","ZenMotion","PeakForm"],
    "Accessories": ["ChronosCo","HelioCraft","Voyageur"]
}

product_names = {
    "Smartphones": ["Pulse X2 5G","Orbit Edge Pro","NovaBeam Mini"],
    "Laptops": ["AeroLink Ultra","PulseBook Air","Orbit Flex 14"],
    "Tablets": ["NovaSlate 11","PulseTab Studio","OrbitPad Go"],
    "Wearables": ["ChronoFit Max","PulseBand Active","OrbitSense 3"],
    "Audio": ["NovaSound Arc","PulsePods Pro","OrbitWave Studio"],
    "Kitchen": ["CasaPure Air Fryer","UrbanNest Smart Blender","BrightHive Sous Vide"],
    "Furniture": ["UrbanNest Lift Desk","CasaPure Modular Sofa","BrightHive Ergo Chair"],
    "Decor": ["CasaPure Ambient Lamp","BrightHive Wall Art","UrbanNest Planter Set"],
    "Cleaning": ["BrightHive Robot Vac","CasaPure Steam Mop","UrbanNest Purifier"],
    "Skincare": ["LuxeGlow Hydrating Serum","PureBloom Barrier Cream","EvoDerm Night Mask"],
    "Makeup": ["PureBloom Velvet Lip Tint","LuxeGlow Radiant Palette","EvoDerm Weightless Mascara"],
    "Haircare": ["LuxeGlow Repair Oil","PureBloom Volume Mist","EvoDerm Balance Shampoo"],
    "Footwear": ["AtlasWear Knit Runner","MetroThread City Sneaker","VelvetLine Suede Boot"],
    "Apparel": ["MetroThread Tech Jacket","AtlasWear Utility Chino","VelvetLine Knit Dress"],
    "Bags": ["AtlasWear Transit Pack","VelvetLine Everyday Tote","MetroThread Flex Sling"],
    "Outerwear": ["MetroThread Parka","AtlasWear Rain Shell","VelvetLine Wool Coat"],
    "Equipment": ["CoreFlex Adjustable Kettlebell","PeakForm Resistance Kit","ZenMotion Smart Trainer"],
    "Athleisure": ["ZenMotion Sculpt Legging","CoreFlex Seamless Tee","PeakForm Hybrid Hoodie"],
    "Supplements": ["PeakForm Plant Protein","ZenMotion Focus Gummies","CoreFlex Recovery Drink"],
    "Watches": ["ChronosCo Meridian","HelioCraft Solar Watch","Voyageur Pilot"],
    "Jewelry": ["HelioCraft Halo Earrings","ChronosCo Axis Bracelet","Voyageur North Star Pendant"],
    "Travel": ["Voyageur Carbon Carry-On","HelioCraft Modular Pack","ChronosCo Tech Organizer"],
    "Smart Home": ["OrbitOne Smart Hub","NovaSound Multi-Room Speaker","PulseTech Secure Cam"]
}

products = []
seen_pairs = set()
while len(products) < 80:
    category = random.choice(list(categories.keys()))
    sub_category = random.choice(categories[category])
    names = product_names.get(sub_category)
    if not names:
        continue
    name = random.choice(names)
    brand = random.choice(brands[category])
    pair = (name, brand)
    if pair in seen_pairs:
        continue
    seen_pairs.add(pair)
    price = round(random.uniform(15, 2200), 2)
    rating = round(random.uniform(3.4, 4.9), 1)
    stock_quantity = random.randint(20, 600)
    product = {
        "product_id": str(uuid.uuid4()),
        "product_name": name,
        "category": category,
        "sub_category": sub_category,
        "brand": brand,
        "price": price,
        "rating": rating,
        "stock_quantity": stock_quantity
    }
    products.append(product)

payment_methods = ["credit_card","debit_card","paypal","apple_pay","google_pay","klarna"]
order_statuses = ["processing","shipped","delivered","cancelled","returned"]

orders = []
for _ in range(150):
    user = random.choice(users)
    order_date = random_date(datetime.datetime(2024,2,1), end_date).isoformat()
    status = random.choices(order_statuses, weights=[30,25,30,8,7])[0]
    payment = random.choices(payment_methods, weights=[35,20,15,10,10,10])[0]
    orders.append({
        "order_id": str(uuid.uuid4()),
        "user_id": user["user_id"],
        "order_date": order_date,
        "payment_method": payment,
        "order_status": status,
        "total_amount": 0.0
    })

base_counts = {order["order_id"]: 1 for order in orders}
remaining = 350 - len(orders)
order_ids = [order["order_id"] for order in orders]
for _ in range(remaining):
    base_counts[random.choice(order_ids)] += 1

order_items = []
for order in orders:
    oid = order["order_id"]
    for _ in range(base_counts[oid]):
        product = random.choice(products)
        quantity = random.randint(1, 4)
        price_per_unit = round(product["price"] * random.uniform(0.92, 1.05), 2)
        line_total = round(quantity * price_per_unit, 2)
        order_items.append({
            "order_item_id": str(uuid.uuid4()),
            "order_id": oid,
            "product_id": product["product_id"],
            "quantity": quantity,
            "price_per_unit": price_per_unit,
            "line_total": line_total
        })
        order["total_amount"] += line_total
    order["total_amount"] = round(order["total_amount"], 2)

reviews = []
review_text_options = [
    "Exceeded expectations in quality and delivery.",
    "Great value for the price and fast shipping.",
    "Product matches description and works as promised.",
    "Packaging was premium and setup was easy.",
    "Solid performance though battery life could be longer.",
    "Style and comfort are impressive.",
    "Reliable purchase; would recommend to friends.",
    "Met my needs but shipping took a little longer.",
    "Fantastic build quality and user-friendly features.",
    "Customer support resolved my queries quickly."
]

for _ in range(120):
    product = random.choice(products)
    user = random.choice(users)
    rating = random.randint(3,5)
    review_date = random_date(datetime.datetime(2024,3,1), end_date).isoformat()
    reviews.append({
        "review_id": str(uuid.uuid4()),
        "product_id": product["product_id"],
        "user_id": user["user_id"],
        "rating": rating,
        "review_text": random.choice(review_text_options),
        "review_date": review_date
    })


def write_csv(filename, fieldnames, rows):
    path = output_dir / filename
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv('users.csv', ["user_id","full_name","email","phone","created_at","country","gender","age","is_prime_member"], users)
write_csv('products.csv', ["product_id","product_name","category","sub_category","brand","price","rating","stock_quantity"], products)
write_csv('orders.csv', ["order_id","user_id","order_date","payment_method","order_status","total_amount"], orders)
write_csv('order_items.csv', ["order_item_id","order_id","product_id","quantity","price_per_unit","line_total"], order_items)
write_csv('reviews.csv', ["review_id","product_id","user_id","rating","review_text","review_date"], reviews)

print("Generated:", len(users), "users;", len(products), "products;", len(orders), "orders;", len(order_items), "order items;", len(reviews), "reviews")
