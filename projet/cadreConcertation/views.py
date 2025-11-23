from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML, CSS
from .models import Rapport
from .serializers import RapportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action

class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated]
   
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rapport = serializer.save()
        return Response(
          {"id": rapport.id, "message": "Rapport sauvegardé"},
          status=status.HTTP_201_CREATED
        )
    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(self, request, pk):
        try:
            rapport = Rapport.objects.get(pk=pk)
        except Rapport.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Contexte pour le template
        context = {
            'rapport': rapport,
            # On peut passer ici l'URL absolue pour charger les images statiques (logos)
            'base_url': request.build_absolute_uri('/') 
        }

        # 1. Rendu HTML
        html_string = render_to_string('rapports/template_master.html', context)

        # 2. Génération PDF avec WeasyPrint
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        
        # On force le CSS ici ou on l'inclut dans le HTML
        pdf_file = html.write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Rapport_{rapport.id}.pdf"'
        return response