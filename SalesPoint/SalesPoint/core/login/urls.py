from django.urls import path
from SalesPoint.core.login.views import LoginFormView, LogoutView


urlpatterns = [
    path("", LoginFormView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name="logout"),
]
