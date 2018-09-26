from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware.csrf import get_token

from company_profile.cp_articles.views import CPArticle
from company_profile.cp_configs.models import BrandAsset, BrandIdentity, ColorScheme, Template

from dispatcher.views import ComponentRenderer
from dispatcher.views import Dispatcher

from .models import UserConfigs
from .forms import AssetEditForm, TemplateEditForm, ColorEditForm, IdentityEditForm

from urllib.parse import urlparse


class CPAsset(LoginRequiredMixin, ComponentRenderer, Dispatcher):
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

    def post(self, request, *args, **kwargs):
        data = super(CPAsset, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']

        if  kwargs['action'] == 'edit':
            asset = BrandAsset.objects.get(pk=kwargs['pk'])
            self.form = AssetEditForm(request.POST, request.FILES, instance=asset)

        if self.form.is_valid():
            asset = self.form.save(commit=False)
            referer = request.META['HTTP_REFERER']
            if '/cms/asset/edit' in referer:
                parse_object = urlparse(referer)
                url_splitted = parse_object.path.split("/")
                try:
                    old_asset = BrandAsset.objects.get(pk = url_splitted[-2])
                except:
                    old_asset = ''

                if old_asset and not asset.favicon:
                    asset.favicon = old_asset.favicon

                if old_asset and not asset.hero_image_1:
                    asset.hero_image_1 = old_asset.hero_image_1

                if old_asset and not asset.hero_image_2:
                    asset.hero_image_2 = old_asset.hero_image_2

                if old_asset and not asset.hero_image_3:
                    asset.hero_image_3 = old_asset.hero_image_3

                if old_asset and not asset.brand_logo:
                    asset.brand_logo = old_asset.brand_logo

                if old_asset and not asset.main_photo_1:
                    asset.main_photo_1 = old_asset.main_photo_1
                    
                if old_asset and not asset.main_photo_2:
                    asset.main_photo_2 = old_asset.main_photo_2

                if old_asset and not asset.extra_image_1:
                    asset.extra_image_1 = old_asset.extra_image_1

                if old_asset and not asset.extra_image_2:
                    asset.extra_image_2 = old_asset.extra_image_2

                if old_asset and not asset.extra_image_3:
                    asset.extra_image_3 = old_asset.extra_image_3

                asset.save()
                
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
                'asset' : asset,
                'component':self.component
            }
        )


    def get(self, request, *args, **kwargs):
        asset = ""
        if  kwargs['action'] == 'delete' or kwargs['action'] == 'edit':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    asset = BrandAsset.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)

        method = request.GET.get('method', '')
        data = super(CPAsset, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form

        featured_image = ''
        if  kwargs['action'] == 'edit':
            form = AssetEditForm(instance=asset)

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'edit' :
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
                'asset' : asset,
            }
        )
        

class CPIdentity(LoginRequiredMixin, ComponentRenderer, Dispatcher):
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
    form = IdentityEditForm()

    def get(self, request, *args, **kwargs):
        identity = ""
        if  kwargs['action'] == 'delete' or kwargs['action'] == 'edit':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    identity = BrandIdentity.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)

        method = request.GET.get('method', '')
        data = super(CPIdentity, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form

        featured_image = ''
        if  kwargs['action'] == 'edit':
            form = IdentityEditForm(instance=identity)

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'edit' :
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
                'identity' : identity,
            }
        )

class CPTemplate(LoginRequiredMixin, ComponentRenderer, Dispatcher):
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

class CPColor(LoginRequiredMixin, ComponentRenderer, Dispatcher):
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


