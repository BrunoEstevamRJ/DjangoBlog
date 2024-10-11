# urls app blog
from django.urls import path
from . import views
from .views import SignUpView

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile', views.profile, name='profile'),
    path('my-posts/', views.user_posts, name='user_posts'),
]