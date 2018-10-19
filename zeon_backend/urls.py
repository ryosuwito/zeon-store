"""zeon_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from dispatcher.views import Index, Blog, Article, Page, Comment, ArticleList, Reply
from django.conf import settings
from django.conf.urls.static import static
from company_profile.cp_admin import urls as cp_admin
from store.st_admin import urls as st_admin

import company_profile.cp_admin.ckeditor_uploader.urls as ckeditor_uploader_urls
import store.st_storefront.urls as storefront
import store.st_database_wilayah.urls as wilayah
import store.st_shopping_cart.urls as cart
import store.st_purchase_order.urls as order
#import shipping_backend.urls as shipping

from store.st_purchase_order.views import checkout, pay, history

urlpatterns = [
    path('wilayah/', include(wilayah, namespace='wilayah_backend')),
    path('cart/', include(cart, namespace='cart_backend')),
    path('checkout/', checkout, name="checkout"),
    path('pay/', pay, name="pay"),
    path('history/', history, name="history"),
    path('order/', include(order, namespace='order_backend')),
    #path('shipping/', include(shipping, namespace='shipping_backend')),
    path('str/', include(st_admin, namespace='st_admin')),
    path('cms/', include(cp_admin, namespace='cp_admin')),
    path('core/admin/', admin.site.urls),
    path('blog/<str:kategori>/<str:slug>/', Article.as_view(), name="blog_detail"),
    path('comment/<str:article_slug>/<str:method>/', Comment.as_view(), name="add_comment"),
    path('comment/<str:article_slug>/', Comment.as_view(), name="view_all_comment"),
    path('reply/<str:article_slug>/<int:comment_pk>/<str:method>/', Reply.as_view(), name="add_reply"),
    re_path(r'^$', Index.as_view()), 
    re_path(r'^blog/$', Blog.as_view(), name="blog_index"),
    re_path(r'^ckeditor/', include(ckeditor_uploader_urls)),
    re_path(r'^store/', include(storefront, namespace='store_backend')),
    re_path(r'^taggit/', include('taggit_selectize.urls')),
    path('<str:page_slug>/', Page.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
