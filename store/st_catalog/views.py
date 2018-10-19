from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from dispatcher.views import Dispatcher
from dispatcher.views import ComponentRenderer

from company_profile.cp_user_configs.models import UserConfigs

from .models import Product, Category
from .forms import ProductAddForm, CategoryAddForm

class STProduct(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'st_catalog/component/product_main.html'
    index_local_script = 'st_catalog/component/product_local_script.html'
    add_main = 'st_catalog/component/product_add_main.html'
    add_local_script = 'st_catalog/component/product_add_local_script.html'
    edit_main = 'st_catalog/component/product_edit_main.html'
    edit_local_script = 'st_catalog/component/product_edit_local_script.html'
    index_url = '/str/product/'
    form = ProductAddForm()
    def post(self, request, *args, **kwargs):
        data = super(STProduct, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']
        if  kwargs['action'] == 'edit':
            product = Product.objects.get(pk=kwargs['pk'])
            self.form = ProductAddForm(request.POST, request.FILES, instance=product)
        else:
            self.form = ProductAddForm(request.POST, request.FILES)

        if self.form.is_valid():
            product = self.form.save(commit=False)
            product.site = site
            product.save()
            self.form.save_m2m()

            if kwargs['action'] != 'preview':
                if not product.categories.all() :
                    product.categories.add(Category.objects.get_or_create(site=site, name="default")[0])
                    product.save()

            return HttpResponseRedirect(self.index_url)

        self.form.fields["categories"].queryset = Category.objects.filter(site=site)
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
        if  kwargs['action'] == 'delete' or kwargs['action'] == 'edit':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    product = Product.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)
        data = super(STProduct, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form
        featured_image = ''

        if  kwargs['action'] == 'edit':
            form = ProductAddForm(instance=product)
        elif  kwargs['action'] == 'delete':
            product.delete()
            return HttpResponseRedirect(self.index_url)

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'edit' or \
            kwargs['action'] == 'delete' :
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)

        form.fields["categories"].queryset = Category.objects.filter(site=site)

        if method == 'get_component':
            return self.get_component(request, token, data, configs, site, member, form, featured_image)

        return render(request, self.template, {
                'form': form,
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component,
                'featured_image' : featured_image,
            }
        )

class STCategory(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'st_catalog/component/category_main.html'
    index_local_script = 'st_catalog/component/category_local_script.html'
    add_main = 'st_catalog/component/category_add_main.html'
    add_local_script = 'st_catalog/component/category_add_local_script.html'
    edit_main = 'st_catalog/component/category_edit_main.html'
    edit_local_script = 'st_catalog/component/category_edit_local_script.html'
    index_url = '/str/category/'
    form = CategoryAddForm()

    def post(self, request, *args, **kwargs):
        data = super(STCategory, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']
        if  kwargs['action'] == 'edit':
            category = Category.objects.get(pk=kwargs['pk'])
            self.form = CategoryAddForm(request.POST, request.FILES, instance=category)
            if self.form.is_valid():
                category = self.form.save()
                return HttpResponseRedirect(self.index_url)
        else:
            self.form = CategoryAddForm(request.POST, request.FILES)

        if self.form.is_valid():
            category = self.form.save(commit=False)
            category.site = site
            category.save()

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
        category = ""
        if  kwargs['action'] == 'delete':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    category = Category.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)
        if category.title == 'post':
            return HttpResponseRedirect(self.index_url)

        method = request.GET.get('method', '')
        data = super(STCategory, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form
        featured_image = ''
        if  kwargs['action'] == 'edit':
            try:
                category = Category.objects.get(pk=kwargs['pk'])
            except:
                return HttpResponseRedirect(self.index_url)
            form = CategoryAddForm(instance=category)

        elif  kwargs['action'] == 'delete':
            products = Product.objects.filter(categories=category)
            if products:
                for product in products:
                    try:
                        product.categories.remove(category)
                    except:
                        pass
            category.delete()
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
            }
        )


