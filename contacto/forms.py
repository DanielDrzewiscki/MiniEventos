from django import forms

class FormularioContacto(forms.Form):

    nombre = forms.CharField(label="Nombre",required="true")
    mail = forms.EmailField(label="Correo",required="true")
    contenido = forms.CharField(label="Contenido", widget=forms.Textarea)
