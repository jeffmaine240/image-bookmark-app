from django.contrib import admin
from .models import Profile, Contact

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Contact)