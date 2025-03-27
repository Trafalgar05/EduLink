from django.contrib import admin
from .models import Formateur
from .models import NewsletterSubscriber

@admin.register(Formateur)
class FormateurAdmin(admin.ModelAdmin):
    list_display = ("nom_complet", "email", "localite", "get_matieres", "date_joined")
    search_fields = ("nom_complet", "email", "localite", "matiere", "matiere_personnalisee")
    ordering = ("date_joined",)

    def get_matieres(self, obj):
        return obj.matiere if not obj.matiere_personnalisee else obj.matiere_personnalisee
    get_matieres.short_description = 'Matière'
    
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'