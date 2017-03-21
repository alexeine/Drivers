from django.shortcuts import render
from django.contrib.auth import authenticate, login
# Create your views here.
from django.views.generic import TemplateView, DetailView


class Choose(TemplateView):
	template_name = 'landing/choose.html'


class Main(TemplateView):
	template_name = 'landing/preset.html'


class Action(TemplateView):
	template_name = 'landing/action.html'

class Final(TemplateView):
	template_name = 'landing/final.html'

class Result(TemplateView):
	template_name = 'landing/result.html'