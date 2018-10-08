from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.middleware.csrf import get_token
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ArticleAddForm, ArticlePreviewForm, CategoryAddForm
from company_profile.cp_articles.models import Article as ArticleModel
from company_profile.cp_articles.models import TempArticle as TempArticleModel
from company_profile.cp_articles.models import Category
from company_profile.cp_user_configs.models import UserConfigs
from dispatcher.views import ComponentRenderer
from dispatcher.views import Dispatcher

import time
from urllib.parse import urlparse

class CPArticle(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_articles/component/cms_article_main.html'
    index_local_script = 'cp_articles/component/cms_article_local_script.html'
    add_main = 'cp_articles/component/cms_article_add_main.html'
    add_local_script = 'cp_articles/component/cms_article_add_local_script.html'
    edit_main = 'cp_articles/component/cms_article_edit_main.html'
    edit_local_script = 'cp_articles/component/cms_article_edit_local_script.html'
    index_url = '/cms/article/'
    form = ArticleAddForm()
    def post(self, request, *args, **kwargs):
        data = super(CPArticle, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']
        if  kwargs['action'] == 'edit':
            article = ArticleModel.objects.get(pk=kwargs['pk'])
            self.form = ArticleAddForm(request.POST, request.FILES, instance=article)
            """
            if self.form.is_valid():
                article = self.form.save()
                if not article.category.all() :
                    article.category.add(Category.objects.get_or_create(site=site, title="post")[0])
                    article.save()
                return HttpResponseRedirect(self.index_url)
            """
        elif  kwargs['action'] == 'preview':
            self.form = ArticlePreviewForm(request.POST, request.FILES)
        else:
            self.form = ArticleAddForm(request.POST, request.FILES)

        if self.form.is_valid():
            article = self.form.save(commit=False)
            article.site = site
            article.save()
            self.form.save_m2m()
            if kwargs['action'] != 'preview':
                if not article.category.all() :
                    article.category.add(Category.objects.get_or_create(site=site, title="post")[0])
                    article.save()
            else:
                referer = request.META['HTTP_REFERER']
                if '/cms/article/edit' in referer:
                    parse_object = urlparse(referer)
                    url_splitted = parse_object.path.split("/")
                    try:
                        old_article = ArticleModel.objects.get(pk = url_splitted[-2])
                    except:
                        old_article = ''
                    if old_article and not article.featured_image:
                        article.featured_image = old_article.featured_image
                        article.save()

                if not article.category.all() :
                    article.category.clear()
                    article.category.add(Category.objects.get_or_create(site=site, title="preview")[0])
                    article.save()
            if kwargs['action'] == 'preview':
                article.class_name='TempArticle'
                article.save()
                return JsonResponse({'url': article.get_article_url()}, status=200)

            return HttpResponseRedirect(self.index_url)

        self.form.fields["category"].queryset = Category.objects.filter(site=site)
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
                    article = ArticleModel.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)
        method = request.GET.get('method', '')
        data = super(CPArticle, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        self.form.fields["category"].queryset = Category.objects.filter(site=site)
        form = self.form
        featured_image = ''
        if  kwargs['action'] == 'edit':
            featured_image = article.get_image_url()
            form = ArticleAddForm(instance=article)
        elif  kwargs['action'] == 'delete':
            article.delete()
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
                'member': member,
                'data': data,
                'configs': configs,
                'site': site,
                'token': token,
                'component':self.component,
                'featured_image' : featured_image,
            }
        )


class CPCategory(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_articles/component/cms_category_main.html'
    index_local_script = 'cp_articles/component/cms_category_local_script.html'
    add_main = 'cp_articles/component/cms_category_add_main.html'
    add_local_script = 'cp_articles/component/cms_category_add_local_script.html'
    edit_main = 'cp_articles/component/cms_category_edit_main.html'
    edit_local_script = 'cp_articles/component/cms_category_edit_local_script.html'
    index_url = '/cms/category/'
    form = CategoryAddForm()

    def post(self, request, *args, **kwargs):
        data = super(CPCategory, self).get(request, args, kwargs)
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
        data = super(CPCategory, self).get(request, args, kwargs)
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
            articles = ArticleModel.objects.filter(category=category)
            if articles:
                for article in articles:
                    try:
                        article.category.remove(category)
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
