from django.contrib import admin
from comptes.models import *

# Register your models here.

class adminProfil(admin.ModelAdmin):
    list_display = ("user","licensenumber","placeofbirth","profile","image","bio")

admin.site.register(Profil,adminProfil)

