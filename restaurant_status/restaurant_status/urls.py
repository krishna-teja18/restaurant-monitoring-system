# from django.contrib import admin
# from django.urls import path, include
# from monitor import views


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('trigger_report/', views.trigger_report, name='trigger_report'),
#     path('get_report/<str:report_id>/', views.get_report, name='get_report'),
#     path('api-auth/', include('rest_framework.urls')),
# ]

# store_monitoring/urls.py

from django.contrib import admin
from django.urls import path
from monitor.views import trigger_report, get_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trigger_report/', trigger_report, name='trigger_report'),
    path('get_report/<str:report_id>/', get_report, name='get_report'),
]

