from django.urls import path
from . import views

urlpatterns = [
    path('', views.Upload_employee, name='employee_file_upload'),
    path('csv/', views.handle_csv_upload, name='scv_file'),
]