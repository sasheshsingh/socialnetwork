from django.urls import path
from .views import RegisterView, LoginView, UserView, UserSearchListAPIView

urlpatterns = [
    path("signup", RegisterView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("me", UserView.as_view(), name="me"),
    path("search", UserSearchListAPIView.as_view(), name="search"),
]
