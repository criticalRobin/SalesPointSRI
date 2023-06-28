from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SalesPoint.core.erp.models import Client
from SalesPoint.core.erp.forms import ClientForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms.widgets import TextInput


class ClientListView(ListView):
    model = Client
    template_name = "client/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] = reverse_lazy("erp:client_list")
        context["entity"] = "Clientes"
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "client/create.html"
    success_url = reverse_lazy("erp:client_list")

    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de un Cliente"
        context["list_url"] = reverse_lazy("erp:client_list")
        context["entity"] = "Clientes"
        return context


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "client/create.html"
    success_url = reverse_lazy("erp:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de un Cliente"
        context["list_url"] = reverse_lazy("erp:client_list")
        context["entity"] = "Clientes"
        context["form"].fields["dni"].widget = TextInput(attrs={"readonly": "readonly"})
        return context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client/delete.html"
    success_url = reverse_lazy("erp:client_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminación de un Cliente"
        context["list_url"] = reverse_lazy("erp:client_list")
        context["entity"] = "Clientes"
        return context
