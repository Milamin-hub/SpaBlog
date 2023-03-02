from django.views.generic import ListView, CreateView, DetailView
from django.db.models import F
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from blog.models import Post, Comment, PostFile
from blog.forms import CommentForm, PostForm
from lxml.html import fromstring
import bleach
import re
import datetime


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 25
    ordering = ['-created']

    def get_queryset(self):
        qs = super().get_queryset()
        sort = self.request.GET.get('sort', '')
        if sort == 'name':
            qs = qs.order_by('author__username', '-created')
        elif sort == 'email':
            qs = qs.order_by('author__email', '-created')
        elif sort == 'created':
            qs = qs.order_by('-created')
        elif sort == 'created-reverse':
            qs = qs.order_by('created')
        else:
            qs = qs.order_by('-created')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.datetime.now()
        context['file'] = PostFile.objects.all()
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
        response = super().form_valid(form)
        
        # Handling files
        files = self.request.FILES.getlist('file')
        for file in files:
            post_file = PostFile(post=self.object, file=file)
            post_file.save()
            
        # Cleaning HTML content
        form.instance.body = clean_html(form.instance.body)
        
        # Validating HTML
        if not is_valid_html(form.instance.body):
            form.add_error('body', 'Invalid HTML')
            return self.form_invalid(form)
        
        return response


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_comment_id = self.request.GET.get('parent_comment_id', None)
        if parent_comment_id:
            context['parent_comment_id'] = parent_comment_id
        return context

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

class CommentReplyView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('home')
    
    def post(self, request, comment_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            post = comment.post
            parent_id = form.cleaned_data.get("parent_id")
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment = form.save(commit=False)
                comment.post = post
                comment.parent = parent_comment
                comment.save()
            else:
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
        return redirect("home")
    

def clean_html(content):
    allowed_tags = ['a', 'code', 'i', 'strong']
    allowed_attrs = {'a': ['href', 'title']}
    return bleach.clean(content, tags=allowed_tags, attributes=allowed_attrs, strip=True)

def is_valid_html(content):
    try:
        fromstring(content)
        return True
    except:
        return False