from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from projet.permissions import CustomDjangoModelPermissions
from setting.models import Tache


from .models import (
    EstExecuteeAction,
    EstExecuteeFCPDR,
    EstExecuteeFCPTDD,
    EstExecuteeGCAUTRES,
    EstExecuteeGCSUB,
    EstExecuteeModeGestion,
    EstExecuteeOperationFDCDR,
    EstExecuteeSur,
    EstProgramme,
    Operation,
    Consommation,
    Groupe,
    PieceJointeConsommation,
)
from .serializers import (
    EstExecuteeActionSerializer,
    EstExecuteeFCPDRSerializer,
    EstExecuteeFCPTDDSerializer,
    EstExecuteeGCAUTRESSerializer,
    EstExecuteeGCSUBSerializer,
    EstExecuteeModeGestionSerializer,
    EstExecuteeOperationFDCDRSerializer,
    EstExecuteeSurSerializer,
    EstProgrammeSerializer,
    GroupeExecutionSerializer,
    OperationSerializer,
    ConsommationSerializer,
    PieceJointeConsommationSerializer,
)
from .filters import (
    ConsommationFilter,
    EstExecuteeGCSUBFilter,
    EstExecuteeGCAutresFilter,
    EstExecuteeOperationFCPFilter,
    GroupeFilter,
    OperationFilter,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Un ModelViewSet de base qui surcharge la méthode destroy pour
    retourner l'ID de l'élément supprimé dans la réponse.
    """

    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        resource_id = instance.id
        self.perform_destroy(instance)
        return Response(
            data={"message": "Deleted successfully", "deleted_id": resource_id},
        )

    def perform_destroy(self, instance):
        """
        Cette méthode exécute la suppression de l'instance.
        Elle est appelée dans `destroy()`.
        """
        instance.delete()


class EstExecuteeActionViewSet(BaseModelViewSet):
    queryset = EstExecuteeAction.objects.all()
    serializer_class = EstExecuteeActionSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeAction.objects.all().order_by("-id")


class EstExecuteeFCPDRViewSet(BaseModelViewSet):
    queryset = EstExecuteeFCPDR.objects.all()
    serializer_class = EstExecuteeFCPDRSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeFCPDR.objects.all().order_by("-id")


class EstExecuteeFCPTDDViewSet(BaseModelViewSet):
    queryset = EstExecuteeFCPTDD.objects.all()
    serializer_class = EstExecuteeFCPTDDSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeFCPTDD.objects.all().order_by("-id")


class EstExecuteeGCAUTRESViewSet(BaseModelViewSet):
    queryset = EstExecuteeGCAUTRES.objects.all()
    serializer_class = EstExecuteeGCAUTRESSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstExecuteeGCAutresFilter

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeGCAUTRES.objects.all().order_by("-id")


class EstExecuteeGCSUBViewSet(BaseModelViewSet):
    queryset = EstExecuteeGCSUB.objects.all()
    serializer_class = EstExecuteeGCSUBSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstExecuteeGCSUBFilter

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeGCSUB.objects.all().order_by("-id")


class EstExecuteeModeGestionViewSet(BaseModelViewSet):
    queryset = EstExecuteeModeGestion.objects.all()
    serializer_class = EstExecuteeModeGestionSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeModeGestion.objects.all().order_by("-id")


class EstExecuteeOperationFDCDRViewSet(BaseModelViewSet):
    queryset = EstExecuteeOperationFDCDR.objects.all()
    serializer_class = EstExecuteeOperationFDCDRSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EstExecuteeOperationFCPFilter

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeOperationFDCDR.objects.all().order_by("-id")


class EstExecuteeSurViewSet(BaseModelViewSet):
    queryset = EstExecuteeSur.objects.all()
    serializer_class = EstExecuteeSurSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstExecuteeSur.objects.all().order_by("-id")


class EstProgrammeViewSet(BaseModelViewSet):
    queryset = EstProgramme.objects.all()
    serializer_class = EstProgrammeSerializer

    def get_queryset(self):
        # Surcharge de get_queryset pour trier par date de création
        return EstProgramme.objects.all().order_by("-id")


from rest_framework.parsers import FormParser


class PieceJointeConsommationViewSet(BaseModelViewSet):
    queryset = PieceJointeConsommation.objects.all()
    serializer_class = PieceJointeConsommationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


class OperationViewSet(BaseModelViewSet):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    filterset_class = OperationFilter


class ConsommationViewSet(BaseModelViewSet):
    queryset = Consommation.objects.all()
    serializer_class = ConsommationSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    filterset_class = ConsommationFilter


class GroupeViewSet(BaseModelViewSet):
    queryset = Groupe.objects.all()
    serializer_class = GroupeExecutionSerializer
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    filterset_class = GroupeFilter


from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from setting.serializers import UploadSerializer

from setting.imports import import_excel_file


class ExcelImportViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Importer un fichier Excel pour la gestion du suivi de l'execution",
        operation_description="Cette vue permet de téléverser un fichier Excel pour l'importation des données BIP. Le fichier doit être au format Excel.",
        manual_parameters=[
            openapi.Parameter(
                "file_uploaded",
                openapi.IN_FORM,
                description="Le fichier Excel à importer",
                type=openapi.TYPE_FILE,
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Le fichier a été importé avec succès",
                examples={
                    "application/json": {"message": "Fichier Excel importé avec succès"}
                },
            ),
            400: openapi.Response(
                description="Aucun fichier fourni",
                examples={"application/json": {"error": "Aucun fichier fourni"}},
            ),
        },
    )
    @action(detail=False, methods=["post"], url_path="execution")
    def import_excel(self, request):
        if "file_uploaded" not in request.FILES:
            return Response(
                {"error": "Aucun fichier fourni"}, status=status.HTTP_400_BAD_REQUEST
            )
        excel_file = request.FILES["file_uploaded"]
        file_path = default_storage.save(f"media/temp/{excel_file.name}", excel_file)

        try:
            # Importer le fichier Excel
            import_excel_file(file_path)
            return Response(
                {"message": "Fichier Excel importé avec succès"},
                status=status.HTTP_200_OK,
            )
        finally:
            # Supprimer le fichier après traitement
            print("import reussi")


import io
from django.http import FileResponse
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Tache, Operation, Groupe, Consommation  # Vérifie bien l'emplacement


@api_view(["GET"])
@permission_classes([AllowAny])
def Annexe1View(request):
    """
    Vue Django REST Framework qui génère et renvoie le PDF en téléchargement.
    """
    return generate_table_1_pdf_response(request)


def generate_table_1_pdf_response(request):
    """
    Construit et renvoie le PDF en tant que FileResponse (pour téléchargement).
    """
    pdf_content = generate_table_1_pdf()  # Appelle la fonction qui construit le PDF
    response = FileResponse(io.BytesIO(pdf_content), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'
    return response


def generate_table_1_pdf():
    """
    Génère un PDF contenant un tableau qui reprend :
      - La Tache (en tant que 'Structure')
      - Le 'Volet dépenses courantes' (en dur)
      - Les Groupes associés à la Tache
      - Les Opérations rattachées au Groupe
      - Quelques colonnes pour Montant, Consommation, etc.
    Retourne un buffer PDF (en bytes).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Styles
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_header = styles["Heading4"]
    style_title = styles["Title"]
    style_normal.alignment = 1
    style_header.alignment = 1

    # En-tête du tableau
    table_data = [
        [
            Paragraph("Structures", style_header),
            Paragraph("Mode d'exécution", style_header),
            Paragraph("", style_header),
            Paragraph("Détails des opérations<br/>par rubriques", style_header),
            Paragraph("Montants", style_header),
            Paragraph("Consommation", style_header),
            Paragraph("Taux d'exécution<br/>Physique", style_header),
            Paragraph("Taux d'exécution<br/>Financier", style_header),
            Paragraph(
                "Procédure de contractualisation<br/>(en cours / mode de passation)",
                style_header,
            ),
            Paragraph("Difficultés / Observations", style_header),
        ]
    ]

    # Liste pour stocker les commandes SPAN pour les fusions
    stylesCustom = []

    # Index de la ligne courante (commence après l'en-tête)
    row_index = 1

    # Récupérer les tâches
    taches = Tache.objects.filter(type_execution="FCPDR").order_by("id")

    for tache in taches:
        # Index de début pour la tâche
        tache_start_row = row_index
        montant_tache = 0
        conso_tache = 0
        taux_physique_tache_tab = []
        taux_financier_tache_tab = []

        # Groupes distincts liés aux opérations de cette tâche
        groupes = Groupe.objects.filter(operation__tache=tache).distinct()

        for i, groupe in enumerate(groupes):
            # Index de début pour le groupe
            groupe_start_row = row_index

            # Opérations pour ce groupe et cette tâche
            operations = Operation.objects.filter(tache=tache, groupe=groupe)
            montant = 0
            total_conso = 0
            taux_physique_tab = []
            taux_financier_tab = []

            for operation in operations:
                consommations = Consommation.objects.filter(
                    operation=operation
                ).order_by("-id")
                total_consommation = sum(c.montant_engage or 0 for c in consommations)
                total_conso += total_consommation

                # Taux d'exécution physique
                taux_physique = (
                    consommations[0].pourcentage_exec_physique if consommations else 0
                )
                taux_physique_tab.append(taux_physique)

                # Taux d'exécution financier
                montant_op = operation.montant or 0
                montant += montant_op
                taux_financier = (
                    (total_consommation / montant_op * 100) if montant_op != 0 else 0
                )
                taux_financier_tab.append(taux_financier)

                # Ajouter la ligne pour l'opération
                table_data.append(
                    [
                        Paragraph(tache.title_fr or "", style_normal),  # Structure
                        Paragraph(
                            "Volet dépenses courante", style_normal
                        ),  # Valeur en dur
                        Paragraph(groupe.title_fr or "", style_normal),  # Groupe
                        Paragraph(operation.title_fr or "", style_normal),  # Opération
                        str(montant_op),
                        str(total_consommation),
                        f"{round(taux_physique, 2)}%",
                        f"{round(taux_financier, 2)}%",
                        (
                            Paragraph(
                                consommations[0].situation_contract or "", style_normal
                            )
                            if consommations
                            else ""
                        ),
                        (
                            Paragraph(consommations[0].observations or "", style_normal)
                            if consommations
                            else ""
                        ),
                    ]
                )
                row_index += 1

            # Ajouter la ligne "SOUS TOTAL"
            table_data.append(
                [
                    Paragraph(tache.title_fr or "", style_normal),  # Structure
                    Paragraph("Volet dépenses courante", style_normal),  # Valeur en dur
                    Paragraph(groupe.title_fr or "", style_normal),  # Groupe
                    Paragraph(f"SOUS TOTAL {i+1}", style_header),
                    Paragraph(f"{montant}", style_header),
                    str(total_conso),
                    f"{round(sum(taux_physique_tab) / len(taux_physique_tab), 2) if taux_physique_tab else 0}%",
                    f"{round(sum(taux_financier_tab) / len(taux_financier_tab), 2) if taux_financier_tab else 0}%",
                    "",
                    "",
                ]
            )
            row_index += 1
            montant_tache += montant
            conso_tache += total_conso
            taux_physique_tache_tab.append(
                round(sum(taux_physique_tab) / len(taux_physique_tab), 2)
            )
            taux_financier_tache_tab.append(
                round(sum(taux_financier_tab) / len(taux_financier_tab), 2)
            )

            # Ajouter la fusion pour le groupe (colonne 2) si au moins une opération existe
            if len(operations) > 2:
                stylesCustom.append(("SPAN", (2, groupe_start_row), (2, row_index - 1)))

        if groupes:
            table_data.append(
                [
                    Paragraph(
                        f"Total ({tache.title_fr})" or "", style_header
                    ),  # Structure
                    "",
                    "",
                    "",
                    Paragraph(f"{montant_tache}", style_header),
                    Paragraph(str(conso_tache), style_header),
                    Paragraph(
                        f"{round(sum(taux_physique_tache_tab) / len(taux_physique_tache_tab), 2) if taux_physique_tache_tab else 0}%",
                        style_header,
                    ),
                    Paragraph(
                        f"{round(sum(taux_financier_tache_tab) / len(taux_financier_tache_tab), 2) if taux_financier_tache_tab else 0}%",
                        style_header,
                    ),
                    "",
                    "",
                ]
            )
            row_index += 1

        # Ajouter la fusion pour la tâche (colonne 0) si des lignes ont été ajoutées
        if (row_index - tache_start_row) > 0:
            stylesCustom.append(("SPAN", (0, tache_start_row), (0, row_index - 2)))
            stylesCustom.append(("SPAN", (1, tache_start_row), (1, row_index - 2)))
            stylesCustom.append(("SPAN", (0, row_index - 1), (3, row_index - 1)))
            stylesCustom.append(
                (
                    "BACKGROUND",
                    (0, row_index - 1),
                    (-1, row_index - 1),
                    colors.lightgrey,
                )
            )

    # Création du tableau
    table = Table(table_data, colWidths=[80, 60, 80, 100, 80, 70, 70, 100, 100],repeatRows=1)

    # Appliquer les styles, y compris les fusions
    print(stylesCustom)
    stylesCustom = [s for s in stylesCustom if s[0] != "SPAN"]

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("SPAN", (1, 0), (2, 0)),  # Fusionner les colonnes 1 et 2
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
            + stylesCustom  # Ajouter les commandes de fusion
        )
    )
    title = Paragraph("SITUATION DES FONDS DE CONTREPARTIE", style_title)
    spacer = Spacer(1, 12)
    # Construire le PDF
    doc.build([title, spacer, table])

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


@api_view(["GET"])
@permission_classes([AllowAny])
def Annexe2View(request):
    """
    Vue Django REST Framework qui génère et renvoie le PDF en téléchargement.
    """
    return generate_table_2_pdf_response(request)


def generate_table_2_pdf_response(request):
    """
    Construit et renvoie le PDF en tant que FileResponse (pour téléchargement).
    """
    pdf_content = generate_table_2_pdf()  # Appelle la fonction qui construit le PDF
    response = FileResponse(io.BytesIO(pdf_content), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'
    return response


def generate_table_2_pdf():
    """
    Génère un PDF contenant un tableau qui reprend :
      - La Tache (en tant que 'Structure')
      - Le 'Volet dépenses courantes' (en dur)
      - Les Groupes associés à la Tache
      - Les Opérations rattachées au Groupe
      - Quelques colonnes pour Montant, Consommation, etc.
    Retourne un buffer PDF (en bytes).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    # Styles
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_header = styles["Heading4"]
    style_title = styles["Title"]
    style_normal.alignment = 1
    style_header.alignment = 1

    # En-tête du tableau
    table_data = [
        [
            Paragraph("Structures", style_header),
            Paragraph("Mode d'exécution", style_header),
            Paragraph("Détails des opérations<br/>par rubriques", style_header),
            Paragraph("Montants", style_header),
            Paragraph("Consommation", style_header),
            Paragraph("Taux d'exécution<br/>Physique", style_header),
            Paragraph("Taux d'exécution<br/>Financier", style_header),
            Paragraph(
                "Procédure de contractualisation<br/>(en cours / mode de passation)",
                style_header,
            ),
            Paragraph("Difficultés / Observations", style_header),
        ]
    ]

    # Liste pour stocker les commandes SPAN pour les fusions
    stylesCustom = []

    # Index de la ligne courante (commence après l'en-tête)
    row_index = 1

    # Récupérer les tâches
    taches = Tache.objects.filter(type_execution="SUBV").order_by("id")

    for tache in taches:
        # Index de début pour la tâche
        tache_start_row = row_index
        montant_tache = 0
        conso_tache = 0
        taux_physique_tache_tab = []
        taux_financier_tache_tab = []

        # Groupes distincts liés aux opérations de cette tâche
        groupes = Groupe.objects.filter(operation__tache=tache).distinct()

        for i, groupe in enumerate(groupes):
            # Index de début pour le groupe
            groupe_start_row = row_index

            # Opérations pour ce groupe et cette tâche
            operations = Operation.objects.filter(tache=tache, groupe=groupe)
            montant = 0
            total_conso = 0
            taux_physique_tab = []
            taux_financier_tab = []

            for operation in operations:
                consommations = Consommation.objects.filter(
                    operation=operation
                ).order_by("-id")
                total_consommation = sum(c.montant_engage or 0 for c in consommations)
                total_conso += total_consommation

                # Taux d'exécution physique
                taux_physique = (
                    consommations[0].pourcentage_exec_physique if consommations else 0
                )
                taux_physique_tab.append(taux_physique)

                # Taux d'exécution financier
                montant_op = operation.montant or 0
                montant += montant_op
                taux_financier = (
                    (total_consommation / montant_op * 100) if montant_op != 0 else 0
                )
                taux_financier_tab.append(taux_financier)

                # Ajouter la ligne pour l'opération
                table_data.append(
                    [
                        Paragraph(tache.title_fr or "", style_normal),  # Structure
                        Paragraph(groupe.title_fr or "", style_normal),  # Groupe
                        Paragraph(operation.title_fr or "", style_normal),  # Opération
                        str(montant_op),
                        str(total_consommation),
                        f"{round(taux_physique, 2)}%",
                        f"{round(taux_financier, 2)}%",
                        (
                            Paragraph(
                                consommations[0].situation_contract or "", style_normal
                            )
                            if consommations
                            else ""
                        ),
                        (
                            Paragraph(consommations[0].observations or "", style_normal)
                            if consommations
                            else ""
                        ),
                    ]
                )
                row_index += 1

            # Ajouter la ligne "SOUS TOTAL"
            table_data.append(
                [
                    Paragraph(tache.title_fr or "", style_normal),  # Structure
                    Paragraph(groupe.title_fr or "", style_normal),  # Groupe
                    Paragraph(f"SOUS TOTAL {i+1}", style_header),
                    Paragraph(f"{montant}", style_header),
                    str(total_conso),
                    f"{round(sum(taux_physique_tab) / len(taux_physique_tab), 2) if taux_physique_tab else 0}%",
                    f"{round(sum(taux_financier_tab) / len(taux_financier_tab), 2) if taux_financier_tab else 0}%",
                    "",
                    "",
                ]
            )
            row_index += 1
            montant_tache += montant
            conso_tache += total_conso
            taux_physique_tache_tab.append(
                round(sum(taux_physique_tab) / len(taux_physique_tab), 2)
            )
            taux_financier_tache_tab.append(
                round(sum(taux_financier_tab) / len(taux_financier_tab), 2)
            )

            # Ajouter la fusion pour le groupe (colonne 2) si au moins une opération existe
            if operations:
                stylesCustom.append(("SPAN", (2, groupe_start_row), (2, row_index - 1)))

        if groupes:
            table_data.append(
                [
                    Paragraph(
                        f"Total ({tache.title_fr})" or "", style_header
                    ),  # Structure
                    "",
                    "",
                    Paragraph(f"{montant_tache}", style_header),
                    Paragraph(str(conso_tache), style_header),
                    Paragraph(
                        f"{round(sum(taux_physique_tache_tab) / len(taux_physique_tache_tab), 2) if taux_physique_tache_tab else 0}%",
                        style_header,
                    ),
                    Paragraph(
                        f"{round(sum(taux_financier_tache_tab) / len(taux_financier_tache_tab), 2) if taux_financier_tache_tab else 0}%",
                        style_header,
                    ),
                    "",
                    "",
                ]
            )
            row_index += 1

        # Ajouter la fusion pour la tâche (colonne 0) si des lignes ont été ajoutées
        if row_index > tache_start_row:
            stylesCustom.append(("SPAN", (0, tache_start_row), (0, row_index - 2)))
            stylesCustom.append(("SPAN", (0, row_index - 1), (2, row_index - 1)))
            stylesCustom.append(
                (
                    "BACKGROUND",
                    (0, row_index - 1),
                    (-1, row_index - 1),
                    colors.lightgrey,
                )
            )

    # Création du tableau
    table = Table(table_data, colWidths=[80, 80, 100, 80, 70, 70, 100, 100])

    # Appliquer les styles, y compris les fusions
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
            + stylesCustom  # Ajouter les commandes de fusion
        )
    )

    title = Paragraph("EXECUTION DES TRANSFERTS EN INVESTISSEMENT", style_title)
    spacer = Spacer(1, 12)
    # Construire le PDF
    doc.build([title, spacer, table])

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle


class VerticalParagraph(Paragraph):
    """Paragraphe imprimé verticalement (rotation de 90 degrés dans le sens antihoraire)"""

    def __init__(self, text, style):
        super().__init__(text, style)
        self.horizontal_position = -self.style.leading

    def draw(self):
        """Dessiner le texte avec une rotation"""
        canvas = self.canv
        canvas.rotate(90)  # Rotation de 90 degrés
        canvas.translate(1, self.horizontal_position)
        super().draw()

    def wrap(self, available_width, _):
        """Ajuster les dimensions pour le texte vertical"""
        string_width = self.canv.stringWidth(
            self.getPlainText(), self.style.fontName, self.style.fontSize
        )
        self.horizontal_position = -(available_width + self.style.leading) / 2
        height, _ = super().wrap(
            availWidth=1 + string_width, availHeight=available_width
        )
        return self.style.leading, height


from collections import defaultdict
from contractualisation.models import Etape, EtapeContractualisation


@api_view(["GET"])
@permission_classes([AllowAny])
def Annexe3View(request):
    """
    Vue Django REST Framework qui génère et renvoie le PDF en téléchargement.
    """
    return generate_table_3_pdf_response(request)


def generate_table_3_pdf_response(request):
    """
    Construit et renvoie le PDF en tant que FileResponse (pour téléchargement).
    """
    pdf_content = generate_table_3_pdf()  # Appelle la fonction qui construit le PDF
    response = FileResponse(io.BytesIO(pdf_content), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'
    return response


from reportlab.pdfgen import canvas


def generate_table_3_pdf():
    """
    Génère un PDF contenant un tableau avec les tâches, étapes, et données financières.
    Retourne un buffer PDF (en bytes).
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    # Styles
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_header = styles["Heading4"]
    style_normal.alignment = 1
    style_header.alignment = 1
    # Récupérer les tâches par type
    grouped_data = defaultdict(list)
    for tache in Tache.objects.all():
        grouped_data[tache.type].append(tache)
    tables1 = []
    tables2 = []

    for type in grouped_data:
        if not type:
            continue
        list_etapes = Etape.objects.filter(type=type).order_by("rang")

        if len(list_etapes) > 10:
            c.setPageSize(landscape(A3))
            page_width, page_height = landscape(A3)
        else:
            c.setPageSize(landscape(A4))
            page_width, page_height = landscape(A4)

        # Créer le titre
        title_text = f"MISE EN ŒUVRE DU PLAN DE PASSATION DES MARCHES {type}"
        title = Paragraph(title_text, style_header)
        title.wrapOn(c, page_width - 200, 50)  # Ajuster la largeur disponible
        title.drawOn(c, 100, page_height - 100)  # Positionner en haut

        # En-têtes principaux
        headers = [
            Paragraph("Désignation et localisation du projet", style_header),
            *[
                item
                for etape in list_etapes
                for item in [Paragraph(etape.title, style_header), "", ""]
            ],
            Paragraph("Montant (FCFA) du Contrat", style_header),
            "",
            "",
            "",
            Paragraph("Observations", style_header),
        ]
        sub_headers = [
            "",
            *[
                item
                for _ in list_etapes
                for item in [
                    VerticalParagraph("Date Prévue", style_header),
                    VerticalParagraph("Date effective", style_header),
                    VerticalParagraph("Écart (jours)", style_header),
                ]
            ],
            VerticalParagraph("Prévisionnel", style_header),
            VerticalParagraph("Réel", style_header),
            VerticalParagraph("Écart", style_header),
            VerticalParagraph("Taux de consommation", style_header),
            "",
        ]

        # definition du style

        style_columns = [
            ("SPAN", (0, 0), (0, 1)),
            ("SPAN", (-1, 0), (-1, 1)),
            ("SPAN", (-5, 0), (-2, 0)),
        ]
        for i, _ in enumerate(list_etapes):
            style_columns.append(("SPAN", (1 + (i * 3), 0), (3 + (i * 3), 0)))

        # Initialiser les données du tableau
        table_data = [headers, sub_headers]

        # Ajouter les lignes de données pour chaque tâche
        for tache in grouped_data[type]:
            row_data = [Paragraph(tache.title_fr, style=style_normal)]
            montantEtape = None
            etapes_contractualisations = EtapeContractualisation.objects.filter(
                tache=tache
            )

            for etape in list_etapes:
                contract = etapes_contractualisations.filter(etape=etape)
                if contract.exists():
                    contract = contract[0]
                    if contract.montant_prevu and contract.montant_reel:
                        montantEtape = contract
                    # Date prévue
                    row_data.append(
                        VerticalParagraph(
                            (
                                contract.date_prevue.strftime("%d/%m/%Y")
                                if contract.date_prevue
                                else ""
                            ),
                            style=style_normal,
                        )
                    )
                    # Date effective ou saisine
                    if contract.date_saisine:
                        row_data.append(
                            VerticalParagraph(
                                contract.date_saisine.strftime("%d/%m/%Y"),
                                style=style_normal,
                            )
                        )
                        row_data.append(
                            VerticalParagraph(
                                (
                                    f"{(contract.date_saisine - contract.date_prevue).days} J"
                                    if contract.date_prevue
                                    else ""
                                ),
                                style=style_normal,
                            )
                        )
                    else:
                        row_data.append(
                            VerticalParagraph(
                                (
                                    contract.date_effective.strftime("%d/%m/%Y")
                                    if contract.date_effective
                                    else ""
                                ),
                                style=style_normal,
                            )
                        )
                        row_data.append(
                            VerticalParagraph(
                                (
                                    f"{(contract.date_effective - contract.date_prevue).days} J"
                                    if contract.date_effective and contract.date_prevue
                                    else ""
                                ),
                                style=style_normal,
                            )
                        )
                else:
                    # Si pas de contrat, ajouter des cellules vides
                    row_data.extend(["", "", ""])

            # Ajouter les colonnes de montant
            row_data.extend(
                [
                    VerticalParagraph(
                        f"{montantEtape.montant_prevu}" if montantEtape else "",
                        style=style_normal,
                    ),
                    VerticalParagraph(
                        f"{montantEtape.montant_reel}" if montantEtape else "",
                        style=style_normal,
                    ),
                    VerticalParagraph(
                        f"{montantEtape.ecart_montant}" if montantEtape else "",
                        style=style_normal,
                    ),
                    VerticalParagraph(
                        f"{montantEtape.taux_consomation}" if montantEtape else "",
                        style=style_normal,
                    ),
                    VerticalParagraph("", style=style_normal),
                ]
            )

            # Ajouter la ligne au tableau
            table_data.append(row_data)

        # Créer le tableau
        col_widths = [80] + [20] * (len(table_data[0]) - 2) + [80]
        table = Table(table_data, colWidths=col_widths)  # Ajuster les largeurs
        table_width = sum(col_widths)

        # Appliquer les styles
        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 1),
                        colors.lightgrey,
                    ),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
                + style_columns
            )
        )
        x = (page_width - table_width) / 2
        y = 50
        table.wrapOn(c, page_width, page_height)
        table.drawOn(c, x, y)
        c.showPage()

    # Générer le document
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
