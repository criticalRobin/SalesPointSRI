from django.urls import path
from SalesPoint.core.reports.views import ReportSaleView

app_name = 'rpt'
urlpatterns = [
    # URLS DE LA PARTE DE CATEGORIAS
    path("venta/", ReportSaleView.as_view(), name="report_sale"),
]