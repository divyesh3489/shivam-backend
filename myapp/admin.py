from django.contrib import admin
from .models import CustomUser,Blogs
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Blogs)
