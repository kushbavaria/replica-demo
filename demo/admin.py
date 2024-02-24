from django.contrib import admin

# Register your models here.

from .models import Celeb, Celeb_occupation, Occupation

admin.site.register(Celeb)
admin.site.register(Occupation)
admin.site.register(Celeb_occupation)
