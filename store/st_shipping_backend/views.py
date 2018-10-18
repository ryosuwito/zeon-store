from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from dispatcher.views import Dispatcher
from dispatcher.views import ComponentRenderer

from company_profile.cp_user_configs.models import UserConfigs

from .models import ShippingOrigin
from .forms import ShippingAddForm

class STShipping(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'st_shipping_backend/component/shipping_main.html'
    index_local_script = 'st_shipping_backend/component/shipping_local_script.html'
    add_main = 'st_shipping_backend/component/shipping_add_main.html'
    add_local_script = 'st_shipping_backend/component/shipping_add_local_script.html'
    edit_main = 'st_shipping_backend/component/shipping_edit_main.html'
    edit_local_script = 'st_shipping_backend/component/shipping_edit_local_script.html'
    index_url = '/cms/shipping/'
    form = ShippingAddForm()

    def get(self, request, *args, **kwargs):
        origin = ""
        if  kwargs['action'] == 'delete' or kwargs['action'] == 'edit':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    origin = ShippingOrigin.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)

        method = request.GET.get('method', '')
        data = super(STShipping, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form
        featured_image = ''
        if  kwargs['action'] == 'edit':
            form = ShippingAddForm(instance=origin)
        elif  kwargs['action'] == 'delete':
            origin.delete()
            return HttpResponseRedirect(self.index_url)

        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'edit':
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)


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
