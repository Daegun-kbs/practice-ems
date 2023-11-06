from django.urls import path
from . import views

app_name = 'ems'

urlpatterns = [
   path('main/', views.show_main, name='main'),
   path('redis/', views.show_redis, name='redis'),
   path('request_alarm/', views.request_alarm, name='request_alarm'),
   path('influx/', views.show_influx, name='influx'),
   path('update_dbtable_influx/', views.ajax_update_table_influx, name='ajax_update_table_influx'),
   path('export-data-sec/', views.export_data_to_csv_sec, name='export_data_sec'),
   path('maria/', views.show_maria, name='maria'),
   path('update_dbtable/', views.ajax_update_table, name='ajax_update_table'),
   path('export-data-min/', views.export_data_to_csv_min, name='export_data_min'),
   path('statistics/', views.show_statistics, name='statistics'),
   path('update_dbtable_chart/', views.ajax_update_table_chart, name='ajax_update_table_chart'),
   path('chart_data/', views.chart_data, name='chart_data'),
]