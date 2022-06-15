from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from comptes.models import Profil
from maintenance.models import *
from .utils import render_to_pdf 
from maintenance.filters import *

# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         tasks = maintenance.objects.filter(technicalrecorder=request.user).order_by('-date')
#         user = request.user
#         data = {
#             'tasks':tasks,
#             'user':user
#         }
#         pdf = render_to_pdf('task/page.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')

def printPdf(request,id):
    user = get_object_or_404(User,id=id)
    tasks = maintenance.objects.filter(technicalrecorder=user).order_by('-date')

    data = {
        'tasks':tasks,
        'user':user,
    }
    pdf = render_to_pdf('task/page.html',data)
    return HttpResponse(pdf, content_type='application/pdf')


def printPdf_bis(request,id):

     single_profil = get_object_or_404(Profil,id=id)
     user = single_profil.user 
       
     Tasks = maintenance.objects.filter(technicalrecorder=user).order_by('-date')  
    
     Maintenance = user.maintenance_set.all() 

     myFilter = MaintenanceFilter(request.GET, queryset=Maintenance)
     Tasks = myFilter.qs 

     data = {
         'Tasks':Tasks,
         'user':user,
        
         'Maintenance':Maintenance
        }
     pdf = render_to_pdf('task/page.html',data)
     return HttpResponse(pdf, content_type='application/pdf') 
     
   
       