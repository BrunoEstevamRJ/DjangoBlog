from django.urls import path
from . import views
from .views import SignUpView, PostCreateView, edit_post, post_single
from django.contrib.auth.views import LogoutView

app_name = 'blog'

urlpatterns = [

    path('', views.home, name='homepage'),

    path('create/', PostCreateView.as_view(), name='create_post'),  
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile', views.profile, name='profile'),
    path('accounts/edit-profiles', views.edit_profile, name='edit-profile'),

    path('my-posts/', views.user_posts, name='user_posts'),
    
    path('<slug:post_slug>/edit/', views.edit_post, name='edit_post'),
    path('<slug:post>/', views.post_single, name='post_single'), # verificar <slug:post> & <slug:post_slug>
    path('accounts/logout/', LogoutView.as_view(next_page='blog:homepage'), name='logout'),

]
