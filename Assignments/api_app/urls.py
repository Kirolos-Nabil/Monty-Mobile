from django.urls import path
from .views import UserViews

urlpatterns = [
    path('user-api/', UserViews.as_view()),
    path('user-api/<int:id>', UserViews.as_view())
]