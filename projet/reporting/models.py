from django.db import models
from django.contrib.auth.models import User
import os

def document_image_path(instance, filename):
    """Generate upload path for document images"""
    return f'documents/{instance.document.id}/images/{filename}'

class ConcertationDocument(models.Model):
    DOCUMENT_TYPES = [
        ('bip_followup', 'Cadre de Concertation BIP'),
        ('other', 'Autre'),
    ]
    
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, default='bip_followup')
    month = models.CharField(max_length=7)  # Format "YYYY-MM"
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Métadonnées du document
    total_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    physical_execution_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Ajout pour le sommaire automatique
    auto_generate_toc = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['document_type', 'month', 'year']
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.title} - {self.month}"
    
    def generate_table_of_contents(self):
        """Génère automatiquement le sommaire basé sur les sections actives"""
        active_sections = self.sections.filter(is_active=True).exclude(
            section_type__in=['cover', 'summary']
        ).order_by('order')
        
        toc_html = '<div class="table-of-contents"><h3>Sommaire</h3><ul>'
        for section in active_sections:
            toc_html += f'<li><a href="#{section.section_type}">{section.title}</a></li>'
        toc_html += '</ul></div>'
        
        return toc_html

class DocumentSection(models.Model):
    SECTION_TYPES = [
        ('cover', 'Page de couverture'),
        ('summary', 'Sommaire'),
        ('analytical_summary', 'Résumé analytique'),
        ('introduction', 'Introduction'),
        ('recommendations', 'Recommandations'),
        ('budget_presentation', 'Présentation du budget'),
        ('execution_status', 'État d\'exécution'),
        ('annexes', 'Annexes'),
        ('custom', 'Section personnalisée'),
    ]
    
    document = models.ForeignKey(ConcertationDocument, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_auto_generated = models.BooleanField(default=False)  # Pour le sommaire
    last_saved = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['document', 'section_type']
    
    def __str__(self):
        return f"{self.document.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Auto-générer le sommaire si c'est une section sommaire
        if self.section_type == 'summary' and self.document.auto_generate_toc:
            self.content = self.document.generate_table_of_contents()
            self.is_auto_generated = True
        super().save(*args, **kwargs)

class SectionImage(models.Model):
    section = models.ForeignKey('DocumentSection', on_delete=models.CASCADE, related_name='images')
    document = models.ForeignKey('ConcertationDocument', on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    original_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    file_size = models.IntegerField()
    mime_type = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reporting_section_images'
    
    def __str__(self):
        return f"{self.original_name} (Section {self.section_id})"

class BudgetComponent(models.Model):
    """Pour stocker les données des tableaux budgétaires"""
    document = models.ForeignKey(ConcertationDocument, on_delete=models.CASCADE, related_name='budget_components')
    component_name = models.CharField(max_length=100)
    provision = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    physical_rate_june = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    physical_rate_july = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    engagement_rate_june = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    engagement_rate_july = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    class Meta:
        ordering = ['-provision']
    
    def __str__(self):
        return f"{self.component_name} - {self.document.month}"