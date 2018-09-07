from __future__ import absolute_import

from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from django.urls import reverse
from ckeditor_uploader import views

urlpatterns = [
    re_path(r'^upload/', login_required(views.upload, login_url='/cms/login/'), name='ckeditor_upload'),
    re_path(r'^browse/', never_cache(login_required(views.browse, login_url='/cms/login/')), name='ckeditor_browse'),
]