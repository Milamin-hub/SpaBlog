from django.views.generic import ListView, CreateView, DetailView
from django.db.models import F
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from blog.models import Post, Comment
from blog.forms import CommentForm, PostForm
from django.http import HttpResponseBadRequest
import datetime


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 2
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.datetime.now()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = Post.objects.filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True).order_by(F('created_at').desc(nulls_last=True))
        context['comment_form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            try:
                form.instance.parent = Comment.objects.get(id=parent_id, post=post)
            except Comment.DoesNotExist:
                return HttpResponseBadRequest()
        
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comments.html'
    context_object_name = 'comments'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        queryset = queryset.filter(post=post, active=True)

        queryset = queryset.filter(parent__isnull=True)

        queryset = queryset.order_by('-created')

        order_by = self.request.GET.get('order_by')
        reverse = self.request.GET.get('reverse')

        if order_by == 'username':
            queryset = queryset.order_by('author__username')

        elif order_by == 'email':
            queryset = queryset.order_by('author__email')

        elif order_by == 'created':
            queryset = queryset.order_by('created')

        if reverse == '1':
            queryset = queryset.reverse()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context