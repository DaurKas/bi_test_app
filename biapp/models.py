from django.db import models

# Create your models here.
class Receipt(models.Model):
    cashier = models.ForeignKey('Cashier', on_delete=models.CASCADE, related_name='receipts')
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='receipts')
    total_amount = models.DecimalField(max_digits=12, decimal_places=3)
    discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True, related_name='receipts')
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Receipt {self.id} - Total: {self.total_amount}"

class ReceiptItem(models.Model):
    receipt = models.ForeignKey('Receipt', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='receipt_items')
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=12, decimal_places=3)

    def __str__(self):
        return f"Item {self.product.name} (x{self.quantity}) in Receipt {self.receipt.id}"
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Cashier(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Client(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Store(models.Model):
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.location
    
    
class Discount(models.Model):
    TYPE_CHOICES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    discount_name = models.CharField(max_length=255, null=True, blank=True)
    discount_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    discount_start = models.DateTimeField(null=True)
    discount_end = models.DateTimeField(null=True)
    def __str__(self):
        return f"Discount {self.discount_name} - {self.discount_value}"