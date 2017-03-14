from django.shortcuts import render
from django.contrib.auth import authenticate, login
# Create your views here.
from django.views.generic import TemplateView, DetailView


class StartPageView(TemplateView):
	template_name = 'landing/start.html'


class Login(TemplateView):
	template_name = 'landing/login.html'

	

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...


class Main(TemplateView):
	template_name = 'landing/main.html'