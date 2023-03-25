from django import forms

class FormularioPrueba(forms.Form):
    campo1 = forms.CharField(label='Campo 1', max_length=100)
    campo2 = forms.CharField(label='Campo 2', max_length=100)