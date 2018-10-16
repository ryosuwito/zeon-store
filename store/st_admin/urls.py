from django.urls import path, re_path
from .views import Index, StoreProduct, StoreCategory, StoreOrder, StoreCustomer, StoreShipping
app_name = 'store'

urlpatterns = [
    path('product/<str:action>/<int:pk>/', StoreProduct.as_view(), name='product_edit_delete'),
    path('product/<str:action>/', StoreProduct.as_view(), name='product_add'),
    path('product/', StoreProduct.as_view(), name='product_all'),

    path('category/<str:action>/<int:pk>/', StoreCategory.as_view(), name='category_edit_delete'),
    path('category/<str:action>/', StoreCategory.as_view(), name='category_add'),
    path('category/', StoreCategory.as_view(), name='category_all'),

    path('order/<str:action>/<int:pk>/', StoreCategory.as_view(), name='order_edit_delete'),
    path('order/<str:action>/', StoreCategory.as_view(), name='order_add'),
    path('order/', StoreCategory.as_view(), name='order_all'),

    path('customer/<str:action>/<int:pk>/', StoreCustomer.as_view(), name='customer_edit_delete'),
    path('customer/<str:action>/', StoreCustomer.as_view(), name='customer_add'),
    path('customer/', StoreCustomer.as_view(), name='customer_all'),

    path('shipping/<str:action>/<int:pk>/', StoreShipping.as_view(), name='shipping_edit_delete'),
    path('shipping/<str:action>/', StoreShipping.as_view(), name='shipping_add'),
    path('shipping/', StoreShipping.as_view(), name='shipping_all'),

    path('', Index.as_view(), name='index'),
]