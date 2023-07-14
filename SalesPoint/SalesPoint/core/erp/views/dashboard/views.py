from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import FloatField
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.db.models import FloatField
from django.contrib.auth.decorators import login_required

from SalesPoint.core.erp.models import Sale, Product, SaleDetails


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "get_graph_sales_year_month":
                data = {
                    "name": "Porcentaje de venta",
                    "showInLegend": False,
                    "colorByPoint": True,
                    "data": self.get_graph_sales_year_month(),
                }
            elif action == "get_graph_sales_products_year_month":
                data = {
                    "name": "Porcentaje",
                    "colorByPoint": True,
                    "data": self.get_graph_sales_products_year_month(),
                }
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_graph_sales_year_month(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 13):
                total = (
                    Sale.objects.filter(date_sale__year=year, date_sale__month=m)
                    .aggregate(r=Coalesce(Sum("total"), 0, output_field=FloatField()))
                    .get("r")
                )
                data.append(float(total))
        except:
            pass
        return data

    def get_graph_sales_products_year_month(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Product.objects.all():
                total = (
                    SaleDetails.objects.filter(
                        sale__date_sale__year=year,
                        # sale__date_sale__month=month,
                        product_id=p.id,
                    )
                    .aggregate(
                        r=Coalesce(Sum("subtotal"), 0, output_field=FloatField())
                    )
                    .get("r")
                )
                if total > 0:
                    data.append({"name": p.name, "y": float(total)})
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["panel"] = "Panel de administrador"
        context["graph_sales_year_month"] = self.get_graph_sales_year_month()
        return context
