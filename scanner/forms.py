from django import forms
from .models import CodigoEscaneado

class CodigoEscaneadoForm(forms.ModelForm):
    class Meta:
        model = CodigoEscaneado
        fields = ['codigo', 'tipo']
