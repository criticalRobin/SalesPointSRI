from django.http import HttpResponseRedirect
from django.shortcuts import render
from SalesPoint.core.erp.mixins import CategorySuperMixin
from SalesPoint.core.erp.models import Category
from SalesPoint.core.erp.forms import CategoryForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


class CategoryListView(ListView):
    model = Category
    template_name = "category/list.html"
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_url"] = reverse_lazy("erp:category_list")
        context["entity"] = "Categorias"
        return context


class CategoryCreateView(CategorySuperMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category/create.html"
    success_url = reverse_lazy("erp:category_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de una Categoría"
        context["list_url"] = reverse_lazy("erp:category_list")
        context["entity"] = "Categorias"
        return context


class CategoryUpdateView(CategorySuperMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "category/create.html"
    success_url = reverse_lazy("erp:category_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de una Categoría"
        context["list_url"] = reverse_lazy("erp:category_list")
        context["entity"] = "Categorias"
        return context


class CategoryDeleteView(CategorySuperMixin, DeleteView):
    model = Category
    template_name = "category/delete.html"
    success_url = reverse_lazy("erp:category_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminación de una Categoría"
        context["list_url"] = reverse_lazy("erp:category_list")
        context["entity"] = "Categorias"
        return context
