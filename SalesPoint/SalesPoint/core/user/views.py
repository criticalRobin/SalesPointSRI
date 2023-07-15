from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from SalesPoint.core.user.models import User
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from SalesPoint.core.user.forms import UserForm
from SalesPoint.core.user.mixins import UserSuperMixin


class UserListView(ListView):
    model = User
    template_name = "user/list.html"
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST["action"]
            if action == "searchdata":
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data = {"error": "Ha ocurrido un error"}
        except Exception as e:
            data = {"error": str(e)}
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Usuarios"
        context['create_url'] = reverse_lazy('usr:user_create')
        context["list_url"] = reverse_lazy("usr:user_list")
        context["entity"] = "Usuarios"
        return context
    
    
class UserCreateView(UserSuperMixin, CreateView):  
    model = User
    form_class = UserForm
    template_name = "user/create.html"
    success_url = reverse_lazy("usr:user_list")
    
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context["form"] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de un Usuario"
        context["list_url"] = reverse_lazy("usr:user_list")
        context["entity"] = "Usuarios"
        return context