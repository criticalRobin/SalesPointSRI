from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class UserSuperMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(request, "No tienes permisos para acceder a esta sección")
            return HttpResponseRedirect(reverse_lazy("usr:user_list"))
        return super(UserSuperMixin, self).dispatch(request, *args, **kwargs)