from django.contrib import admin
from maintenance.models import *

# Register your models here.

class maintenanceAdmin(admin.ModelAdmin):
    list_display = ("date","location","actype","acregistration","typemaintenance","privilege","ata","operation","time","maintenanceref","remark","technicalrecorder")
    list_filter = ("technicalrecorder","privilege")
    search_fields = ["technicalrecorder","acregistration","typemaintenance","actype","ata","operation"]

class typetasksAdmin(admin.ModelAdmin):
    list_display = ('singletask',)

class typeactivitiesAdmin(admin.ModelAdmin):
    list_display = ('singleactivity',)

class postAdmin(admin.ModelAdmin):
    list_display = ('title','created','updated','auteur')

admin.site.register(Post,postAdmin)
admin.site.register(maintenance,maintenanceAdmin)
admin.site.register(TypeActivities,typeactivitiesAdmin)
admin.site.register(TypeTasks,typetasksAdmin)
