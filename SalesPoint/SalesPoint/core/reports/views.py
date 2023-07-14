# from typing import Any, Dict
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from SalesPoint.core.erp.models import Sale
from django.urls import reverse_lazy
from SalesPoint.core.reports.forms import ReportForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
# Create your views here.

class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Sale.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_sale__range=[start_date, end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.client.dni,
                        s.client.names,
                        s.client.surnames,
                        s.date_sale.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        # format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('rpt:report_sale')
        context['form'] = ReportForm()
        return context