from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from dispatcher.views import Dispatcher
from dispatcher.views import ComponentRenderer

from company_profile.cp_user_configs.models import UserConfigs

from .models import Customer
from .forms import CustomerAddForm


class STCustomer(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'st_customer/component/customer_main.html'
    index_local_script = 'st_customer/component/customer_local_script.html'
    add_main = 'st_customer/component/customer_add_main.html'
    add_local_script = 'st_customer/component/customer_add_local_script.html'
    edit_main = 'st_customer/component/customer_edit_main.html'
    edit_local_script = 'st_customer/component/customer_edit_local_script.html'
    index_url = '/cms/customer/'
    form = CustomerAddForm()

    def post(self, request, *args, **kwargs):
        data = super(STCustomer, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']
        if  kwargs['action'] == 'edit':
            customer = Customer.objects.get(pk=kwargs['pk'])
            self.form = CustomerAddForm(request.POST, request.FILES, instance=customer)
            if self.form.is_valid():
                customer = self.form.save()
                return HttpResponseRedirect(self.index_url)
        else:
            self.form = CustomerAddForm(request.POST, request.FILES)

        if self.form.is_valid():
            customer = self.form.save(commit=False)
            customer.site = site
            customer.member = member
            customer.save()

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
        customer = ""
        if  kwargs['action'] == 'delete':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    customer = Customer.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)

        method = request.GET.get('method', '')
        data = super(STCustomer, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form
        featured_image = ''        
        if  kwargs['action'] == 'edit':
            try:
                customer = Customer.objects.get(pk=kwargs['pk'])
            except:
                return HttpResponseRedirect(self.index_url)
            form = CustomerAddForm(instance=category)

        elif  kwargs['action'] == 'delete':
            return HttpResponseRedirect(self.index_url)

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
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
            }
        )