from django.contrib.auth.models import AbstractUser
from django.db import models

class Formateur(AbstractUser):
    username = None  # On désactive le username
    nom_complet = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)  # 🔹 Champ email obligatoire

    # Choices
    LOCALITE_CHOICES = [
        ("Dakar", "Dakar"),
        ("Thiès", "Thiès"),
        ("Saint-Louis", "Saint-Louis"),
        ("Kaolack", "Kaolack"),
        ("Ziguinchor", "Ziguinchor"),
        ("Autre", "Autre"),
    ]
    
    MATIERE_CHOICES = [
        ("Mathématiques", "Mathématiques"),
        ("Français", "Français"),
        ("Arabe", "Arabe"),
        ("Histo-Geo", "Histo-Geo"),
        ("Physique", "Physique"),
        ("Anglais", "Anglais"),
        ("Informatique", "Informatique"),
        ("Autre", "Autre"),
    ]

    localite = models.CharField(max_length=100, choices=LOCALITE_CHOICES, default="Dakar")
    matiere = models.CharField(max_length=50, choices=MATIERE_CHOICES, default="Mathématiques")
    matiere_personnalisee = models.CharField(max_length=100, blank=True, null=True)
    numero = models.CharField(max_length=20, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    # 🔹 Utilise 'nom_complet' comme identifiant de connexion
    USERNAME_FIELD = 'nom_complet'
    # 🔹 Champs requis pour la commande 'createsuperuser'
    REQUIRED_FIELDS = ['email', 'localite', 'matiere']  

    # Relations ManyToMany (évite les conflits avec AbstractUser)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='formateur_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='formateur_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.nom_complet
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email