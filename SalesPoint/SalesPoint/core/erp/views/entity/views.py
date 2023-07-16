from django.shortcuts import render
from SalesPoint.core.erp.models import Entity
from SalesPoint.core.erp.forms import EntityForm
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from SalesPoint.core.erp.mixins import ClientSuperMixin


class EntityUpdateView(UpdateView):
    model = Entity
    form_class = EntityForm
    template_name = "entity/create.html"
    success_url = reverse_lazy("erp:dashboard")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de tu Empresa"
        context["list_url"] = reverse_lazy("erp:dashboard")
        context["entity"] = "Entidad"
        return context