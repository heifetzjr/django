from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'birth_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nome completo',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'email@exemplo.com',
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
            }),
        }
        labels = {
            'name': 'Nome',
            'email': 'E-mail',
            'birth_date': 'Data de nascimento',
        }
        