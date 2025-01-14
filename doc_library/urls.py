# filepath: /c:/Users/hp/myproject/doc_library/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('documents/', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
]
