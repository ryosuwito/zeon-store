from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.forms.models import model_to_dict
from django.urls import reverse
from django.template.loader import render_to_string

from company_profile.cp_pages.models import PageModel, TempPageModel
from company_profile.cp_articles.models import Article as ArticleModel
from company_profile.cp_articles.models import Category as CategoryModel
from company_profile.cp_articles.models import TempArticle as TempArticleModel
from company_profile.cp_user_configs.models import UserConfigs

from company_profile.cp_comment.forms import AddVisitorForm, AddCommentForm, AddReplyForm
from company_profile.cp_comment.models import Visitor as VisitorModel
from company_profile.cp_comment.models import Comment as CommentModel
from company_profile.cp_comment.models import Reply as ReplyModel
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
        data = super(Index, self).get(request, args, kwargs)
        configs, is_created = UserConfigs.objects.get_or_create(member = data['member'])
        if is_created:
            super(Index, self).set_default_configs(configs)
        site = data['site']
        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        if site.domain == 'sidomo.com':
           recent_articles = ArticleModel.objects.filter(site=site, is_published=True).order_by('-created_date')[:3]
           return render(request, 
                "zeon_backend/templates/index-3.html",
                {
                    'recent_article':recent_articles
                }
           )
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
        if site.domain == 'sidomo.com':
            template = "zeon_backend/templates/blog_index.html"
        else:
            self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
            self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
            template = "company_profile/%s/blog-index.html"%(configs.templates.dir_name)

        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        article_list = ArticleModel.objects.filter(site=site, is_published=True).order_by('-created_date')

        max_page = 4
        min_page = 0
        articles = ''
        if article_list and len(article_list) > 6:
            is_paginated = True
            try:
                paginator = Paginator(article_list,6)
                page = request.GET.get('page', 1)
                try:
                    articles = paginator.page(page)
                except PageNotAnInteger:
                    articles = paginator.page(1)
                except EmptyPage:
                    articles = paginator.page(paginator.num_pages)

                max_page = articles.number + 4
                min_page = articles.number - 4
            except:
                pass
        else:
            is_paginated = False
            articles = article_list
                
        recent_articles = articles[:3]
        return render(request, template, {
            'articles': articles,
            'max_page':max_page,
            'min_page':min_page,
            'is_paginated' : is_paginated,
            'recent_articles': recent_articles, 
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

        visitor_form = AddVisitorForm()
        comment_form = AddCommentForm()
        reply_form = AddReplyForm()
        comment = Comment()
        comment_and_reply = comment.get_comment_and_reply(article)
        article.page_view += 1
        article.save()
        recent_articles = ArticleModel.objects.filter(site=site, is_published=True).order_by('-created_date')[:3]

        msg = request.GET.get('msg', 'none')

        if msg == 'add':
            message = 'Komentar Anda akan tampil setelah disetujui Admin'
        else:
            message = ''

        if site.domain == 'sidomo.com':
            template = "zeon_backend/templates/blog-post.html"
            return render(request, template, 
                {'article': article, 
                'message': message,
                'recent_articles': recent_articles, 
                'comments':comment_and_reply,
                'visitor_form': visitor_form,
                'comment_form': comment_form,
                'reply_form': reply_form})

        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
        self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
        template = "company_profile/%s/article-detail.html"%(configs.templates.dir_name)
        return render(request, template, {
            'article': article, 
            'message': message,
            'recent_articles': recent_articles, 
            'comments':comment_and_reply,
            'visitor_form': visitor_form,
            'comment_form': comment_form,
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
            if kwargs['page_slug'] == 'hubungi':
                return render(request, "zeon_backend/templates/contact.html")
            elif kwargs['page_slug'] == 'profil':
                return render(request, "zeon_backend/templates/coming-soon.html")
                
            elif kwargs['page_slug'] == 'marketing-plan':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'partner':
                return render(request, "zeon_backend/templates/coming-soon.html")

            elif kwargs['page_slug'] == 'website-builder':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'android-builder':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'ios-builder':
                return render(request, "zeon_backend/templates/coming-soon.html")

            elif kwargs['page_slug'] == 'harga':
                return render(request, "zeon_backend/templates/pricing-tables.html")

            elif kwargs['page_slug'] == 'galeri-event':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'testimoni':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'kebijakan-privasi':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'syarat-ketentuan':
                return render(request, "zeon_backend/templates/coming-soon.html")

            elif kwargs['page_slug'] == 'faq':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'stockist-cabang':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'metode-pembayaran':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'karir':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'developer-club':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'kritik-saran':
                return render(request, "zeon_backend/templates/coming-soon.html")
            elif kwargs['page_slug'] == 'report':
                return render(request, "zeon_backend/templates/coming-soon.html")
            else:
                return render(request, "zeon_backend/templates/404.html")

        assets = configs.brand_assets
        scheme = configs.color_scheme
        identity = configs.brand_identity
        self.component['base'] = "company_profile/%s/base.html"%(configs.templates.dir_name) 
        self.component['sidebar'] = "company_profile/%s/sidebar.html"%(configs.templates.dir_name) 
        if request.GET.get('method', '') == 'preview':
            page = TempPageModel.objects.get(slug=kwargs['page_slug'])
        else:
            page = PageModel.objects.get(slug=kwargs['page_slug'])

        page.page_view += 1
        page.save()
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
    
    
    def post(self, request, *args, **kwargs):
        data = super(Comment, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        try:
            method = kwargs['method']
            article = ArticleModel.objects.get(site=site, slug=kwargs['article_slug'])
        except:
            method = ''
            article = ''
        
        if method != 'add' or not article:
            return HttpResponse('Wrong Method', status=403)

        visitor_form = AddVisitorForm(request.POST)
        comment_form = AddCommentForm(request.POST)
        if visitor_form.is_valid() and comment_form.is_valid():
            visitor_form_data = visitor_form.cleaned_data
            visitor = VisitorModel.objects.get_or_create(email=visitor_form_data['email'],
                    site=site,
                    name=visitor_form_data['name'])[0]
            comment_form_data = comment_form.cleaned_data
            comment = CommentModel.objects.create(visitor=visitor,
                    site=site,
                    content=comment_form_data['content'],
                    article=article)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER')+'?msg=add')
    

    def get_comment_and_reply(self, article):
        comments = CommentModel.objects.filter(
                    is_approved=True,
                    article=article)
        return [self.format_comment(comment) for comment in comments]

    def format_comment(self, comment):
        return {
            'created_date' : comment.created_date.strftime("%d/%B/%Y %H:%m"),
            'visitor': comment.visitor.name, 
            'content': comment.content,
            'is_approved': comment.is_approved,
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


class ComponentRenderer:
    def get_component(self, request, token, data, configs, site, member, form, featured_image):
        main = render_to_string(self.component['main'], 
                                    {'form': form,'token': token, 'member': member,'data': data, 'site': site, 'configs': configs,
                                    'featured_image' : featured_image})
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

class ArticleList(Dispatcher):
    def get(self, request, *args, **kwargs):
        data = super(ArticleList, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        try:
            method = kwargs['method']
        except:
            method = ''
        
        if method == 'add':
            return HttpResponse('Wrong Method', status=403)
        try:
            articles = ArticleModel.objects.filter(site=site)
        except:
            return HttpResponse('Article Not Found', status=404)

        if articles:
            return JsonResponse([{
                "article_title":article.title, 
                "article_url":article.get_article_url(),
                "article_is_published":article.is_published,
                "article_featured_image":article.get_image_url()} for article in articles], safe=False)

class Reply(Dispatcher):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Not Found' , status=404)
    
    
    def post(self, request, *args, **kwargs):
        data = super(Reply, self).get(request, args, kwargs)
        configs = UserConfigs.objects.get(member = data['member'])
        site = data['site']
        try:
            method = kwargs['method']
            article = ArticleModel.objects.get(site=site, slug=kwargs['article_slug'])
        except:
            method = ''
            article = ''

        if method != 'add' or not article:
            return HttpResponse('Wrong Method', status=403)

        visitor_form = AddVisitorForm(request.POST)
        reply_form = AddReplyForm(request.POST)
        if visitor_form.is_valid() and reply_form.is_valid():
            visitor_form_data = visitor_form.cleaned_data
            visitor = VisitorModel.objects.get_or_create(email=visitor_form_data['email'],
                    name=visitor_form_data['name'])[0]
            try:
                comment = CommentModel.objects.get(pk=kwargs['comment_pk'])
            except:
                return HttpResponse('Not Found', status=404)
            
            reply_form_data = reply_form.cleaned_data
            reply = ReplyModel.objects.create(visitor=visitor,
                    content=reply_form_data['content'], comment=comment)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))