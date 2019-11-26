from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'forge'

urlpatterns = [
    path('s/<slug:slug>/update/<uuid:pk>',
         views.StructureUpdate.as_view(), name='update_structure'),
    path('s/<slug:slug>/delete/<uuid:pk>',
         views.StructureDelete.as_view(), name='delete_structure'),
    path('s/<slug:slug>/preview/<uuid:pk>',
         views.preview_structure, name='preview_structure'),
    path('s/<slug:slug>/<uuid:pk>/',
         views.StructureDetails.as_view(), name='structure_details'),
    path('s/create/',
         views.StructureCreate.as_view(), name='create_structure'),

    path('s', RedirectView.as_view(pattern_name='forge:index')),

    path('d/<slug:slug>/create/<uuid:pk>',
         views.DataCreate.as_view(), name='create_data'),
    path('d/<slug:slug>/update/<uuid:pk>',
         views.DataUpdate.as_view(), name='update_data'),
    path('d/<slug:slug>/update/<str:action>/<uuid:pk>',
         views.DataUpdate.as_view(), name='amend_data'),
    path('d/<slug:slug>/delete/<uuid:pk>',
         views.DataDelete.as_view(), name='delete_data'),
    path('d/<slug:slug>/<uuid:pk>/',
         views.DataDetails.as_view(), name='data_details'),

    path('', views.StructureList.as_view(), name='index'),
]
