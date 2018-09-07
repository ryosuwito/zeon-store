from django.shortcuts import render
from dispatcher.views import Dispatcher
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import ArticleAddForm

import time
from company_profile.cp_user_configs.models import UserConfigs

class CPArticle(LoginRequiredMixin, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_admin/component/cms_article_main.html'
    index_local_script = 'cp_admin/component/cms_article_local_script.html'
    add_main = 'cp_admin/component/cms_article_add_main.html'
    add_local_script = 'cp_admin/component/cms_article_add_local_script.html'
    edit_main = 'cp_admin/component/cms_article_edit_main.html'
    edit_local_script = 'cp_admin/component/cms_article_edit_local_script.html'
    delete_main = 'cp_admin/component/cms_article_delete_main.html'
    delete_local_script = 'cp_admin/component/cms_article_delete_local_script.html'
    index_url = '/cms/article/'
    form = ArticleAddForm()

    def get(self, request, *args, **kwargs):
        if  kwargs['action'] == 'delete' or kwargs['action'] == 'edit':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
        method = request.GET.get('method', 'none')
        data = super(CPArticle, self).get(request, args, kwargs)
        form = self.form
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'edit' or \
            kwargs['action'] == 'delete' :
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)
            
        if method == 'get_component':
            return self.get_component(request, token, data, configs, site, member, form)
                            
        return render(request, self.template, {
                'form': form,
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component
            }
        )

    def get_component(self, request, token, data, configs, site, member, form):
        main = render_to_string(self.component['main'], 
                                    {'form': form,'token': token, 'member': member,'data': data, 'site': site, 'configs': configs})
        local_script = render_to_string(self.component['local_script'], 
                                    {'token': token, 'member': member,'data': data, 'site': site, 'configs': configs})
        return JsonResponse({'main': main,
                        'local_script': local_script}, status=200)

    def set_component(self, kwargs):
        if kwargs['action'] == 'show_all':
            self.component['main'] = self.index_main
            self.component['local_script'] = self.index_local_script
        elif kwargs['action'] == 'add':
            self.component['main'] = self.add_main
            self.component['local_script'] = self.add_local_script
        elif kwargs['action'] == 'edit':
            self.component['main'] = self.edit_main
            self.component['local_script'] = self.edit_local_script
        elif kwargs['action'] == 'delete':
            self.component['main'] = self.delete_main
            self.component['local_script'] = self.delete_local_script
        



