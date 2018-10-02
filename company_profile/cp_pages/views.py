from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from .forms import PageAddForm, PagePreviewForm
from .models import PageModel, TempPageModel

import time
from urllib.parse import urlparse

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

    def post(self, request, *args, **kwargs):
        data = super(CPPage, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']

        if  kwargs['action'] == 'edit':
            page = PageModel.objects.get(pk=kwargs['pk'])
            self.form = PageAddForm(request.POST, request.FILES, instance=page)
            if self.form.is_valid():
                return HttpResponseRedirect(self.index_url)
        elif  kwargs['action'] == 'preview':
            self.form = PagePreviewForm(request.POST, request.FILES)
        else:
            self.form = PageAddForm(request.POST, request.FILES)

        
        if self.form.is_valid():
            page = self.form.save(commit=False)
            page.site = site
            page.save()
            self.form.save_m2m()

            if kwargs['action'] == 'preview':
                referer = request.META['HTTP_REFERER']
                if '/cms/page/edit' in referer:
                    parse_object = urlparse(referer)
                    url_splitted = parse_object.path.split("/")
                    try:
                        old_page = PageModel.objects.get(pk = url_splitted[-2])
                    except:
                        old_page = ''

                    if old_page and not page.banner_image_1:
                        page.banner_image_1 = old_page.banner_image_1
                    if old_page and not page.banner_image_2:
                        page.banner_image_2 = old_page.banner_image_2
                    if old_page and not page.banner_image_3:
                        page.banner_image_3 = old_page.banner_image_3
                        
                    page.class_name='TempPage'
                    page.save()
                    return JsonResponse({'url': page.get_page_url()+'?method=preview'}, status=200)

            return HttpResponseRedirect(self.index_url)

        token = get_token(request)
        configs = UserConfigs.objects.get(member = member)
        return render(request, self.template, {
                'form': self.form,
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component
            }
        )
    def get(self, request, *args, **kwargs):
        page = ""
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
        featured_image = ''
        if  kwargs['action'] == 'edit':
            form = PageAddForm(instance=page)

            featured_image = {
                'banner_image_1' : page.banner_image_1,
                'banner_image_2' : page.banner_image_2,
                'banner_image_3' : page.banner_image_3,
            }

        elif  kwargs['action'] == 'delete':
            page.delete()
            return HttpResponseRedirect(self.index_url)

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'edit' or \
            kwargs['action'] == 'delete' :
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)

        if method == 'get_component':
            return self.get_component(request, token, data, configs, site, member, form, featured_image)
                                     
        return render(request, self.template, {
                'form': form,
                'featured_image': featured_image,
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component,
                'page' : page,
            }
        )