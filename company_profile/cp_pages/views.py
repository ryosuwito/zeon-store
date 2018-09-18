from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.urls import reverse
from django.template.loader import render_to_string
from .forms import PageAddForm
from .models import PageModel

import time
from company_profile.cp_user_configs.models import UserConfigs
from company_profile.cp_articles.views import CPArticle
from dispatcher.views import ComponentRenderer
from dispatcher.views import Dispatcher

class CPPage(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_pages/component/cms_page_main.html'
    index_local_script = 'cp_pages/component/cms_page_local_script.html'
    add_main = 'cp_pages/component/cms_page_add_main.html'
    add_local_script = 'cp_pages/component/cms_page_add_local_script.html'
    edit_main = 'cp_pages/component/cms_page_edit_main.html'
    edit_local_script = 'cp_pages/component/cms_page_edit_local_script.html'
    index_url = '/cms/page/'
    form = PageAddForm()

    def get(self, request, *args, **kwargs):
        if  kwargs['action'] == 'delete' or kwargs['action'] == 'edit':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    page = PageModel.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)
        method = request.GET.get('method', '')
        data = super(CPPage, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form
        if  kwargs['action'] == 'edit':
            form = PageAddForm(instance=page)
        elif  kwargs['action'] == 'delete':
            page.delete()
            return HttpResponseRedirect(reverse('cms:page_all'))

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'edit' or \
            kwargs['action'] == 'delete' :
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)

        if method == 'get_component':
            featured_image = ""
            return self.get_component(request, token, data, configs, site, member, form, featured_image)
                                     
        return render(request, self.template, {
                'form': form,
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component,
                'page' : page,
            }
        )