from django import forms
from .models import Tutoria
from .constants import TEMAS

class FormTutorias(forms.ModelForm):

    alumno = forms.CharField(disabled=True, required=False)
    tutor = forms.CharField(disabled=True, required=False)
    tema = forms.ChoiceField(choices=TEMAS)
    fecha = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    descripcion = forms.CharField(widget=forms.Textarea, max_length=255, required=False)


    class Meta:
        model = Tutoria
        fields = ['tema', 'fecha', 'descripcion']
