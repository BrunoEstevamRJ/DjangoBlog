
m django.urls import path
from . import views


app_name = "chat"


urlpatterns = [
        path("chat/<int:user_id>/", view.chat_room, name="chat_room"),
        ]        
