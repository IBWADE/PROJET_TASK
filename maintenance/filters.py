import django_filters
from django_filters import DateFilter

from .models import *

class MaintenanceFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte')
   # note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = maintenance
        fields = '__all__'
        exclude = ['date', 'location','actype','acregistration','typemaintenance','ata','operation','time','maintenanceref','remark','technicalrecorder']
