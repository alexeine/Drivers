from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ('user', 'image_thumb', 'image',  'slug',  'email', 'position',
        'investment', 'area', 'company', 'holding', 'cluster', 'total', 'ebitda',
        'userInvestment', 'teamInvestment', 'rentability',)
    #readonly_fields = ['image_thumb', 'created_date', 'modified_date']
    inline_classes = ('grp-open',)

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
    inlines = [ProfileInline] + UserAdmin.inlines

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug',)
    search_fields = ('user__username',)
    fields = ('user', 'image_thumb', 'image',  'slug', 'investment', 'area', 'company', 'holding', 'cluster', 'total', 'ebitda',
        'userInvestment', 'teamInvestment', 'rentability', 'email', 'position', )
    #readonly_fields = ['image_thumb', 'created_date', 'modified_date']
