from django.core.management.base import BaseCommand
from faker import Faker
from biapp.models import Receipt, ReceiptItem, Cashier, Store, Client, Discount, Product
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Populate database with test data"

    def handle(self, *args, **kwargs):
        PRODUCT_NUM = 1000
        STORE_NUM = 20
        CASHIER_NUM = 200
        fake = Faker()
        product_names = generate_product_names(1000)
        for i in range(PRODUCT_NUM):
            rand_price = fake.random_int(100, 100000)
            product = Product(name=product_names[i], price=rand_price)
            product.save()

        for _ in range(STORE_NUM):
            store_location = fake.street_address()
            store = Store(location=store_location)
            store.save()
            
        for _ in range(CASHIER_NUM):
            cashier_name = fake.name()
            cashier = Cashier(name=cashier_name)
            cashier.save()
        generate_and_save_discounts()
        self.stdout.write(self.style.SUCCESS("Database populated with init test data!"))
        
        
#returns list of random possible names for a shop's products
#length of the list - num
def generate_product_names(num):
    categories = [
        "Laptop", "Smartphone", "Headphones", "Camera", "Backpack", "Watch", "Shoes",
        "Shirt", "Pants", "Tablet", "TV", "Monitor", "Mouse", "Keyboard", "Chair",
        "Desk", "Sunglasses", "Hat", "Perfume", "Speaker", "Book", "Notebook", "Pen",
        "Toy", "Game", "Gloves", "Scarf", "Jacket", "Coat", "Sweater", "Boots",
        "Ring", "Necklace", "Bracelet", "Earrings", "Towel", "Pillow", "Blanket",
        "Bag", "Lamp", "Mirror", "Rug", "Plant", "Vase", "Cup", "Bottle", "Watch",
        "Bicycle", "Helmet", "Ball", "Tent", "Sleeping Bag", "Drill", "Hammer",
        "Saw", "Vacuum Cleaner", "Fan", "Iron", "Kettle", "Blender", "Microwave",
        "Oven", "Fridge", "Dishwasher", "Toaster", "Mixer", "Juicer", "Grill",
        "Cooker", "Freezer", "Clock", "Dresser", "Shelf", "Wardrobe", "Stroller",
        "Crib", "Diapers", "Pacifier", "Lotion", "Soap", "Shampoo", "Conditioner",
        "Toothpaste", "Toothbrush", "Hairdryer", "Straightener", "Curling Iron",
        "Socks", "Underwear", "Cap", "Headband", "Water Bottle", "Lunch Box", "Thermos",
        "Bread", "Milk", "Bottle of Water", "Eggs", "Chocolate bar", "Dragon", "Sword",
        "Axe", "Dragon", "Juice", "Rifle", "Bow", "Pigeon", "Chicken", "Knife", "Yogurt", "Sugar",
        "Salt", "Flour", "Plastic bag", "Mineral water", "Clip", "Tea", "Coffee", "Cheese", ""
    ]
    adjectives = [
        "Luxury", "Classic", "Modern", "Stylish", "Elegant", "Premium", "Durable",
        "Compact", "Portable", "Smart", "High-Tech", "Eco-Friendly", "Affordable",
        "Lightweight", "Advanced", "Ergonomic", "Foldable", "Wireless", "Bluetooth",
        "Waterproof", "Multi-functional", "Energy-Efficient", "Versatile", "Innovative",
        "Chic", "Comfortable", "Trendy", "Rugged", "Customized", "Unique", "Vintage",
        "Sophisticated", "Minimalist", "Soft", "Fluffy", "Cozy", "Handmade", "Organic",
        "Professional", "Secure", "Adjustable", "Silent", "Fast", "Compact", "Portable"
    ]
    product_names = set()
    while len(product_names) < num:
        product_name = f"{random.choice(adjectives)} {random.choice(categories)}"
        product_names.add(product_name)
    product_names_list = list(product_names)
    return product_names_list



#create and adds to the table some test discounts
def generate_and_save_discounts():
    discount_names = [
        "Winter Sale", "New Year Special", "Valentines",
        "Birthday offer", "Wedding special", "Secret sale"
    ]
    discount_types = ['percentage', 'fixed']
    start_date = datetime(2025, 1, 7)
    end_date = datetime(2025, 2, 7)
    for i in range(6):
        discount_start = start_date + timedelta(days=random.randint(0, 15))
        duration_days = random.choice([2, 3, 7, 10, 14, 20])
        discount_end = discount_start + timedelta(days=duration_days)
        if discount_end > end_date:
            discount_end = end_date
        discount = Discount(
            discount_name=discount_names[i],
            discount_type=random.choice(discount_types),
            discount_value=round(random.randint(10, 50) + random.randint(0, 99) / 100, 2),  
            discount_start=discount_start,
            discount_end=discount_end
        )
        discount.save()





    