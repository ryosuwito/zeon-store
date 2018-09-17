from django.urls import path, re_path
from .views import Login, Index, CmsArticle, Logout, CmsPage, CmsCategory, CmsAsset, CmsIdentity, CmsTemplate, CmsColor

app_name = 'cms'

urlpatterns = [
    path('article/<str:action>/<int:pk>/', CmsArticle.as_view(), name='article_edit_delete'),
    path('article/<str:action>/', CmsArticle.as_view(), name='article_add'),
    path('article/', CmsArticle.as_view(), name='article_all'),
    path('category/<str:action>/<int:pk>/', CmsCategory.as_view(), name='category_edit_delete'),
    path('category/<str:action>/', CmsCategory.as_view(), name='category_add'),
    path('category/', CmsCategory.as_view(), name='category_all'),
    path('page/<str:action>/<int:pk>/', CmsPage.as_view(), name='page_edit_delete'),
    path('page/<str:action>/', CmsPage.as_view(), name='page_add'),
    path('page/', CmsPage.as_view(), name='page_all'),
    path('asset/<str:action>/<int:pk>/', CmsAsset.as_view(), name='asset_edit'),
    path('asset/', CmsAsset.as_view(), name='asset_all'),
    path('identity/<str:action>/<int:pk>/', CmsIdentity.as_view(), name='identity_edit'),
    path('identity/', CmsIdentity.as_view(), name='identity_all'),
    path('template/<str:action>/<int:pk>/', CmsTemplate.as_view(), name='template_edit'),
    path('template/', CmsTemplate.as_view(), name='template_all'),
    path('color/<str:action>/<int:pk>/', CmsColor.as_view(), name='color_edit'),
    path('color/', CmsColor.as_view(), name='color_all'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('', Index.as_view(), name='index'),
]