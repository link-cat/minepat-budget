from django import forms


class ExcelUploadForm(forms.Form):
    file_uploaded = forms.FileField(
        label="Téléversez votre fichier Excel",
        help_text="Le fichier doit être au format Excel.",
    )
