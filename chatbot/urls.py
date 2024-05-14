from django.urls import path
from .views import dog_chatbot, show_chatbot, get_chat_history

urlpatterns = [
    path('dog_chatbot/', dog_chatbot, name='dog_chatbot'),  # 定义路由
    path('', show_chatbot, name='show_chatbot'),  # 前端页面
    path('get_chat_history/', get_chat_history, name='get_chat_history'),  # 前端页面
]