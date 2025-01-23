from django.contrib import admin
from .models import Document,UploadFolder,Category

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at', 'owner', 'folder', 'category')
    search_fields = ('title', 'owner__username','folder__name', 'category__name')
admin.site.register(UploadFolder)
admin.site.register(Category)
