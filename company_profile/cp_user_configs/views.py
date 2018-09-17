from django.shortcuts import render
from company_profile.cp_articles.views import CPArticle
from .form import AssetEditForm
        
class CPAsset(CPArticle):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_admin/component/cms_asset_main.html'
    index_local_script = 'cp_admin/component/cms_asset_local_script.html'
    edit_main = 'cp_admin/component/cms_asset_edit_main.html'
    edit_local_script = 'cp_admin/component/cms_asset_edit_local_script.html'
    index_url = '/cms/asset/'
    form = AssetEditForm()

    def get(self, request, *args, **kwargs):
        action = kwargs['action']
        pk = kwargs['pk']
        return super(CPAsset, self).get(request, args, action=action, pk=pk)
