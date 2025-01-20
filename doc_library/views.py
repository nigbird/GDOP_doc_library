from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Document
from django.views.generic.edit import FormView
from .forms import FileFieldForm


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