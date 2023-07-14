from typing import Any, Dict
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView

class LoginFormView(LoginView):
    template_name = 'login.html'
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('erp:dashboard')
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicar Sesión'
        return context
