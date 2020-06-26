from django.contrib import admin

# Register your models here.
from .models import RadioStation, Tag, Recording

admin.site.register(RadioStation)
admin.site.register(Tag)
admin.site.register(Recording)
