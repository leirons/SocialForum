import logging
from typing import Any, Dict


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.safestring import mark_safe
from django.core.cache import cache


import json


from .exceptions.ThereNotAnyPosts import ThereNotAnyPosts
from .filters import Filter
from .models import *
from .services import subscribelogic

logger = logging.getLogger('django')

# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID


class MultipleModelView(TemplateView):
    """Shows all Subjects and Themes of the subject"""
    template_name = 'mysite/base_mysite.html'

    def get_context_data(self) -> Dict[str, Any]:
        logger.info(f"The user {self.request.user} entered on the page ")

        messages = cache.get("messages")[:50]
        filter_ = Filter(self.request.GET, queryset=Theme.objects.all())
        context = super(MultipleModelView, self).get_context_data()
        context['modeltwo'] = Theme.objects.all()
        context['modelone'] = Subject.objects.all()
        context['modelsix'] = Post.objects.all().order_by('created_at')[:10]
        context['filter'] = filter_
        context["room_name_json"] = mark_safe(json.dumps("chat"))
        context["messages"] = mark_safe(json.dumps(messages))
        print(messages)
        return context


class Themes(TemplateView):
    """Shows all themes in Subject"""
    template_name = 'mysite/themes.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super(Themes, self).get_context_data()
        try:
            logger.info(f"The user {self.request.user.id} went to the page")
            last_post_id = Post.objects.filter(where_we_are__slug=self.kwargs['slug']).last().id
            context['last_three_comments'] = Comments.objects.filter(post_id=last_post_id)[:3]
            context['last_five_comments'] = Comments.objects.all()[:5]
            post_list = Post.objects.all()
            paginator = Paginator(post_list, 10)
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['page_obj'] = page_obj
            context['slug'] = self.kwargs['slug']
        except Exception as ThereNotAnyPosts:
            logger.info(ThereNotAnyPosts)
        finally:
            return context


class Posts(TemplateView):
    template_name = 'mysite/posts.html'

    def get_context_data(self, **kwargs) -> Dict[str, Any]:

        """
        ?????????? ???????????????????????? ?? ??????????.
        ???????? ?????????????????????? ?????????????? ????????????????????????, ?????????????? ??????????????????
        ?? ????????????, ???? ?????????????????????? ???? ?????????????? ?? ??????????????.
        ?????? ???????????????????????????? ?????????????????????????? ?????????????? ???????? ????????????????????????
        """
        logger.info(f"The user went to the page: {self.request.user.id}")

        if self.request.user:
            P = Post.objects.get(pk=kwargs['pk'])
            P.popularity = P.popularity + 1
            P.save()

        context = super(Posts, self).get_context_data(**kwargs)
        user_id = self.request.user.id
        args = 'user_id', 'user__username', 'post__id', 'body', 'created_on'
        if user_id:
            comments = Comments.objects.values(*args).exclude(
                user_id__ignore_user__in=CustomUser.objects.get(id=user_id).user.all()
            ).prefetch_related('user')
        else:
            comments = Comments.objects.values(*args).filter(post_id=kwargs['pk'])

        for comment in comments:
            user_of_comment = comment['user_id']
            user_object = CustomUser.objects.get(id=user_of_comment)
            comment['online'] = user_object.online()

        context['user_id'] = self.request.user.id
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class EditComments(UpdateView):
    model = Comments
    template_name = 'mysite/comments.html'
    fields = ['body']

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """?????????????????? ?????? ??????????????, ???????? ?????????? ???? ?????????????????? ??????????????????????????"""
        logger.info(f"???? ???????????????? ??????????{self.request.user.id}")
        context = super().get_context_data(**kwargs)
        login_user_id = self.request.user.pk
        post_id = Comments.objects.get(id=self.kwargs['pk'])
        context['Error'] = True
        if post_id.user_id != login_user_id:
            context['Error'] = False
            logger.info(f"The comment is not a user, it is forbidden to edit {post_id.user_id}")
        logger.info(f'Editing is allowed')

        return context


class EditPost(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'mysite/post_edit.html'
    fields = ['title', 'text']

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """?????????????????? ?????? ????????, ???????? ?????????? ???? ?????????????????? ??????????????????????????"""
        context = super().get_context_data(**kwargs)
        login_user_id = self.request.user.pk
        post_id = Post.objects.get(id=self.kwargs['pk'])
        print(login_user_id)
        print(post_id.user_id)
        context['Error'] = True
        if post_id.user_id != login_user_id:
            context['Error'] = False

        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'mysite/CreatePost.html'
    success_url = reverse_lazy('themes')

    def form_valid(self, form) -> super:
        obj = form.save(commit=False)
        obj.user_id = self.request.user.id
        get_slug = Theme.objects.get(slug=self.kwargs['slug'])
        obj.where_we_are_id = get_slug.id
        return super().form_valid(form)


class CreateComment(LoginRequiredMixin, CreateView):
    model = Comments
    fields = ['user', 'post', 'body']
    template_name = 'mysite/CreateComment.html'
    success_url = reverse_lazy('themes')

    def form_valid(self, form) -> super:
        obj = form.save(commit=False)
        obj.user_id = self.request.user.id
        obj.save()
        return super().form_valid(form)


class Profile(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data()


def subscribe(request):
    if request.method == "POST":
        logger.info(f"User {request.user.id} subscribed to the newsletter")
        email = request.POST['email']
        subscribelogic.subscribelogic(email)
        messages.success(request, "Email received. thank You! ")

    return render(request, "mysite/base_mysite.html")
