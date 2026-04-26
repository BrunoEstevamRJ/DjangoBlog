from django.urls import path
from accounts import views as accounts_views

app_name = 'accounts'

urlpatterns = [
    path('people/', accounts_views.discover_people, name='discover_people'),
    path('profile/<str:username>/', accounts_views.profile, name='profile'),
    path('edit-profile/', accounts_views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/follow/', accounts_views.toggle_follow, name='toggle_follow'),
]
