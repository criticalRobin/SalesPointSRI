from django.urls import path
from SalesPoint.core.erp.views.category.views import *
from SalesPoint.core.erp.views.client.views import *
from SalesPoint.core.erp.views.product.views import *
from SalesPoint.core.erp.views.sale.views import *
from SalesPoint.core.erp.views.tests.views import *

app_name = 'erp'

urlpatterns = [
    # URLS DE LA PARTE DE CATEGORIAS
    path('categoria/listado', CategoryListView.as_view(), name='category_list'),
    path('categoria/agregar/', CategoryCreateView.as_view(), name='category_create'),
    path('categoria/editar/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('categoria/eliminar/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # URLS DE LA PARTE DE CLIENTES
    path('cliente/listado', ClientListView.as_view(), name='client_list'),
    path('cliente/agregar/', ClientCreateView.as_view(), name='client_create'),
    path('cliente/editar/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('cliente/eliminar/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # URLS DE LA PARTE DE PRODUCTOS
    path('producto/listado', ProductListView.as_view(), name='product_list'),
    path('producto/agregar/', ProductCreateView.as_view(), name='product_create'),
    path('producto/editar/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('producto/eliminar/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # URLS DE LA PARTE DE VENTAS
    path('venta/listado', SaleListView.as_view(), name='sale_list'),
    path('venta/agregar/', SaleCreateView.as_view(), name='sale_create'),
    path('venta/editar/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('venta/eliminar/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('venta/pdf/<int:pk>/', SaleInvoicePdf.as_view(), name='sale_pdf'),
    # test
    path('test/', TestView.as_view(), name='test'),
]