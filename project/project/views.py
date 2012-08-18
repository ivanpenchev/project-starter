# project/views.py
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = "index.html"

class LoginView(TemplateView):
    template_name = "sign_in.html"
