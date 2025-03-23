from django.urls import path
from accounts import views as accounts_views

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', accounts_views.profile, name='profile'),
    path('edit-profile/', accounts_views.edit_profile, name='edit_profile'),
]
