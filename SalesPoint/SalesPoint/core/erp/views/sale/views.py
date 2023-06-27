from gettext import translation
import json
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import render
from SalesPoint.core.erp.models import Sale, Product, SaleDetails
from SalesPoint.core.erp.forms import SaleForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import transaction
import os
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


class SaleListView(ListView):
    model = Sale
    template_name = 'sale/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Product.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    sale = Sale()
                    date_sale_str = self.request.POST.get('date_sale')
                    date_sale = datetime.strptime(date_sale_str, '%d/%m/%Y').strftime('%Y-%m-%d')
                    sale.date_sale = date_sale
                    sale.subtotal = float(vents['subtotal'])
                    sale.iva = float(vents['iva'])
                    sale.total = float(vents['total'])
                    sale.client_id = self.request.POST.get('client')
                    sale.save()
                    
                    for i in vents['products']:
                        det = SaleDetails()
                        det.price = float(i['pvp'])
                        det.amount = int(i['amount'])
                        det.subtotal = float(i['subtotal'])
                        det.product_id = i['id']
                        det.sale_id = sale.id
                        det.save()
            else:
                data['error'] = 'No ha ingresado una opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Ventas'
        context['action'] = 'add'
        return context
    
    
class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('erp:sale_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Venta'
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context
    
    
class SaleDeleteView(DeleteView):
    model = Sale
    template_name = 'sale/delete.html'
    success_url = reverse_lazy('erp:sale_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de una Ventas'
        context['list_url'] = reverse_lazy('erp:sale_list')
        context['entity'] = 'Ventas'
        return context
    

class SaleInvoicePdf(View):
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
            template = get_template('sale/invoice.html')
            context = {
                'sale': Sale.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'TIENDITA S.A.', 'ruc': '9999999999999', 'address': 'Su Corazón'},
                # 'icon': '{}{}'.format(settings.STATIC_URL, 'noviaaaa.jpg'),
                }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                # link_callback=self.link_callback
                )
            return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(reverse_lazy('erp:sale_create'))