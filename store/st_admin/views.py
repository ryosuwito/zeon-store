from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from dispatcher.views import Dispatcher
from dispatcher.views import ComponentRenderer
from django.shortcuts import render
from django.views import View

from store.st_catalog.views import STProduct, STCategory
from store.st_purchase_order.views import STOrder
from store.st_customer.views import STCustomer
from store.st_shipping_backend.views import STShipping

class Index(LoginRequiredMixin, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base']='st_admin/component/index_base.html'
    def get(self, request, *args, **kwargs):
        token = get_token(request)
        data = super(Index, self).get(request, args, kwargs)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        self.component['header'] =  'st_admin/component/index_header.html'
        self.component['main'] = 'st_admin/component/index_main.html'
        self.component['local_script'] = 'st_admin/component/index_local_script.html'
        if(request.GET.get('method', '') == 'get_component'):
            return self.get_component(request, token, data, configs, site, member)

        return render(request, self.template, {
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component
            }
        )

    def post(self, request, *args, **kwargs):
        pass

    def get_component(self, request, token, data, configs, site, member):
        header =  render_to_string(self.component['header'], 
                                    {'token': token, 'member': member,'data': data, 'site': site, 'configs': configs})
        main = render_to_string(self.component['main'], 
                                    {'token': token, 'member': member,'data': data, 'site': site, 'configs': configs})
        local_script = render_to_string(self.component['local_script'], 
                                    {'token': token, 'member': member,'data': data, 'site': site, 'configs': configs})

        return JsonResponse({'main': main,
                            'local_script': local_script,
                            'header': header}, status=200)

class StoreProduct(STProduct):
    def get(self, request, *args, **kwargs):
        try:
            action = kwargs['action']
        except:
            action = 'show_all'
        
        try:
            pk = kwargs['pk']
        except:
            pk = 'none'

        return super(StoreProduct, self).get(request, args, action=action, pk=pk)

class StoreCategory(STCategory):
    def get(self, request, *args, **kwargs):
        try:
            action = kwargs['action']
        except:
            action = 'show_all'
        
        try:
            pk = kwargs['pk']
        except:
            pk = 'none'

        return super(StoreCategory, self).get(request, args, action=action, pk=pk)

class StoreOrder(STOrder):
    def get(self, request, *args, **kwargs):
        try:
            action = kwargs['action']
        except:
            action = 'show_all'
        
        try:
            pk = kwargs['pk']
        except:
            pk = 'none'

        return super(StoreOrder, self).get(request, args, action=action, pk=pk)

class StoreCustomer(STCustomer):
    def get(self, request, *args, **kwargs):
        try:
            action = kwargs['action']
        except:
            action = 'show_all'
        
        try:
            pk = kwargs['pk']
        except:
            pk = 'none'

        return super(StoreCustomer, self).get(request, args, action=action, pk=pk)

class StoreShipping(STShipping):
    def get(self, request, *args, **kwargs):
        try:
            action = kwargs['action']
        except:
            action = 'show_all'
        
        try:
            pk = kwargs['pk']
        except:
            pk = 'none'

        return super(StoreShipping, self).get(request, args, action=action, pk=pk)
