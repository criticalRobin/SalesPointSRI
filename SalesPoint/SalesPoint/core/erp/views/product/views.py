from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from SalesPoint.core.erp.models import Product
from SalesPoint.core.erp.forms import ProductForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Productos'
        return context
    
    
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('erp:product_list')
    
    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Producto'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Productos'
        return context
    
    
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('erp:product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de un Producto'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Productos'
        return context
    
    
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('erp:product_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Producto'
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Productos'
        return context