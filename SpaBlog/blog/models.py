from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from captcha.fields import CaptchaField
from account.models import Profile
from django.utils.text import slugify
import magic


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-created', 'author__username', 'author__email']

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.year,self.publish.month, self.publish.day, self.slug])

    def author_photo(self):
        profile = Profile.objects.get(user=self.author)
        return profile.photo.url


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ('created', )
    
    def author_photo(self):
        profile = Profile.objects.get(user=self.author)
        return profile.photo.url

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Captcha(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='captcha')
    captcha = CaptchaField()

    class Meta:
        ordering = ('post', )
    

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='post_files')

    def save(self, *args, **kwargs):
        if self.file:
            mime = magic.Magic(mime=True)
            file_type = mime.from_buffer(self.file.read(1024))

            if file_type.startswith('image'):
                self.file.upload_to = 'post_images'
            elif file_type.startswith('text'):
                self.file.upload_to = 'post_text_files'
            else:
                # handle other types of files
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file.name}"
    
