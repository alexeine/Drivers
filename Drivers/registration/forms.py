"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""
from __future__ import unicode_literals


from django import forms
from django.utils.translation import ugettext_lazy as _

from .users import UserModel, UsernameField
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

User = UserModel()


class EmailAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.data['username']
        try:
            username = User.objects.get(Q(email=username) | Q(username=username)).username
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )
        return username