from django.http import JsonResponse
from django.shortcuts import render
from SalesPoint.core.user.models import User
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


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
        context["list_url"] = reverse_lazy("usr:user_list")
        context["entity"] = "Usuarios"
        return context