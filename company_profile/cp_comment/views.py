from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.middleware.csrf import get_token

from company_profile.cp_user_configs.models import UserConfigs
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
    index_main = 'cp_comment/component/cms_comment_main.html'
    index_local_script = 'cp_comment/component/cms_comment_local_script.html'
    add_main = 'cp_comment/component/cms_comment_add_main.html'
    add_local_script = 'cp_comment/component/cms_comment_add_local_script.html'
    edit_main = 'cp_comment/component/cms_comment_edit_main.html'
    edit_local_script = 'cp_comment/component/cms_comment_edit_local_script.html'
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
        if  kwargs['action'] == 'delete' or \
            kwargs['action'] == 'approve' :
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    comment = Comment.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)

        if kwargs['action'] == 'delete' and \
            comment :
            comment.delete()
            return HttpResponseRedirect(self.index_url)

        elif kwargs['action'] == 'approve' and \
            comment :
            comment.is_approved = True
            comment.save()
            return HttpResponseRedirect(self.index_url)


        method = request.GET.get('method', '')
        data = super(CPComment, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form

        if kwargs['action'] == 'show_all':
            self.set_component(kwargs)
        else :
            return HttpResponseRedirect(self.index_url)

        comments = Comment.objects.filter(site=site)
        data['comments'] = comments

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
    add_main = 'cp_comment/component/cms_reply_add_main.html'
    add_local_script = 'cp_comment/component/cms_reply_add_local_script.html'
    index_url = '/cms/comment/'
    form = AddReplyForm()

    def post(self, request, *args, **kwargs):
        data = super(CPReply, self).get(request, args, kwargs)
        member = data['member']
        site = data['site']
        if  kwargs['action'] == 'add' and kwargs['pk']:
            self.form = AddReplyForm(request.POST)
        else:
            return HttpResponseRedirect(self.index_url)

        if self.form.is_valid():
            try:
                comment = Comment.objects.get(pk=kwargs['pk'])
            except:
                return HttpResponseRedirect(self.index_url)
            form_content = self.form.cleaned_data.get('content')
        
            visitor = Visitor.objects.get_or_create(name='admin@%s'%site.domain,
                        site=site)[0]

            Reply.objects.create(comment=comment,
                visitor=visitor,
                content=form_content,
                is_approved=True)

        return HttpResponseRedirect(self.index_url)

    def get(self, request, *args, **kwargs):
        comment = reply = ""
        if  kwargs['action'] == 'delete' or \
            kwargs['action'] == 'add' or \
            kwargs['action'] == 'approve' :
            if kwargs['pk'] == 'none':
                return HttpResponseRedirect(self.index_url)
            else :
                try:
                    if kwargs['action'] == 'add':
                        comment = Comment.objects.get(pk=kwargs['pk'])
                    else:
                        reply = Reply.objects.get(pk=kwargs['pk'])
                except:
                    return HttpResponseRedirect(self.index_url)
                

        if kwargs['action'] == 'delete' and \
            reply :
            reply.delete()
            return HttpResponseRedirect(self.index_url)

        elif kwargs['action'] == 'approve' and \
            reply :
            reply.is_approved = True
            reply.save()
            return HttpResponseRedirect(self.index_url)


        method = request.GET.get('method', '')
        data = super(CPReply, self).get(request, args, kwargs)
        token = get_token(request)
        member = data['member']
        configs = UserConfigs.objects.get(member = member)
        site = data['site']
        form = self.form

        if kwargs['action'] == 'add' and comment:
            data['comment'] = comment
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
