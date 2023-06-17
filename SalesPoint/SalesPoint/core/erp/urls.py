from django.urls import path
from SalesPoint.core.erp.views.category.views import *

urlpatterns = [
    path('categoria/listado', CategoryListView.as_view(), name='category_list'),
]