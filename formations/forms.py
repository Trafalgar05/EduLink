from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Formateur

class RegisterForm(UserCreationForm):
    nom_complet = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom complet'})
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemple@domaine.com'})
    )
    
    localite = forms.ChoiceField(
        choices=[
            ("", "Choisissez une localité"),
            ("Dakar", "Dakar"),
            ("Thiès", "Thiès"),
            ("Saint-Louis", "Saint-Louis"),
            ("Kaolack", "Kaolack"),
            ("Ziguinchor", "Ziguinchor"),
            ("Autre", "Autre"),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    matiere = forms.ChoiceField(
        choices=[
            ("", "Choisissez une matière"),
            ("Mathématiques", "Mathématiques"),
            ("Français", "Français"),
            ("Arabe", "Arabe"),
            ("Histo-Geo", "Histo-Geo"),
            ("Physique", "Physique"),
            ("Anglais", "Anglais"),
            ("Informatique", "Informatique"),
            ("Autre", "Autre"),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    matiere_personnalisee = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Précisez votre matière'})
    )

    numero = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+221 77 123 45 67'}),
        required=True
    )

    class Meta:
        model = Formateur
        fields = ["nom_complet", "email", "password1", "password2", "localite", "matiere", "matiere_personnalisee", "numero"]
        
    def clean(self):
        cleaned_data = super().clean()
        matiere = cleaned_data.get("matiere")
        matiere_personnalisee = cleaned_data.get("matiere_personnalisee")

        if matiere == "Autre" and not matiere_personnalisee:
            self.add_error("matiere_personnalisee", "Veuillez saisir la matière enseignée.")

        return cleaned_data

class FormateurEditForm(forms.ModelForm):
    class Meta:
        model = Formateur
        fields = ['nom_complet', 'email', 'localite', 'matiere', 'matiere_personnalisee', 'numero']