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
from bs4 import BeautifulSoup
import re 

class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated]
    
    def _extract_toc_and_figures(self, rapport):
        """
        Extrait la table des matières (avec sous-sections H2) 
        et la liste des figures du rapport
        """
        sections = [
            {
                'id': 'resume',
                'title': 'Résumé Analytique',
                'content': rapport.resume_analytique
            },
            {
                'id': 'intro',
                'title': 'Introduction',
                'content': rapport.introduction
            },
            {
                'id': 'etat',
                'title': 'État de mise en œuvre des recommandations et résolutions du Cadre de Concertation',
                'content': rapport.etat_mise_en_oeuvre
            },
            {
                'id': 'presentation',
                'title': f'Présentation du Budget d\'Investissement Public {rapport.annee} du MINEPAT',
                'content': rapport.presentation_du_budget
            },
            {
                'id': 'situation',
                'title': f'Situation des composantes du BIP {rapport.annee} du MINEPAT',
                'content': rapport.situation
            },
            {
                'id': 'conclusion',
                'title': 'Conclusion',
                'content': rapport.conclusion
            },
        ]
        
        toc = []
        all_figures = []
        figure_counter = 1
        
        for section in sections:
            # Structure de base de la section
            section_toc = {
                'id': section['id'],
                'title': section['title'],
                'subsections': []
            }
            
            if section['content']:
                soup = BeautifulSoup(section['content'], 'html.parser')
                
                # 1. Extraire les H2 (sous-sections)
                h2_tags = soup.find_all('h2')
                for idx, h2 in enumerate(h2_tags):
                    h2_id = f"{section['id']}_h2_{idx}"
                    # Ajouter l'ID au H2 dans le contenu original
                    h2['id'] = h2_id
                    section_toc['subsections'].append({
                        'id': h2_id,
                        'title': h2.get_text(strip=True)
                    })
                
                # Mettre à jour le contenu avec les IDs ajoutés
                section['processed_content'] = str(soup)
                
                # 2. Extraire les figures (img avec légende)
                # Chercher tous les éléments <p> contenant "Figure" ou "figure"
                all_elements = soup.find_all(['p', 'img'])
                
                for i, elem in enumerate(all_elements):
                    if elem.name == 'p':
                        text = elem.get_text(strip=True)
                        # Vérifier si le paragraphe contient "Figure" (insensible à la casse)
                        if re.search(r'\bfigure\b', text, re.IGNORECASE):
                            # Chercher l'image suivante
                            next_elem = None
                            for j in range(i + 1, len(all_elements)):
                                if all_elements[j].name == 'img':
                                    next_elem = all_elements[j]
                                    break
                                elif all_elements[j].name == 'p' and all_elements[j].get_text(strip=True):
                                    # Si on trouve un autre paragraphe avec du texte, on arrête
                                    break
                            
                            if next_elem:
                                # Ajouter la figure
                                figure_id = f"figure_{figure_counter}"
                                next_elem['id'] = figure_id
                                all_figures.append({
                                    'id': figure_id,
                                    'number': figure_counter,
                                    'caption': text,
                                    'section': section['title']
                                })
                                figure_counter += 1
                
                # Mettre à jour le contenu final avec les IDs des figures
                section['processed_content'] = str(soup)
            else:
                section['processed_content'] = section['content']
            
            toc.append(section_toc)
        
        return {
            'toc': toc,
            'figures': all_figures,
            'sections': sections
        }
   
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
        # Extraire le sommaire et les figures
        extracted_data = self._extract_toc_and_figures(rapport)
            
            # Contexte pour le template
        context = {
            'rapport': rapport,
            'base_url': request.build_absolute_uri('/'),
            'toc': extracted_data['toc'],
            'figures': extracted_data['figures'],
            'sections': extracted_data['sections']
        }
            
        html_string = render_to_string('rapports/template_master.html', context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf_file = html.write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Rapport_{rapport.id}.pdf"'
        return response