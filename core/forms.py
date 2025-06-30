from django import forms
from .models import nkgmodel,altocafezalmodel,velosogreenmodel,burbomcofelmodel,coxupemodel,carmocofelmodel,expocacermodel,velosocofemodel,volcafemodel

class AltocafezalModelForm(forms.ModelForm):
    class Meta:
        model = altocafezalmodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }





class burbomcofeModelForm(forms.ModelForm):
    class Meta:
        model = burbomcofelmodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }






class carmocofeModelForm(forms.ModelForm):
    class Meta:
        model = carmocofelmodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }





class expocacerModelForm(forms.ModelForm):
    class Meta:
        model = expocacermodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }






class coxupeModelForm(forms.ModelForm):
    class Meta:
        model = coxupemodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }



class nkgModelForm(forms.ModelForm):
    class Meta:
        model = nkgmodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }




class velosocofeModelForm(forms.ModelForm):
    class Meta:
        model = velosocofemodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }




class velosogreenfeModelForm(forms.ModelForm):
    class Meta:
        model = velosogreenmodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }






class volcafeModelForm(forms.ModelForm):
    class Meta:
        model = volcafemodel
        # Incluímos apenas os campos que serão preenchidos pelo usuário;
        # o campo data_registro não é editável e será definido automaticamente.
        fields = ['nome', 'id_equipamento']
        labels = {
            'nome': 'Nome do Cliente',
            'id_equipamento': 'ID do Equipamento'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do cliente'
            }),
            'id_equipamento': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o ID do equipamento'
            }),
        }
