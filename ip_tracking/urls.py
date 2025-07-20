from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('protected/', views.authenticated_view, name='protected'),
]
