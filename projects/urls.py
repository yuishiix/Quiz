# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('request-quotation/', views.quotation_request, name='quotation_request'),
    path('load-materials/', views.load_materials, name='load_materials'),
    path('quotation/success/', views.quotation_success, name='quotation_success'),
    path('my-quotes/', views.list_of_my_quotes, name='homepage'),
    path('materials-and-elements/', views.all_project_materials_and_elements, name='all_project_materials_and_elements'),
    path('add-element/', views.add_project_element, name='add_project_element'),
    path('add-material/', views.add_material, name='add_material'),

]
