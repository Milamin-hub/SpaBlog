from captcha.fields import CaptchaField
from django import forms
from django.forms.widgets import Textarea
from blog.models import Comment, Post


class PostForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags', 'status', 'captcha')


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'rows': 5})
        }


class CaptchaForm(forms.Form):
    captcha = forms.CharField(max_length=4)
