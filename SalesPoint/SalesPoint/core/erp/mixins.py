from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class CategorySuperMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "No tienes permisos para acceder a esta sección")
            return HttpResponseRedirect(reverse_lazy("erp:category_list"))
        return super(CategorySuperMixin, self).dispatch(request, *args, **kwargs)
    
    
class ProductSuperMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "No tienes permisos para acceder a esta sección")
            return HttpResponseRedirect(reverse_lazy("erp:product_list"))
        return super(ProductSuperMixin, self).dispatch(request, *args, **kwargs)
    
    
class ClientSuperMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "No tienes permisos para acceder a esta sección")
            return HttpResponseRedirect(reverse_lazy("erp:client_list"))
        return super(ClientSuperMixin, self).dispatch(request, *args, **kwargs)
    
