from __future__ import unicode_literals

import datetime
import hashlib
import re
import string

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db import models, transaction
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now as datetime_now
from django.utils.translation import ugettext_lazy as _

from .users import UserModel, UserModelString

SHA1_RE = re.compile('^[a-f0-9]{40}$')


def send_email(addresses_to, ctx_dict, subject_template, body_template,
               body_html_template):
    """
    Function that sends an email
    """
    subject = (
        getattr(settings, 'REGISTRATION_EMAIL_SUBJECT_PREFIX', '') +
        render_to_string(
            subject_template, ctx_dict)
    )
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    from_email = getattr(settings, 'REGISTRATION_DEFAULT_FROM_EMAIL',
                         settings.DEFAULT_FROM_EMAIL)
    message_txt = render_to_string(body_template,
                                   ctx_dict)

    email_message = EmailMultiAlternatives(subject, message_txt,
                                           from_email, addresses_to)

    if getattr(settings, 'REGISTRATION_EMAIL_HTML', True):
        try:
            message_html = render_to_string(
                body_html_template, ctx_dict)
        except TemplateDoesNotExist:
            pass
        else:
            email_message.attach_alternative(message_html, 'text/html')

    email_message.send()


class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.

    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.

    """

    def _activate(self, profile, get_profile):
        """
        Activate the ``RegistrationProfile`` given as argument.
        User is able to login, as ``is_active`` is set to ``True``
        """
        user = profile.user
        user.is_active = True
        profile.activated = True

        with transaction.atomic():
            user.save()
            profile.save()
        if get_profile:
            return profile
        else:
            return user

    def activate_user(self, activation_key, get_profile=False):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.

        If the key is valid and has not expired, return the ``User``
        after activating.

        If the key is not valid or has expired, return ``False``.

        If the key is valid but the ``User`` is already active,
        return ``User``.

        If the key is valid but the ``User`` is inactive, return ``False``.

        To prevent reactivation of an account which has been
        deactivated by site administrators, ``RegistrationProfile.activated``
        is set to ``True`` after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                # This is an actual activation failure as the activation
                # key does not exist. It is *not* the scenario where an
                # already activated User reuses an activation key.
                return False

            if profile.activated:
                # The User has already activated and is trying to activate
                # again. If the User is active, return the User. Else,
                # return False as the User has been deactivated by a site
                # administrator.
                if profile.user.is_active:
                    return profile.user
                else:
                    return False

            if not profile.activation_key_expired():
                return self._activate(profile, get_profile)

        return False

    def create_inactive_user(self, site, new_user=None, send_email=True,
                             request=None, profile_info={}, **user_info):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.
        Additionally, if email is sent and ``request`` is supplied,
        it will be passed to the email template.

        """
        if new_user is None:
            password = user_info.pop('password')
            new_user = UserModel()(**user_info)
            new_user.set_password(password)
        new_user.is_active = False

        # Since we calculate the RegistrationProfile expiration from this date,
        # we want to ensure that it is current
        new_user.date_joined = datetime_now()

        with transaction.atomic():
            new_user.save()
            registration_profile = self.create_profile(
                new_user, **profile_info)

        if send_email:
            registration_profile.send_activation_email(site, request)

        return new_user

    def create_profile(self, user, **profile_info):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.

        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a secure random string.

        """
        profile = self.model(user=user, **profile_info)

        if 'activation_key' not in profile_info:
            profile.create_new_activation_key(save=False)

        profile.save()

        return profile

@python_2_unicode_compatible
class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.

    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.

    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.

    """
    user = models.OneToOneField(
        UserModelString(),
        on_delete=models.CASCADE,
        verbose_name=_('user'),
    )
    activation_key = models.CharField(_('activation key'), max_length=40)
    activated = models.BooleanField(default=False)

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    def __str__(self):
        return "Registration information for %s" % self.user

    def create_new_activation_key(self, save=True):
        """
        Create a new activation key for the user
        """
        random_string = get_random_string(length=32, allowed_chars=string.printable)
        self.activation_key = hashlib.sha1(random_string.encode('utf-8')).hexdigest()

        if save:
            self.save()

        return self.activation_key

class SupervisedRegistrationProfile(RegistrationProfile):

    # Same model as ``RegistrationProfile``, just a different
    # Manager to implement the extra functionality required
    # in admin approval
    objects = SupervisedRegistrationManager()

    def send_admin_approve_complete_email(self, site, request=None):
        """
        Send an "approval is complete" email to the user associated with this
        ``SupervisedRegistrationProfile``.

        The email will use the following templates,
        which can be overriden by settings APPROVAL_COMPLETE_EMAIL_SUBJECT,
        APPROVAL_COMPLETE_EMAIL_BODY, and APPROVAL_COMPLETE_EMAIL_HTML appropriately:

        ``registration/admin_approve_complete_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/admin_approve_complete_email.txt``
            This template will be used for the text body of the email.

        ``registration/admin_approve_complete_email.html``
            This template will be used for the text body of the email.

        These templates will each receive the following context
        variables:

        ``user``
            The new user account

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.requests.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        ``request``
            Optional Django's ``HttpRequest`` object from view.
            If supplied will be passed to the template for better
            flexibility via ``RequestContext``.
        """
        admin_approve_complete_email_subject = getattr(
            settings, 'APPROVAL_COMPLETE_EMAIL_SUBJECT',
            'registration/admin_approve_complete_email_subject.txt')
        admin_approve_complete_email_body = getattr(
            settings, 'APPROVAL_COMPLETE_EMAIL_BODY',
            'registration/admin_approve_complete_email.txt')
        admin_approve_complete_email_html = getattr(
            settings, 'APPROVAL_COMPLETE_EMAIL_HTML',
            'registration/admin_approve_complete_email.html')

        ctx_dict = {
            'user': self.user.username,
            'site': site,
        }
        send_email(
            [self.user.email], ctx_dict,
            admin_approve_complete_email_subject,
            admin_approve_complete_email_body,
            admin_approve_complete_email_html
        )
