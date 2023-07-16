from django.urls import path
from SalesPoint.core.user.views import UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserChangePasswordView

app_name = "usr"

urlpatterns = [
    # URLS DE LA PARTE DE USUARIOS
    path("listado/", UserListView.as_view(), name="user_list"),
    path("crear/", UserCreateView.as_view(), name="user_create"),
    path("editar/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("eliminar/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    path("cambiar_password/<int:pk>/", UserChangePasswordView.as_view(), name="user_change_password"),
]