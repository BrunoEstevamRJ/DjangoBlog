from django.urls import path
from accounts import views as accounts_views  # ✅ Importação correta

app_name = 'accounts'

urlpatterns = [
    path('profile/<str:username>/', accounts_views.profile, name='profile'),  # ✅ Corrigido
    path('accounts/edit-profiles/', accounts_views.edit_profile, name='edit-profile'),
]
