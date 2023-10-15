from django.contrib import admin
from django.urls import path, include
from rest.views import CompanyViewSet
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter() 
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('upload-csv/', views.upload_csv, name='upload-csv'),
    path('count_records/', views.count_records, name='count_records'),
    path('mean_salary/', views.mean_salary, name='mean_salary'),
    path('median_salary/', views.median_salary, name='median_salary'),
    path('percentile_25/', views.percentile_25, name='percentile_25'),
    path('percentile_75/', views.percentile_75, name='percentile_75'),
] 