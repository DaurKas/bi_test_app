from biapp.models import Receipt, ReceiptItem, Cashier, Store, Client, Discount, Product
from biapp.serializers import ReceiptSerializer, CashierSerializer, StoreSerializer, ClientSerializer, DiscountSerializer, ProductSerializer
from faker import Faker
import datetime
from django.utils import timezone

import pandas as pd
import random
import json


#generate single receipt json struct
def generate_mock_receipt():
    fake = Faker()
    cashier = CashierSerializer(random.choice(Cashier.objects.all()))
    store = StoreSerializer(random.choice(Store.objects.all()))
    client_name = fake.name()
    products = list(Product.objects.all())
    items = []
    num_items = random.randint(1, 10)
    total_amount = 0
    
    for _ in range(num_items):
        product_object = random.choice(products)
        product = ProductSerializer(product_object)
        
        quantity = random.randint(1, 10)  # Количество от 1 до 10
        price_per_unit = product_object.price
        items.append({
            "product": product.data,
            "quantity": quantity,
            "price_per_unit": float(price_per_unit),
        })
        total_amount += price_per_unit * quantity
    
    time = timezone.now() + datetime.timedelta(days=random.randint(1, 30)) + datetime.timedelta(hours=random.randint(1, 12))
    
    (hasDiscount, discount) = is_during_discount(time, Discount.objects.all())  
    new_client = Client()
    new_client.name = client_name
    client = ClientSerializer(new_client)

    receipt_json = {
        "cashier": cashier.data,
        "store": store.data,
        "total_amount": float(total_amount),
        "discount": DiscountSerializer(discount).data if hasDiscount else None,
        "timestamp": time,
        "items": items,
        "client": client.data,
    }

    return receipt_json

#generates receipts_num fake receipts
#output: json with array field receipts:[receipt1, receipt2, ...]
def generate_receipts_dump():
    receipts_num = random.randint(1, 300)
    return [generate_mock_receipt() for _ in range(receipts_num)]


#Check for every discount, if receipt date corresponds to at least one returns true and the discount
def is_during_discount(receipt_date, discounts):
    for discount in discounts:
        if discount.discount_start <= receipt_date <= discount.discount_end:
            return (True, discount)
    return (False, None)
    
    

    


