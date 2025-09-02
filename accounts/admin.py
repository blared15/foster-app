from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    readonly_fields = ('get_profile_picture',)
    
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return f'<img src="{obj.profile_picture.url}" style="max-height: 100px; max-width: 100px;" />'
        return 'No image'
    get_profile_picture.allow_tags = True
    get_profile_picture.short_description = 'Profile Picture'

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'get_profile_picture_thumb')
    
    def get_role(self, obj):
        return obj.profile.role
    get_role.short_description = 'Role'
    
    def get_profile_picture_thumb(self, obj):
        if obj.profile.profile_picture:
            return f'<img src="{obj.profile.profile_picture.url}" style="height: 30px; width: 30px; object-fit: cover; border-radius: 50%;" />'
        return 'No image'
    get_profile_picture_thumb.allow_tags = True
    get_profile_picture_thumb.short_description = 'Profile'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)