from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from Drivers.utils.mixins import UserAuthenticatedAccessMixin

from .models import Profile



class ProfileDetailView(UserAuthenticatedAccessMixin, DetailView):
    model = Profile
    template_name = 'landing/main.html'

    def get_object(self):
        if not Profile.objects.filter(slug=self.kwargs['slug']).exists() or self.request.user.profile != Profile.objects.get(slug=self.kwargs['slug']):
            raise Http404
        return self.get_queryset().get(slug=self.kwargs['slug'])
