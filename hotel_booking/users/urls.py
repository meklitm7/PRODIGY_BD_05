from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    UserListView,
    UserDetailView,
     
)

urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),

    path(
        "users/",
        UserListView.as_view(),
        name="user-list",
    ),

    path(
        "users/<uuid:id>/",
        UserDetailView.as_view(),
        name="user-detail",
    ),

     
]