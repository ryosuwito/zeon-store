from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'storefront'
 
urlpatterns = [
    path('detail/<int:product_pk>/<str:referal_code>/', views.product_detail, name='product_detail_with_ref_code'),
    path('detail/<int:product_pk>/', views.product_detail, name='product_detail'),
    re_path(r'detail/$', RedirectView.as_view(url='/store/')),
    path('kategori/<int:category_pk>/<str:referal_code>/', views.product_by_category, name='product_by_category_with_ref_code'),
    path('kategori/<int:category_pk>/', views.product_by_category, name='product_by_category'),
    re_path(r'kategori/$', RedirectView.as_view(url='/store/')),
    path('<str:referal_code>/', views.index, name='product_all_with_ref_code'),
    re_path(r'^$', views.index, name='product_all'),
]
