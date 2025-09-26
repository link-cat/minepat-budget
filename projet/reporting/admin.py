from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import ConcertationDocument, DocumentSection, BudgetComponent

@admin.register(ConcertationDocument)
class ConcertationDocumentAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'document_type', 'month', 'year', 'created_at', 'updated_at')
    list_filter = ('document_type', 'month', 'year')
    search_fields = ('title',)
    date_hierarchy = 'created_at'
    ordering = ('-year', '-month')
    readonly_fields = ('created_at', 'updated_at')  

@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = ('document', 'section_type', 'title', 'order', 'is_active')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title', 'document__title')
    ordering = ('document', 'order')
    readonly_fields = ()

@admin.register(BudgetComponent)
class BudgetComponentAdmin(admin.ModelAdmin):
    list_display = ('document', 'component_name', 'provision', 'physical_rate_june', 'physical_rate_july', 'engagement_rate_june', 'engagement_rate_july')
    list_filter = ('document__document_type',)
    search_fields = ('component_name', 'document__title')
    ordering = ('document', 'component_name')
    readonly_fields = ()
    