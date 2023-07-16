from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from SalesPoint.core.erp.models import Product
from SalesPoint.core.erp.forms import ProductForm, CategoryIVAForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from SalesPoint.core.erp.mixins import ProductSuperMixin


class ProductListView(ListView):
    model = Product
    template_name = 'product/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Product.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('erp:product_create')
        context['list_url'] = reverse_lazy('erp:product_list')
        context['entity'] = 'Productos'
        return context


class ProductCreateView(ProductSuperMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/create.html"
    success_url = reverse_lazy("erp:product_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de un Producto"
        context["list_url"] = reverse_lazy("erp:product_list")
        context["entity"] = "Productos"
        return context


class ProductUpdateView(ProductSuperMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/create.html"
    success_url = reverse_lazy("erp:product_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de un Producto"
        context["list_url"] = reverse_lazy("erp:product_list")
        context["entity"] = "Productos"
        return context
    

class CategoryIVAUpdateView(ProductSuperMixin, View):
    template_name = "product/create.html"
    success_url = reverse_lazy("erp:product_list")

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = CategoryIVAForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CategoryIVAForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            new_iva_choice = form.cleaned_data["new_iva"]
            new_iva_value = form.cleaned_data["new_iva_value"]

            products_in_category = Product.objects.filter(category=category)

            if new_iva_choice == "custom":
                # Si se selecciona "custom", se actualizará con el nuevo valor ingresado por teclado
                products_in_category.update(iva=str(new_iva_value))
            else:
                # Si se selecciona alguna de las opciones predefinidas, se actualizará con esa opción
                products_in_category.update(iva=new_iva_choice)

            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form})


class ProductDeleteView(ProductSuperMixin, DeleteView):
    model = Product
    template_name = "product/delete.html"
    success_url = reverse_lazy("erp:product_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eliminación de un Producto"
        context["list_url"] = reverse_lazy("erp:product_list")
        context["entity"] = "Productos"
        return context
