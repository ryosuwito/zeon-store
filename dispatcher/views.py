from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.forms.models import model_to_dict

from company_profile.cp_pages.models import PageModel
from company_profile.cp_articles.models import Article as ArticleModel
from company_profile.cp_articles.models import Category as CategoryModel
from company_profile.cp_articles.models import TempArticle as TempArticleModel
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
        if get_current_site(request).domain == 'sidomo.com':
           return render(request, "zeon_backend/templates/index-3.html")
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
        article = ArticleModel.objects.all()
        data = super(Blog, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        if site.domain == 'sidomo.com':
            template = "zeon_backend/templates/blog_index.html"
        else:
            self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
            self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
            template = "company_profile/%s/blog-index.html"%(configs.templates.dir_name)

        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        return render(request, template, {
            'article': article,
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
        if kwargs['kategori'] != 'preview':
            try:
                category = CategoryModel.objects.get(site=site, slug=kwargs['kategori'])
                article = ArticleModel.objects.get(site=site, slug=kwargs['slug'])
            except:
                return HttpResponse("Not Found")
        else:
            category = 'preview'
            try:
                article = TempArticleModel.objects.get(site=site, slug=kwargs['slug'])
            except:
                return HttpResponse("Not Found")

        if site.domain == 'sidomo.com':
            template = "zeon_backend/templates/blog-post.html"
            comment = Comment()
            comment_and_reply = comment.get_comment_and_reply(article)
            return render(request, template, {'article': article, 'comments':comment_and_reply})

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
        if site.domain == 'sidomo.com':
            if kwargs['page_slug'] == 'contact':
                return render(request, "zeon_backend/templates/contact.html")
            elif kwargs['page_slug'] == 'about':
                return render(request, "zeon_backend/templates/about.html")
            elif kwargs['page_slug'] == 'services':
                return render(request, "zeon_backend/templates/services.html")
            elif kwargs['page_slug'] == 'pricing':
                return render(request, "zeon_backend/templates/pricing-tables.html")
            else:
                return render(request, "zeon_backend/templates/index-3.html")
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


class Comment(Dispatcher):
    def get(self, request, *args, **kwargs):
        data = super(Comment, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        try:
            method = kwargs['method']
        except:
            method = ''
        
        if method == 'add':
            return HttpResponse('Wrong Method', status=403)
        try:
            article = ArticleModel.objects.get(site=site, slug=kwargs['article_slug'])
        except:
            return HttpResponse('Article Not Found', status=404)

        if article.article_comment.all():
            return JsonResponse(self.get_comment_and_reply(article), safe=False)
        return HttpResponse('Not Found' , status=404)

    def get_comment_and_reply(self, article):
        return [self.format_comment(comment) for comment in article.article_comment.all()]

    def format_comment(self, comment):
        return {
            'created_date' : comment.created_date.strftime("%d/%B/%Y %H:%m"),
            'visitor': comment.visitor.name, 
            'content': comment.content,
            'reply' : self.format_replies(comment),
        }
        
    def format_replies(self, comment):
        if comment.comment_reply.all():
            return [self.format_reply(reply) for reply in  comment.comment_reply.all()]
        else:
            return ''
    
    def format_reply(self, reply):
        return {
            'created_date' : reply.created_date.strftime("%d/%B/%Y %H:%m"),
            'visitor': reply.visitor.name, 
            'content': reply.content,
        }