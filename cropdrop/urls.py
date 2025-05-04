from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("pipes/", views.pipes, name="pipes"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
]
