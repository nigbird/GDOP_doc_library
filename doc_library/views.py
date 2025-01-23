from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.uploadhandler import MemoryFileUploadHandler, TemporaryFileUploadHandler
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views import View
from .models import Document, UploadFolder, Category
from django.views.generic.edit import FormView
from .forms import FileFieldForm
from django.http import JsonResponse
import os
import json





class HomePageView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'doc_library/home.html', {'categories': categories})
from django.shortcuts import render, get_object_or_404


class CategoryDetailView(View):
    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        folders = category.folders.all()
        documents = category.documents.all()
        return render(request, 'doc_library/category_detail.html', {'category': category, 'folders': folders, 'documents': documents})


def admin_required(user):
    return user.is_staff

@method_decorator(user_passes_test(admin_required), name='dispatch')
class CategoryManagementView(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, 'doc_library/manage_categories.html', {'categories': categories})

    def post(self, request, *args, **kwargs):
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)
        return redirect('manage_categories')
        


class UploadFolderView(View):
    def get(self, request, *args, **kwargs):
        folders = UploadFolder.objects.all()
        categories = Category.objects.all()
        return render(request, 'doc_library/upload_folder.html', {'folders':folders, 'categories': categories})

    def post(self, request, *args, **kwargs):
        directories = json.loads(request.POST.get('directories', '{}'))
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id) if category_id else None
        folder_name = request.POST.get('folder_name', 'default_folder')
        folder, created = UploadFolder.objects.get_or_create(name=folder_name, category=category)
        for relative_path in set(directories.values()):
            folder_name = os.path.dirname(relative_path)
            if folder_name:
                UploadFolder.objects.get_or_create(name=folder_name, category=category)

        for file in request.FILES.getlist('file_field'):
            relative_path = os.path.join(folder_name, file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            Document.objects.create(title=file.name, file=file, folder=folder, owner=request.user, category=category)

        return HttpResponse('Folder uploaded successfully')



def fetch_files(request, folder_id):
    folder = get_object_or_404(UploadFolder, id=folder_id)
    files = Document.objects.filter(folder=folder).values('id', 'title', 'file')
    file_list = list(files)
    print(f"Files in folder {folder.name}: {file_list}") 
    return JsonResponse({'folder_name': folder.name, 'files': file_list})


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "doc_library/upload_document.html"  # Ensure the correct path
    success_url = "/documents/"

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            Document.objects.create(title=f.name, file=f, owner=self.request.user)
        return super().form_valid(form)


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'doc_library/document_list.html', {'documents': documents})

@login_required
def download_document(request, document_id):
    document = Document.objects.get(id=document_id)
    response = HttpResponse(document.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
    return response

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    file_path = document.file.path
    if os.path.exists(file_path):
        os.remove(file_path)
    document.delete()
    return redirect('document_list')