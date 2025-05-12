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
from datetime import datetime
from django.http import FileResponse
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    LongTable,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Tache, Operation, Groupe, Consommation  # Vérifie bien l'emplacement


def compute_page_breaks(table_data, colWidths, available_height):
    """
    Pour chaque ligne du tableau, calcule la hauteur (en prenant la hauteur maximale
    des cellules) et retourne un mapping (liste) indiquant le numéro de page auquel
    la ligne sera placée.
    """
    row_page_mapping = [[]]
    current_page = 0
    cumulative_height = 0
    available_height = available_height - 30  # Ajustement pour les marges
    tache = ""
    groupe = ""

    for index, row in enumerate(table_data):
        # Calcul de la hauteur de la ligne : prendre la hauteur max des cellules
        row_height = 0
        for i, cell in enumerate(row):
            if i == 0:
                if tache != cell.text:
                    print("cell", cell.text)
                    tache = cell.text
                else:
                    continue
            if i == 1:
                continue
            if i == 2:
                if groupe != cell.text:
                    groupe = cell.text
                else:
                    continue
            if hasattr(cell, "wrap"):
                # Utilisation d'une hauteur max arbitraire (assez grande)
                _, height = cell.wrap(colWidths[i], 10000)
                row_height = max(row_height, height + 16)
            else:
                # Si ce n'est pas un flowable, on peut définir une hauteur par défaut
                row_height = max(row_height, 15)

        # Déterminer si la ligne peut tenir sur la page actuelle
        if cumulative_height + row_height > available_height:
            # On passe à la page suivante
            current_page += 1
            if current_page == 1:
                available_height = available_height + 30
            row_page_mapping.append([])
            print(index)
            cumulative_height = row_height
        else:
            cumulative_height += row_height
        print("cumulative_height", cumulative_height)
        print("row_height", row_height)
        row_page_mapping[current_page].append(row)

    return row_page_mapping


def flatten_row_page_mapping(row_page_mapping):
    """
    Transforme le row_page_mapping (liste de listes) en un dictionnaire où la clé est
    l'indice global de la ligne et la valeur est le numéro de la page (0-indexé).
    """
    flat_map = {}
    global_index = 0
    for page_index, page_rows in enumerate(row_page_mapping):
        for _ in page_rows:
            flat_map[global_index] = page_index
            global_index += 1

    return flat_map


def apply_page_spans(flat_mapping, custom_styles):
    """
    Ajuste les spans contenus dans custom_styles en vérifiant que chaque span vertical ne
    déborde pas sur plusieurs pages. Si c'est le cas, le span est découpé pour chaque page.

    :param flat_mapping: dict associant indice de ligne global -> numéro de page (0-indexé)
    :param custom_styles: liste de tuples, par exemple: ("SPAN", (col_start, row_start), (col_end, row_end))
    :return: nouvelle liste de spans ajustée
    """
    adjusted_styles = []
    for style in custom_styles:
        if style[0] == "SPAN":
            (col_start, row_start), (col_end, row_end) = style[1], style[2]
            # Numéro de page de la ligne de début et fin
            page_start = flat_mapping.get(row_start, 0)
            page_end = flat_mapping.get(row_end, 0)
            # Si le span est contenu sur la même page, on le garde tel quel
            if page_start == page_end:
                adjusted_styles.append(style)
            else:
                # On découpe le span sur chaque page comprise entre le début et la fin
                current_page = page_start
                current_segment_start = row_start
                for row in range(row_start, row_end + 1):
                    # Dès qu'on détecte que la ligne courante appartient à une nouvelle page,
                    # on ajoute le span pour l'ancienne page (de current_segment_start à row-1).
                    if flat_mapping.get(row, current_page) != current_page:
                        adjusted_styles.append(
                            (
                                "SPAN",
                                (col_start, current_segment_start),
                                (col_end, row - 1),
                            )
                        )
                        current_page = flat_mapping[row]
                        current_segment_start = row
                # On ajoute le dernier segment qui va de current_segment_start à row_end
                adjusted_styles.append(
                    ("SPAN", (col_start, current_segment_start), (col_end, row_end))
                )
        else:
            # Pour d'autres commandes (par exemple BACKGROUND), on peut les ajouter directement
            adjusted_styles.append(style)
    return adjusted_styles


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

import os
import jpype
import jpype.imports
from jpype.types import *
import platform

import os
import platform
import jpype

def generate_table_1_pdf():
    REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
    input_file = os.path.join(REPORTS_DIR, 'bin', 'annexe1.jasper')
    output_dir = os.path.join('media', 'rapports')
    output_file = os.path.join(output_dir, 'annexe_1.pdf')
    lib_dir = os.path.join(REPORTS_DIR, 'lib')

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Construction du classpath
    separator = ";" if platform.system() == "Windows" else ":"
    classpath = separator.join([
        os.path.join(lib_dir, jar)
        for jar in os.listdir(lib_dir) if jar.endswith(".jar")
    ])
    print("Classpath:", classpath)

    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=classpath, convertStrings=True)
        print("JVM démarrée.")

    from java.util import HashMap
    from java.sql import DriverManager

    try:
        from net.sf.jasperreports.engine import JasperFillManager, JasperExportManager
        print("Classes JasperReports importées avec succès.")
    except Exception as e:
        print("Erreur lors de l'import des classes JasperReports:", e)
        raise

    db_url = f"jdbc:postgresql://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_USER_PASSWORD")
    connection = None

    try:
        connection = DriverManager.getConnection(db_url, db_user, db_pass)
        print("Connexion à la base de données établie.")

        params = HashMap()

        jasperPrint = JasperFillManager.fillReport(input_file, params, connection)
        print("Rapport rempli avec succès.")

        JasperExportManager.exportReportToPdfFile(jasperPrint, output_file)
        print(f"PDF généré avec succès : {output_file}")

        # Lire le PDF et retourner son contenu binaire
        with open(output_file, 'rb') as f:
            pdf_content = f.read()

        return pdf_content

    except Exception as e:
        print("Erreur lors du remplissage ou de l'export :", e)
        e.printStackTrace()
        raise

    finally:
        if connection:
            try:
                connection.close()
                print("Connexion à la base de données fermée.")
            except Exception as e:
                print("Erreur lors de la fermeture de la connexion :", e)


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
    REPORTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'reports')
    input_file = os.path.join(REPORTS_DIR, 'bin', 'annexe2.jasper')
    output_dir = os.path.join('media', 'rapports')
    output_file = os.path.join(output_dir, 'annexe_2.pdf')
    lib_dir = os.path.join(REPORTS_DIR, 'lib')

    # Créer le répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Construction du classpath
    separator = ";" if platform.system() == "Windows" else ":"
    classpath = separator.join([
        os.path.join(lib_dir, jar)
        for jar in os.listdir(lib_dir) if jar.endswith(".jar")
    ])
    print("Classpath:", classpath)

    if not jpype.isJVMStarted():
        jpype.startJVM(classpath=classpath, convertStrings=True)
        print("JVM démarrée.")

    from java.util import HashMap
    from java.sql import DriverManager

    try:
        from net.sf.jasperreports.engine import JasperFillManager, JasperExportManager
        print("Classes JasperReports importées avec succès.")
    except Exception as e:
        print("Erreur lors de l'import des classes JasperReports:", e)
        raise

    db_url = f"jdbc:postgresql://{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_USER_PASSWORD")
    connection = None

    try:
        connection = DriverManager.getConnection(db_url, db_user, db_pass)
        print("Connexion à la base de données établie.")

        params = HashMap()

        jasperPrint = JasperFillManager.fillReport(input_file, params, connection)
        print("Rapport rempli avec succès.")

        JasperExportManager.exportReportToPdfFile(jasperPrint, output_file)
        print(f"PDF généré avec succès : {output_file}")

        # Lire le PDF et retourner son contenu binaire
        with open(output_file, 'rb') as f:
            pdf_content = f.read()

        return pdf_content

    except Exception as e:
        print("Erreur lors du remplissage ou de l'export :", e)
        e.printStackTrace()
        raise

    finally:
        if connection:
            try:
                connection.close()
                print("Connexion à la base de données fermée.")
            except Exception as e:
                print("Erreur lors de la fermeture de la connexion :", e)


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


from contractualisation.models import Etape, EtapeContractualisation

# Paramètre de requête attendu
type_param = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="Type de procedure de contractualisation à filtrer (ex: 'appels d'offres restreint', 'appels d'offres ouverts', etc...)",
    type=openapi.TYPE_STRING,
    required=True,
)


@swagger_auto_schema(
    method="get",
    manual_parameters=[type_param],
    operation_summary="Génère un PDF d'annexe 3 filtré par type de tâche",
    operation_description="""
Ce point de terminaison permet de générer et télécharger un fichier PDF contenant
le tableau des tâches filtré par un type spécifique.
Le PDF contient les données de chaque tâche, étape par étape, ainsi que les montants financiers associés.
""",
    responses={
        200: "PDF généré avec succès",
        400: 'Paramètre "type" manquant ou invalide',
    },
)
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
    type = request.query_params.get("type")
    pdf_content = generate_table_3_pdf(type)  # Appelle la fonction qui construit le PDF
    response = FileResponse(io.BytesIO(pdf_content), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="rapport.pdf"'
    return response


def generate_table_3_pdf(type_selected: str):
    """
    Génère un PDF contenant un tableau avec les tâches, étapes, et données financières pour un type donné.
    Retourne un buffer PDF (en bytes).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A3))

    # Styles
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_header = styles["Heading4"]
    style_normal.alignment = 1
    style_normal.fontName = "DejaVuSans"
    style_header.alignment = 1

    # Récupérer les tâches et étapes liées au type
    taches = Tache.objects.filter(type=type_selected)
    list_etapes = Etape.objects.filter(type=type_selected).order_by("rang")

    if not taches.exists() or not list_etapes.exists():
        raise ValueError("Aucune donnée disponible pour le type fourni.")

    # Titre
    title_text = f"MISE EN ŒUVRE DU PLAN DE PASSATION DES MARCHES {type_selected} au { datetime.today().strftime('%d/%m/%Y')}"
    title = Paragraph(title_text, style_header)

    # En-têtes
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

    # Styles de colonnes
    style_columns = [
        ("SPAN", (0, 0), (0, 1)),
        ("SPAN", (-1, 0), (-1, 1)),
        ("SPAN", (-5, 0), (-2, 0)),
    ]
    for i, _ in enumerate(list_etapes):
        style_columns.append(("SPAN", (1 + (i * 3), 0), (3 + (i * 3), 0)))

    table_data = [headers, sub_headers]

    for tache in taches:
        row_data = [Paragraph(tache.title_fr, style=style_normal)]
        montantEtape = None
        etapes_contractualisations = EtapeContractualisation.objects.filter(tache=tache)

        for etape in list_etapes:
            contract = etapes_contractualisations.filter(etape=etape).first()
            if contract:
                if contract.montant_prevu and contract.montant_reel:
                    montantEtape = contract
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
                date_effective = contract.date_saisine or contract.date_effective
                row_data.append(
                    VerticalParagraph(
                        date_effective.strftime("%d/%m/%Y") if date_effective else "",
                        style=style_normal,
                    )
                )
                ecart = (
                    (date_effective - contract.date_prevue).days
                    if date_effective and contract.date_prevue
                    else ""
                )
                row_data.append(
                    VerticalParagraph(
                        (
                            f"{ecart} J {'❌' if ecart < 0 else '✅'}"
                            if ecart != ""
                            else ""
                        ),
                        style=style_normal,
                    )
                )
            else:
                row_data.extend(["", "", ""])

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

        table_data.append(row_data)

    col_widths = [80] + [20] * (len(table_data[0]) - 2) + [80]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BACKGROUND", (0, 0), (-1, 1), colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
            + style_columns
        )
    )

    doc.build([title, Spacer(1, 12), table])
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
