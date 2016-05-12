from django.forms import forms


class PdfForm(forms.Form):
    file = forms.FileField()
