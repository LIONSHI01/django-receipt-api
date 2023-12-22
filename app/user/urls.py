"""
URL mappings for the user API.
"""

from django.urls import path
from user import views


# NOTE: define app_name and url so in tests file : CREATE_USER_URL = reverse('user:create') could get the same url
app_name = 'user'
urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create')
]
