from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_home, name='home'),

    path('clients/', views.show_clients, name='clients'),
    path('clients/<str:pk>/client-dashboard/', views.show_client_dashboard, name='client-dashboard'),
    path('clients/<str:pk>/client-profile/', views.client_profile, name='client-profile'),
    path('clients/<str:pk>/registration-history/', views.remove_box, name='remove-box'),
    path('clients/<str:pk>/register-box/', views.register_box, name='register-box'),


    path('clients/<str:pk>/visitations/', views.visitations, name='visitations'),
    path('clients/<str:pk>/add-visitation/', views.add_visitation, name='add-visitation'),


    path('clients/register-client/', views.register_client, name='register-client'),
    path('clients/<str:pk>/confirm-delete/', views.confirm_delete, name='confirm-delete'),
    

    path('boxes/', views.show_boxes, name='boxes'),
    path('boxes/<str:pk>/box-history/', views.box_history, name='box-history')

]
