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
from dispatcher.views import Index, Blog, Article, Page, Comment
from django.conf import settings
from django.conf.urls.static import static
from company_profile.cp_admin import urls as cp_admin
import company_profile.cp_admin.ckeditor_uploader.urls as ckeditor_uploader_urls

urlpatterns = [
    re_path(r'^taggit/', include('taggit_selectize.urls')),
    path('cms/', include(cp_admin, namespace='cp_admin')),
    re_path(r'^ckeditor/', include(ckeditor_uploader_urls)),
    path('core/admin/', admin.site.urls),
    re_path(r'^$', Index.as_view()), 
    re_path(r'^blog/$', Blog.as_view(), name="blog_index"),
    path('blog/<str:kategori>/<str:slug>/', Article.as_view(), name="blog_detail"),
    path('comment/<str:article_slug>/<str:method>/', Comment.as_view(), name="add_comment"),
    path('comment/<str:article_slug>/', Comment.as_view(), name="view_all_comment"),
    path('<str:page_slug>/', Page.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
