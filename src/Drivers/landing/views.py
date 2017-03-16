from django.shortcuts import render
from django.contrib.auth import authenticate, login
# Create your views here.
from django.views.generic import TemplateView, DetailView


class StartPageView(TemplateView):
	template_name = 'landing/start.html'


class Main(TemplateView):
	template_name = 'landing/main.html'