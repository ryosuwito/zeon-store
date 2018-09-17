from django.shortcuts import render
from company_profile.cp_articles.views import CPArticle
from .forms import AssetEditForm, TemplateEditForm, ColorEditForm
        
class CPAsset(CPArticle):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_user_configs/component/asset/main.html'
    index_local_script = 'cp_user_configs/component/asset/local_script.html'
    edit_main = 'cp_user_configs/component/asset/edit_main.html'
    edit_local_script = 'cp_user_configs/component/asset/edit_local_script.html'
    index_url = '/cms/asset/'
    form = AssetEditForm()

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        pk = kwargs['pk']
        return super(CPAsset, self).get(request, args, action=action, pk=pk)

class CPIdentity(CPArticle):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_user_configs/component/identity/main.html'
    index_local_script = 'cp_user_configs/component/identity/local_script.html'
    edit_main = 'cp_user_configs/component/identity/edit_main.html'
    edit_local_script = 'cp_user_configs/component/identity/edit_local_script.html'
    index_url = '/cms/asset/'
    form = AssetEditForm()

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        pk = kwargs['pk']
        return super(CPIdentity, self).get(request, args, action=action, pk=pk)

class CPTemplate(CPArticle):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_user_configs/component/template/main.html'
    index_local_script = 'cp_user_configs/component/template/local_script.html'
    edit_main = 'cp_user_configs/component/template/edit_main.html'
    edit_local_script = 'cp_user_configs/component/template/edit_local_script.html'
    index_url = '/cms/'
    form = TemplateEditForm()

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        pk = kwargs['pk']
        return super(CPTemplate, self).get(request, args, action=action, pk=pk)

class CPColor(CPArticle):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    edit_main = 'cp_user_configs/component/color/edit_main.html'
    edit_local_script = 'cp_user_configs/component/color/edit_local_script.html'
    index_url = '/cms/'
    form = ColorEditForm()

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        pk = kwargs['pk']
        return super(CPColor, self).get(request, args, action=action, pk=pk)


