from django.urls import path
from biapp import views
from biapp import dash_sales

urlpatterns = [
    path('biapp/raw/', views.receipt_list),
    path('api/v1/receipt/search/<int:pk>/', views.ReceiptSearchView.as_view()),
    path('api/v1/receipt/discount/search/', views.DiscountSearchView.as_view()),
    path('', views.sales_dashboard)
]