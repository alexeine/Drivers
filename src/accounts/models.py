from django.db import models

# Create your models here.
import os

from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

from uuid import uuid4
from slugify import UniqueSlugify
from imagekit.processors import Adjust
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django.utils.deconstruct import deconstructible




@deconstructible
class UploadToPathAndRename(object):
    '''
        Here we are renaming photos with uuid in order to not overwrite previous photo
    '''
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)



class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_thumbnail = ProcessedImageField(upload_to=UploadToPathAndRename('avatars'),
                                           processors=[ResizeToFill(36, 36), Adjust(sharpness=1.1, contrast=1.1)],
                                           format='JPEG',
                                           options={'quality': 90}, null=True, blank=True)
    
    email = models.EmailField()
    position = models.CharField(max_length=20)
    investment = models.IntegerField()
    area = models.IntegerField()
    company = models.CharField(max_length=20)
    holding = models.CharField(max_length=20)
    cluster = models.CharField(max_length=5)
    total = models.IntegerField()
    ebitda = models.IntegerField()
    userInvestment = models.IntegerField()
    passw = models.CharField(max_length=20, default="")

    companyWeight = models.IntegerField(default=5)
    teamInvestment1 = models.IntegerField()
    teamInvestment2 = models.IntegerField()
    rentability = models.FloatField()
    investmentRentability = models.FloatField()
    

    slug = models.SlugField(unique=True, max_length=100)
    
    def image_thumb(self):
        if self.avatar_thumbnail:
            return '<img src="{0}{1}" width="36" height="36" />'.format(settings.MEDIA_URL, self.avatar_thumbnail)
        else:
            return '<img src="{0}accounts/default/default-avatar.jpg" width="36" height="36" />'.format(settings.STATIC_URL)
    image_thumb.allow_tags = True
   
    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'slug': self.slug})

    def get_avatar(self):
        if self.avatar_thumbnail:
            return self.avatar_thumbnail.url
        else:
            return '{}accounts/default/default-avatar.jpg'.format(settings.STATIC_URL)
    
    def __str__(self):
        return self.user.username

    def get_ebitda_per_area(self):
        return int(float(self.ebitda)/self.area)

def my_unique_check(text, uids):
    if text in uids:
        return False
    return not Profile.objects.filter(slug=text).exists()
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        slugify_unique = UniqueSlugify(
            unique_check=my_unique_check,
            separator='_',
            to_lower=True,
            max_length=100
        )
        slug = slugify_unique(instance.username)
        Profile.objects.create(user=instance, slug=slug)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


