from django.urls import path
from . import views
from .views import SignUpView, PostCreateView, edit_post, post_single, add_comment, delete_comment
from django.contrib.auth.views import LogoutView

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('create/', PostCreateView.as_view(), name='create_post'),

    # signup | login | logout  
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    #path('accounts/logout/', SignUpView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('accounts/profile', views.profile, name='profile'),
    path('accounts/edit-profiles', views.edit_profile, name='edit-profile'),

    path('my-posts/', views.user_posts, name='user_posts'),

    path('<slug:post_slug>/', post_single, name='post_single'),
    path('<slug:post_slug>/comment/', add_comment, name='add_comment'),

    # Rotas do Post
    path('<slug:post_slug>/', views.post_single, name='post_single'),
    path('<slug:post_slug>/edit/', views.edit_post, name='edit_post'),     
    path('<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    path('comentario/<int:comment_id>/apagar/', delete_comment, name='delete_comment'),
    path('<slug:post_slug>/like/', views.like_post, name='like_post'),
    path('<slug:post_slug>/dislike/', views.dislike_post, name='dislike_post'),
]
