from django.urls import path
from SalesPoint.core.user.views import UserListView, UserCreateView

app_name = "usr"

urlpatterns = [
    # URLS DE LA PARTE DE USUARIOS
    path("listado/", UserListView.as_view(), name="user_list"),
    path("crear/", UserCreateView.as_view(), name="user_create"),
    # path("categoria/agregar/", CategoryCreateView.as_view(), name="category_create"),
    # path(
    #     "categoria/editar/<int:pk>/",
    #     CategoryUpdateView.as_view(),
    #     name="category_update",
    # ),
    # path(
    #     "categoria/eliminar/<int:pk>/",
    #     CategoryDeleteView.as_view(),
    #     name="category_delete",
    # ),
]