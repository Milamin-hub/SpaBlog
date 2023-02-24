"""SpaBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account.views import LoginView, LogoutView, RegisterView
from blog.views import PostListView, PostDetailView
from blog.views import CommentCreateView, PostCreateView

from django.conf import settings
from django.conf.urls.static import static
from captcha.views import captcha_image

app_name = 'blog'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', PostListView.as_view(), name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),


    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    path('captcha-image/<str:key>/', captcha_image, name='captcha-image'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)