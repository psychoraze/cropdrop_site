from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("pipes/", views.pipes, name="pipes"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("success/", views.success_view, name="success"),
    path('api/data', views.get_data, name='get_data'),
    path('api/receive', views.receive_data, name='receive_data'),
]
