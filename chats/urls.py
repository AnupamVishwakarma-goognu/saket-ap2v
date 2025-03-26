from django.urls import path
from . import views

urlpatterns = [
	path('create_room_api', views.create_room_api, name = "create_room_api"),
	path('chat_file_send',views.chat_file_send, name="chat_file_send"),
	path('chat_message_send',views.chat_message_send, name="chat_message_send"),
	path('document-view/<int:id>',views.downlaod_file, name="downlaod_file"),

	path('load-all-active-chat-message-forword',views.load_all_active_chat_message_forword,name="load_all_active_chat_message_forword"),
	path('chat-message-forword',views.chat_message_forword,name="chat_message_forword"),
]
