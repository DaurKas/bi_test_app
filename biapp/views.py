from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from biapp.models import Receipt, ReceiptItem, Cashier, Store, Client, Discount, Product
from biapp.serializers import ReceiptSerializer, DiscountSerializer
import pandas as pd

class DiscountSearchView(APIView):
    def get(self, request):
        discount_name = request.query_params.get('name', None)
        search_date = request.query_params.get('date', None)
        
        filters = Q()
        if discount_name:
            filters &= Q(discount_name__icontains=discount_name)
        if search_date:
            filters &= Q(discount_start__lte=search_date, discount_end__gte=search_date)
        
        discounts = Discount.objects.filter(filters)
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReceiptSearchView(APIView):
    def get(self, request, pk):
        try:
            receipt = Receipt.objects.get(pk=pk)
        except Receipt.DoesNotExist:
            return HttpResponse(status=404)

        if request.method == 'GET':
            serializer = ReceiptSerializer(receipt)
            return Response(serializer.data, status=status.HTTP_200_OK)


def get_dashboard_data():
    receipts = pd.DataFrame.from_records(
        Receipt.objects.values('id', 'timestamp', 'total_amount', 'store', 'cashier')
    )
    receipts['timestamp'] = pd.to_datetime(receipts['timestamp'])
    sales_by_day = receipts.groupby(receipts['timestamp'].dt.date).sum('total_amount').reset_index()
    sales_by_store = receipts.groupby('store').sum('total_amount').reset_index()

    items = pd.DataFrame.from_records(
        ReceiptItem.objects.values('product', 'quantity')
    ).groupby('product').sum('quantity').reset_index()

    products = pd.DataFrame.from_records(
        Product.objects.values('id', 'name')
    ).rename(columns={'id': 'product'})

    top_products = items.merge(products, on='product').sort_values('quantity', ascending=False).head(10)
    receipts_by_cashier = receipts.groupby('cashier').size().reset_index(name='num_receipts')
    
    return sales_by_day, sales_by_store, top_products, receipts_by_cashier

def receipt_list(request):
    """
    List all receipts
    """
    if request.method == 'GET':
        receipts = Receipt.objects.all()
        serializer = ReceiptSerializer(receipts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
def receipt_detail(request, pk):
    """
    Retrieve receipt
    """
    try:
        receipt = Receipt.objects.get(pk=pk)
    except Receipt.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ReceiptSerializer(receipt)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
def sales_dashboard(request):
    return render(request, 'biapp/sales_dashboard.html')
