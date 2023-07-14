# from decimal import Decimal
# from gettext import translation
import json
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import render
from SalesPoint.core.erp.models import Sale, Product, SaleDetails
from SalesPoint.core.erp.forms import SaleForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import transaction
# import os
# from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required


# class SaleListView(ListView):
#     model = Sale
#     template_name = 'sale/list.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['list_url'] = reverse_lazy('erp:sale_list')
#         context['entity'] = 'Ventas'
#         return context


class SaleListView(ListView):
    model = Sale
    template_name = "sale/list.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
            elif action == "search_details_prod":
                data = []
                for i in SaleDetails.objects.filter(sale_id=request.POST["id"]):
                    print(i)
                    data.append(i.toJSON())
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Ventas"
        context["create_url"] = reverse_lazy("erp:sale_create")
        context["list_url"] = reverse_lazy("erp:sale_list")
        context["entity"] = "Ventas"
        return context


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale/create.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_products":
                data = []
                prods = Product.objects.filter(name__icontains=request.POST["term"], stock__gt=0)
                for i in prods[0:10]:
                    item = i.toJSON()
                    item["value"] = i.name
                    data.append(item)
            elif action == "add":
                with transaction.atomic():
                    vents = json.loads(request.POST["vents"])
                    sale = Sale()
                    date_sale_str = self.request.POST.get("date_sale")
                    date_sale = datetime.strptime(date_sale_str, "%d/%m/%Y").strftime("%Y-%m-%d")
                    sale.date_sale = date_sale
                    sale.client_id = self.request.POST.get("client")
                    sale.save()

                    for i in vents["products"]:
                        det = SaleDetails()
                        det.price = float(i["pvp"])
                        det.amount = int(i["amount"])
                        det.product_id = i["id"]
                        det.sale = sale  # Asignar el objeto Sale a SaleDetails
                        det.save()
                        det.product.stock -= det.amount
                        det.product.save()

                    sale.calculate_total()  # Calcular subtotal y total
                    sale.save()  # Guardar Sale actualizado

                    # Actualizar los valores de subtotal y total en el formulario
                    form = self.get_form()
                    form.instance = sale
                    form.fields["subtotal"].initial = sale.subtotal
                    form.fields["total"].initial = sale.total

                    if form.is_valid():
                        form.save()
            else:
                raise Exception("El formulario no es válido")

        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de una Venta"
        context["list_url"] = reverse_lazy("erp:sale_list")
        context["entity"] = "Ventas"
        context["action"] = "add"
        return context


class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = "sale/create.html"
    success_url = reverse_lazy("erp:sale_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de una Venta"
        context["list_url"] = reverse_lazy("erp:sale_list")
        context["entity"] = "Ventas"
        return context


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = "sale/delete.html"
    success_url = reverse_lazy("erp:sale_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminación de una Ventas"
        context["list_url"] = reverse_lazy("erp:sale_list")
        context["entity"] = "Ventas"
        return context


class SaleInvoicePdf(View):
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    # def link_callback(self, uri, rel):
    #         """
    #         Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    #         resources
    #         """
    #         result = finders.find(uri)
    #         if result:
    #                 if not isinstance(result, (list, tuple)):
    #                         result = [result]
    #                 result = list(os.path.realpath(path) for path in result)
    #                 path=result[0]
    #         else:
    #                 sUrl = settings.STATIC_URL        # Typically /static/
    #                 sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
    #                 mUrl = settings.MEDIA_URL         # Typically /media/
    #                 mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

    #                 if uri.startswith(mUrl):
    #                         path = os.path.join(mRoot, uri.replace(mUrl, ""))
    #                 elif uri.startswith(sUrl):
    #                         path = os.path.join(sRoot, uri.replace(sUrl, ""))
    #                 else:
    #                         return uri

    #         # make sure that file exists
    #         if not os.path.isfile(path):
    #                 raise Exception(
    #                         'media URI must start with %s or %s' % (sUrl, mUrl)
    #                 )
    #         return path

    def get(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(pk=self.kwargs["pk"])
            # products_iva_12 = sale.details.filter(product__iva="12.00")
            # iva_12_total = sum(product.subtotal * Decimal("0.12") for product in products_iva_12)
            template = get_template("sale/invoice.html")
            context = {
                "sale": sale,
                "comp": {
                    "name": "TIENDITA S.A.",
                    "ruc": "9999999999999",
                    "address": "Su Corazón",
                },
                # "iva_12_total": iva_12_total,
            }
            html = template.render(context)
            response = HttpResponse(content_type="application/pdf")
            pisa_status = pisa.CreatePDF(html, dest=response)
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy("erp:sale_create"))
