from django.urls import path
from SalesPoint.core.erp.views.category.views import *

app_name = 'erp'

urlpatterns = [
    path('categoria/listado', CategoryListView.as_view(), name='category_list'),
    path('categoria/agregar/', CategoryCreateView.as_view(), name='category_create'),
]