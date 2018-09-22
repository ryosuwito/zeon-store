from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from dispatcher.views import ComponentRenderer
from dispatcher.views import Dispatcher

from .models import Comment, Reply, Visitor
from .forms import AddCommentForm, AddReplyForm
      
class CPComment(LoginRequiredMixin, ComponentRenderer, Dispatcher):
    login_url = '/cms/login/'
    template = "cp_admin/index.html"
    component = {}
    component['base'] = 'cp_admin/component/index_base.html'
    component['header'] =  'cp_admin/component/index_header.html'
    index_main = 'cp_articles/component/cms_comment_main.html'
    index_local_script = 'cp_articles/component/cms_comment_local_script.html'
    add_main = 'cp_articles/component/cms_comment_add_main.html'
    add_local_script = 'cp_articles/component/cms_ommenty_add_local_script.html'
    edit_main = 'cp_articles/component/cms_comment_edit_main.html'
    edit_local_script = 'cp_articles/component/cms_comment_edit_local_script.html'
    index_url = '/cms/comment/'
    form = AddCommentForm()

    def post(self, request, *args, **kwargs):
        pass
        """data = super(CPCategory, self).get(request, args, kwargs)
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
        )"""

    def get(self, request, *args, **kwargs):
        comment = ""
        if  kwargs['action'] == 'delete':
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    comment = Comment.objects.get(pk=kwargs['pk'])
                    comment.delete()
                except:
                    return HttpResponseRedirect(self.index_url)

        method = request.GET.get('method', '')
        data = super(CPComment, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form
        if  kwargs['action'] == 'edit':
            try:
                comment = Comment.objects.get(pk=kwargs['pk'])
            except:
                return HttpResponseRedirect(self.index_url)
            form = AddCommentForm(instance=comment)


        if kwargs['action'] == 'show_all' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'edit' or \
            kwargs['action'] == 'delete' :
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)

        featured_image = ""
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

class CPReply(LoginRequiredMixin, ComponentRenderer, Dispatcher):
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
    #form = CategoryAddForm()

    def post(self, request, *args, **kwargs):
        pass
        """data = super(CPCategory, self).get(request, args, kwargs)
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
        )"""

    def get(self, request, *args, **kwargs):
        pass
        """category = ""
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
        )"""
