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
    path('chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:user_id>/get_new_messages/', views.get_new_messages, name='get_new_messages'),
    path('chat/', views.chat_list, name='chat_list'),
    path('chat/mark_read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read'),


    # Pet Yönetimi
    path('admin/', views.admin_views, name='admin_views'),
    path('admin/pets/', views.admin_pet_list_view, name='admin_pet_list'),
    path('admin/pets/edit/<int:pk>/', views.admin_pet_edit, name='admin_pet_edit'),
    path('admin/pets/delete/<int:pk>/', views.admin_pet_delete, name='admin_pet_delete'),
    path('admin/pets/add/', views.admin_pet_report, name='admin_pet_report'),
    # Tag Yönetimi
    path('admin/tags/', views.admin_tag_list, name='admin_tag_list'),
    path('admin/tags/add/', views.admin_tag_add, name='admin_tag_add'),
    path('admin/tags/edit/<int:pk>/', views.admin_tag_edit, name='admin_tag_edit'),
    path('admin/tags/delete/<int:pk>/', views.admin_tag_delete, name='admin_tag_delete'),

    # PetSighting Yönetimi
    path('admin/sightings/', views.admin_sighting_management, name='admin_sighting_management'),
    path('admin/sightings/add/', views.admin_sighting_add, name='admin_sighting_add'),
    path('admin/sightings/edit/<int:pk>/', views.admin_sighting_edit, name='admin_sighting_edit'),
    path('admin/sightings/delete/<int:pk>/', views.admin_sighting_delete, name='admin_sighting_delete'),

    # Message Yönetimi
    path('admin/messages/', views.admin_message_list, name='admin_message_list'),
    path('admin/messages/add/', views.admin_message_add, name='admin_message_add'),
    path('admin/messages/edit/<int:pk>/', views.admin_message_edit, name='admin_message_edit'),
    path('admin/messages/delete/<int:pk>/', views.admin_message_delete, name='admin_message_delete'),
    path('admin/messages/filtered/', views.admin_message_list_filtered, name='admin_message_list_filtered'),


]
