from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Document
from .forms import DocumentForm

def home(request):
    return render(request, 'doc_library/home.html')

@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'doc_library/document_list.html', {'documents': documents})

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.owner = request.user  # Ensure the owner field is set
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'doc_library/upload_document.html', {'form': form})

@login_required
def download_document(request, document_id):
    document = Document.objects.get(id=document_id)
    response = HttpResponse(document.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
    return response