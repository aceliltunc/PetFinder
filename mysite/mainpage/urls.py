from django.urls import path
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('pet/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pet/report/', views.pet_report, name='pet_report'),
    path('pet/<int:pk>/edit/', views.pet_update, name='pet_update'),
    path('pet/<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    path('search/', views.pet_search, name='pet_search'),
    path('import/', views.import_pets, name='import_pets'),
    path('export/', views.export_pets, name='export_pets'),
    path('pets/<int:pet_id>/report/', views.report_pet_sighting, name='report_pet_sighting'),



]
