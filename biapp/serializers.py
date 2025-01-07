from rest_framework import serializers
from biapp.models import Receipt, ReceiptItem, Cashier, Store, Client, Discount, Product

class StoreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Store
        fields = ['id', 'location']
        
class DiscountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Discount
        fields = ['id', 'discount_name', 'discount_type', 'discount_value', 'discount_start', 'discount_end']
        
class ClientSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField(required=False)
    class Meta:
        model = Client
        fields = ['id', 'name']
        
class CashierSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Cashier
        fields = ['id', 'name']
        
class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        
class ReceiptItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product = ProductSerializer()
    
    def create(self, validated_data):
        product_data = validated_data.pop("product")
        product = Product.objects.get(id=product_data['id'])
        return ReceiptItem.objects.create(product=product, **validated_data)
    class Meta:
        model = ReceiptItem
        fields = ['id', 'product', 'quantity', 'price_per_unit']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation
        
class ReceiptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    cashier = CashierSerializer()
    client = ClientSerializer()
    store = StoreSerializer()
    discount = DiscountSerializer(allow_null=True)
    items = ReceiptItemSerializer(many=True)
    
    def create(self, validated_data):
        items_data = validated_data.pop("items")
        cashier_data = validated_data.pop("cashier")
        cashier = Cashier.objects.get(id=cashier_data['id'])
        
        client_data = validated_data.pop("client")
        client, _ = Client.objects.get_or_create(**client_data)
        
        store_data = validated_data.pop("store")
        store = Store.objects.get(id=store_data['id'])
        
        discount_data = validated_data.pop("discount")
        if (discount_data):
            discount = Discount.objects.get(id=discount_data['id'])
        else:
            discount = None
        receipt = Receipt.objects.create(cashier=cashier, client=client, store=store, discount=discount, **validated_data)
        
        for item_data in items_data:
            product_data = item_data.pop('product')  
            product = Product.objects.get(id=product_data['id']) 
            ReceiptItem.objects.create(receipt=receipt, product=product, **item_data)        
        return receipt
    class Meta:
        model = Receipt
        fields = [
            'id', 'cashier', 'client', 'store', 
            'total_amount', 'discount', 'timestamp', 'items'
        ]
    