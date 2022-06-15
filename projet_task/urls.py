"""etechnics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.conf.urls import url
from django.urls import path,include
from projet_task import views
# Configuration des medias 
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('maintenance.urls')),
    path('',include('comptes.urls')),
    path('maintenance_experience_logbook_pdf/<int:id>',views.printPdf,name="printtasks"),
    path('maintenance_experience_logbook_pdf_bis/<int:id>',views.printPdf_bis,name="printPdf_bis")
    

]

# A ne pas supprimer | c'est pour l'affichage des photos 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

