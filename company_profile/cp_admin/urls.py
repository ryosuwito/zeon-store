from django.urls import path, re_path
from .views import Login, Index, CmsArticle, Logout, CmsPage

app_name = 'cms'

urlpatterns = [
    path('article/<str:action>/<int:pk>/', CmsArticle.as_view(), name='article_edit_delete'),
    path('article/<str:action>/', CmsArticle.as_view(), name='article_add'),
    path('article/', CmsArticle.as_view(), name='article_all'),
    path('page/<str:action>/<int:pk>/', CmsPage.as_view(), name='page_edit_delete'),
    path('page/<str:action>/', CmsPage.as_view(), name='page_add'),
    path('page/', CmsPage.as_view(), name='page_all'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', Index.as_view(), name='index'),
]