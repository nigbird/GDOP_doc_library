from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Document, UploadFolder
from django.views.generic.edit import FormView
from .forms import FileFieldForm
import os
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.files.uploadhandler import MemoryFileUploadHandler, TemporaryFileUploadHandler


class UploadFolderView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'doc_library/upload_folder.html')

    def post(self, request, *args, **kwargs):
        folder_name = request.POST.get('folder_name', 'default_folder')
        folder, created = UploadFolder.objects.get_or_create(name=folder_name)
        
        for file in request.FILES.getlist('file_field'):
            relative_path = os.path.join(folder_name, file.name)
            file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            Document.objects.create(title=file.name, file=file, folder=folder, owner=request.user)

        return HttpResponse('Folder uploaded successfully')


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "doc_library/upload_document.html"  # Ensure the correct path
    success_url = "/documents/"

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            Document.objects.create(title=f.name, file=f, owner=self.request.user)
        return super().form_valid(form)

def home(request):
    return render(request, 'doc_library/home.html')

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