from captcha.fields import CaptchaField
from django import forms
from django.forms.widgets import Textarea
from django.core.validators import RegexValidator
from blog.models import Comment, Post


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    
class CaptchaForm(forms.Form):
    captcha = forms.CharField(max_length=4)


class PostForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Post
        fields = ('title', 'body', 'tags', 'status', 'captcha')


class CommentForm(forms.ModelForm):
    captcha = forms.CharField(label='Captcha', max_length=10, validators=[RegexValidator(regex='^[0-9a-zA-Z]*$', message='Only alphanumeric characters are allowed.')])
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': Textarea(attrs={'rows': 5})
        }

