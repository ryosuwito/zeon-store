from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import PageAddForm

import time
from company_profile.cp_user_configs.models import UserConfigs
from company_profile.cp_articles.views import CPArticle

class CPPage(CPArticle):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_admin/component/cms_page_main.html'
    index_local_script = 'cp_admin/component/cms_page_local_script.html'
    add_main = 'cp_admin/component/cmspagee_add_main.html'
    add_local_script = 'cp_admin/component/cms_page_add_local_script.html'
    edit_main = 'cp_admin/component/cms_page_edit_main.html'
    edit_local_script = 'cp_admin/component/cms_page_edit_local_script.html'
    delete_main = 'cp_admin/component/cms_page_delete_main.html'
    delete_local_script = 'cp_admin/component/cms_page_delete_local_script.html'
    index_url = '/cms/page/'
    form = PageAddForm()

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        pk = kwargs['pk']
        return super(CPPage, self).get(request, args, action=action, pk=pk)