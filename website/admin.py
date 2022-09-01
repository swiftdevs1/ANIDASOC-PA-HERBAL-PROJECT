from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(About)
admin.site.register(Testimony)
admin.site.register(Review)


