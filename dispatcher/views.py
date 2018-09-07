from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from company_profile.cp_pages.models import PageModel
from company_profile.cp_articles.models import Article as ArticleModel
from company_profile.cp_articles.models import Category as CategoryModel
from company_profile.cp_user_configs.models import UserConfigs
from membership.models import Member

class Dispatcher(View):
    component = {}
    def get(self, request, *args, **kwargs):
        site = get_current_site(request)
        member = Member.objects.get(site=site)
        return {'member':member, 'site':site}
    def post(self, request, *args, **kwargs):
        pass
    def set_default_configs(configs):
        pass

class Index(Dispatcher):
    def get(self, request, *args, **kwargs):
        #if get_current_site(request).domain == 'sidomo.com':
        #   return render(request, "zeon_backend/templates/index-3.html")
        data = super(Index, self).get(request, args, kwargs)
        configs, is_created = UserConfigs.objects.get_or_create(member = data['member'])
        if is_created:
            super(Index, self).set_default_configs(configs)
        site = data['site']
        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
        self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
        template = "company_profile/%s/index.html"%(configs.templates.dir_name)
        return render(request, template, {
            'component': self.component,
            'configs':configs,
            'site':site,
            'assets': assets,
            'scheme': scheme,
            'identity': identity,
        })


class Blog(Dispatcher):
    def get(self, request, *args, **kwargs):
        data = super(Blog, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
        self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
        template = "company_profile/%s/blog-index.html"%(configs.templates.dir_name)
        return render(request, template, {
            'component': self.component,
            'configs':configs,
            'site':site,
            'assets': assets,
            'scheme': scheme,
            'identity': identity,
        })
    def post(self, request, *args, **kwargs):
        pass

class Article(Dispatcher):
    def get(self, request, *args, **kwargs):
        data = super(Article, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        try:
            category = CategoryModel.objects.get(site=site, slug=kwargs['kategori'])
            article = ArticleModel.objects.filter(site=site, slug=kwargs['slug'], category=category)
        except:
            return HttpResponse("Not Found")

        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
        self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
        template = "company_profile/%s/article-detail.html"%(configs.templates.dir_name)
        return render(request, template, {
            'component': self.component,
            'configs':configs,
            'site':site,
            'assets': assets,
            'scheme': scheme,
            'identity': identity,
        })

class Page(Dispatcher):
    def get(self, request, *args, **kwargs):
        data = super(Page, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
        self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
        page = PageModel.objects.get(slug=kwargs['page_slug'])
        template = "company_profile/%s/page.html"%(configs.templates.dir_name)
        return render(request, template, {
            'component': self.component,
            'configs':configs,
            'site':site,
            'page':page,
            'assets': assets,
            'scheme': scheme,
            'identity': identity,
        })
    def post(self, request, *args, **kwargs):
        pass