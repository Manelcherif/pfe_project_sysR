from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('candidat', 'Candidat'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidat')

    def __str__(self):
        return self.username


class Region(models.Model):
    REGION_CHOICES = [
        ('est', 'Est'),
        ('ouest', 'Ouest'),
        ('centre', 'Centre'),
    ]
    
    nom = models.CharField(
        max_length=20,
        choices=REGION_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_nom_display()


class Departement(models.Model):
    nom_departement = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_departement


class Domaine(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Specialite(models.Model):
    nom = models.CharField(max_length=100)
    domaine = models.ForeignKey(Domaine, on_delete=models.CASCADE, related_name="specialites")

    def __str__(self):
        return self.nom


class Competence(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Langue(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Admin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=100, default='')
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=100, default='')
    telephone = models.CharField(max_length=20, default='0000000000')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.prenom}"


class Candidat(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidat")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    profession = models.CharField(max_length=100)
    description = models.TextField()
    competences = models.ManyToManyField(Competence)
    specialite = models.ManyToManyField(Specialite)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    photo_profil = models.ImageField(upload_to='profile_photos/', default='profile_photos/default.jpg', blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def check_password(self, password):
        return self.user.check_password(password)


class CandidatLangue(models.Model):
    LEVEL_CHOICES = [
        ('A1', 'A1 - Débutant'),
        ('A2', 'A2 - Élémentaire'),
        ('B1', 'B1 - Intermédiaire'),
        ('B2', 'B2 - Intermédiaire supérieur'),
        ('C1', 'C1 - Avancé'),
        ('C2', 'C2 - Maîtrise'),
    ]

    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    langue = models.ForeignKey(Langue, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=2, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.candidat} - {self.langue} ({self.get_niveau_display()})"


class Formation(models.Model):
    titre = models.CharField(max_length=200)
    etablissement = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField()
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name="formations")

    def __str__(self):
        return f"{self.titre} - {self.etablissement}"


class Experience(models.Model):
    entreprise = models.CharField(max_length=200)
    poste = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name="experiences")

    def __str__(self):
        return f"{self.poste} - {self.entreprise}"


class Offre(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    competences = models.ManyToManyField(Competence)
    date_creation = models.DateField(auto_now_add=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, related_name='offres')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=True, related_name='offres')

    def __str__(self):
        return self.titre


class Candidature(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_postulation = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_entretien = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.candidat} - {self.offre} ({self.statut})"


class Entretien(models.Model):
    TYPE_ENTRETIEN_CHOICES = [
        ('video', 'Appel vidéo'),
        ('presentiel', 'Présentiel'),
    ]

    ETAT_CHOICES = [
        ('programme', 'Programmé'),
        ('complete', 'Complété'),
        ('annule', 'Annulé'),
    ]

    date_entretien = models.DateField()
    heure_entretien = models.TimeField()
    type_entretien = models.CharField(max_length=20, choices=TYPE_ENTRETIEN_CHOICES)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='programme')
    candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entretien {self.id} - {self.type_entretien} le {self.date_entretien}"