from rest_framework import serializers
from .models import ConcertationDocument, DocumentSection, BudgetComponent, SectionImage

class DocumentImageSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()
    
    class Meta:
        model = SectionImage
        fields = '__all__'

class DocumentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSection
        fields = ['id', 'section_type', 'title', 'content', 'order', 'is_active', 
                 'is_auto_generated', 'last_saved']
        read_only_fields = ['is_auto_generated', 'last_saved']
    
    def update(self, instance, validated_data):
        # Empêcher la modification du contenu des sections auto-générées
        if instance.is_auto_generated and 'content' in validated_data:
            validated_data.pop('content')
        return super().update(instance, validated_data)

class BudgetComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetComponent
        fields = '__all__'

class ConcertationDocumentSerializer(serializers.ModelSerializer):
    sections = DocumentSectionSerializer(many=True, read_only=True)
    images = DocumentImageSerializer(many=True, read_only=True)
    budget_components = BudgetComponentSerializer(many=True, read_only=True)
    
    class Meta:
        model = ConcertationDocument
        fields = ['id', 'title', 'document_type', 'month', 'year', 
                 'total_budget', 'physical_execution_rate', 'engagement_rate',
                 'auto_generate_toc', 'created_at', 'updated_at', 
                 'sections', 'images', 'budget_components']