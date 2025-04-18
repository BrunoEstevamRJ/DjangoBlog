from . import views

from django.urls import path
from accounts import views as accounts_views

from .views import SignUpView, PostCreateView, edit_post, post_single, add_comment, delete_comment, PostDeleteView
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from accounts.views import profile

app_name = 'blog'

urlpatterns = [

    # Base
    path('', views.home, name='homepage'),
    path('create/', PostCreateView.as_view(), name='create_post'),

    # signup | login | logout  
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),    
    path('accounts/logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),

    

    # Profile
    path('profile/<str:username>/', profile, name='profile'),
    path('accounts/edit-profiles/', accounts_views.edit_profile, name='edit-profile'),


    path('my-posts/', views.user_posts, name='user_posts'),
    path('<slug:post_slug>/', post_single, name='post_single'),

    # Rotas do Post
    path('<slug:post_slug>/', views.post_single, name='post_single'),
    path('<slug:post_slug>/edit/', views.edit_post, name='edit_post'),     
    path('<slug:post_slug>/comment/', views.add_comment, name='add_comment'),
    path('comentario/<int:comment_id>/apagar/', delete_comment, name='delete_comment'),
    path('<slug:post_slug>/like/', views.like_post, name='like_post'),
    path('<slug:post_slug>/dislike/', views.dislike_post, name='dislike_post'),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path('<slug:post_slug>/comment/<int:parent_id>/', views.add_comment, name='reply_comment'),
]
