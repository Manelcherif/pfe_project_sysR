from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Candidat, Formation, Experience, Candidature,
    Offre, CandidatLangue, Utilisateur, Entretien
)

# Formulaire d'inscription uniquement pour les candidats
class CandidatRegisterForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidat'  # Forcer le rôle
        if commit:
            user.save()
        return user


# Formulaire pour les infos personnelles du candidat (profil)
class CandidatForm(forms.ModelForm):
    class Meta:
        model = Candidat
        exclude = ['user', 'photo_profil']


# Formulaire formation
class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['titre', 'etablissement', 'date_debut', 'date_fin']


# Formulaire expérience
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['entreprise', 'poste', 'date_debut', 'date_fin']


# Formulaire compétence langue
class CandidatLangueForm(forms.ModelForm):
    class Meta:
        model = CandidatLangue
        fields = ['langue', 'niveau']


# Formulaire pour postuler à une offre
class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['offre']


# Formulaire pour ajouter une offre (admin uniquement)
class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'description', 'competences', 'region', 'departement']


# Formulaire entretien
class EntretienForm(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = ['date_entretien', 'heure_entretien', 'type_entretien', 'etat', 'candidature']