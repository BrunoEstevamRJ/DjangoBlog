# urls app blog
from django.urls import path
from . import views
from .views import SignUpView, PostCreateView

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('create/', PostCreateView.as_view(), name='create_post'),  # Coloque antes da rota com o slug
    path('<slug:post>/', views.post_single, name='post_single'),    # Mova esta rota para depois
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile', views.profile, name='profile'),
    path('accounts/edit-profiles', views.edit_profile, name='edit-profile'),
    path('my-posts/', views.user_posts, name='user_posts'),
]
