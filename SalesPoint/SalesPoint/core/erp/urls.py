from django.urls import path
from SalesPoint.core.erp.views.category.views import category_list

urlpatterns = [
    path('categoria/listado', category_list, name='category_list'),
]