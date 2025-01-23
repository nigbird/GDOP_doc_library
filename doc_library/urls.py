# filepath: /c:/Users/hp/myproject/doc_library/urls.py
from django.urls import path
from . import views
from .views import HomePageView, CategoryManagementView, UploadFolderView, CategoryDetailView, fetch_files

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),  # Use HomePageView here
    path('manage-categories/', CategoryManagementView.as_view(), name='manage_categories'),
    path('categories/<int:category_id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('documents/', views.document_list, name='document_list'),
    path('upload_folder/', views.UploadFolderView.as_view(), name='upload_folder'),
    path('upload/', views.FileFieldFormView.as_view(), name='upload_document'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
    path('delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('folders/<int:folder_id>/files/', fetch_files, name='fetch_files'),
]

