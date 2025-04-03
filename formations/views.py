from django.shortcuts import render, redirect,  get_object_or_404
from .models import Formateur
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import FormateurEditForm, RegisterForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import NewsletterSubscriber
from django.core.mail import send_mail
from django.conf import settings
import re



def liste_formateurs(request):
    # Récuperation de tous les formateurs
    formateurs = Formateur.objects.all()

    # Filtrage par localité
    localite = request.GET.get('localite')
    if localite:
        formateurs = formateurs.filter(localite=localite)

    # Filtrage par matière
    matiere = request.GET.get('matiere')
    if matiere:
        # Si la matière est "Autre", filtre par matière personnalisée
        if matiere == "Autre":
            formateurs = formateurs.filter(matiere_personnalisee__isnull=False)
        else:
            formateurs = formateurs.filter(matiere=matiere)

    # Liste des localités et matières pour les filtres
    localites = Formateur.LOCALITE_CHOICES
    matieres = Formateur.MATIERE_CHOICES

    return render(request, "formations/liste_formateurs.html", {
        "formateurs": formateurs,
        "localites": localites,
        "matieres": matieres,
    })

def detail_formateur(request, formateur_id):
    formateur = get_object_or_404(Formateur, id=formateur_id)
    return render(request, "formations/detail_formateur.html", {"formateur": formateur})

def home(request):
    return render(request, "formations/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connexion automatique de l'utilisateur
            messages.success(request, "Inscription réussie !")
            return redirect("dashboard")
        else:
            # Affichage des erreurs dans la console pour debug
            print("Erreurs du formulaire:", form.errors) 
    else:
        form = RegisterForm()
    
    return render(request, "formations/register.html", {
        "form": form,
        "errors": form.errors.get_json_data() if form.errors else None
    })

def login_view(request):
    if request.method == "POST":
        # Utilise nom_complet au lieu de username
        nom_complet = request.POST.get('nom_complet')
        password = request.POST.get('password')
        
        user = authenticate(request, nom_complet=nom_complet, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {nom_complet} !")
            return redirect("dashboard")
        else:
            messages.error(request, "Identifiants incorrects")
            form = AuthenticationForm(request, data=request.POST)
    else:
        form = AuthenticationForm()
    
    return render(request, "formations/login.html", {
        "form": form,
        "error_message": "Identifiants invalides" if request.method == "POST" else None
    })

@login_required
def edit_profile(request):
    formateur = request.user
    if request.method == 'POST':
        form = FormateurEditForm(request.POST, request.FILES, instance=formateur)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FormateurEditForm(instance=formateur)

    return render(request, 'formations/edit_profile.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    return render(request, "formations/dashboard.html", {"user": user})

def logout_view(request):
    logout(request)
    return redirect("home") 

@require_POST
def newsletter_subscribe(request):
    email = request.POST.get('email', '').strip()
    
    # Validation email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return JsonResponse({
            'success': False,
            'message': 'Veuillez entrer une adresse email valide'
        })
    
    try:
        # Crée ou récupère l'abonné
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={'is_active': True}
        )
        
        if not created and subscriber.is_active:
            return JsonResponse({
                'success': False,
                'message': 'Vous êtes déjà abonné à notre newsletter'
            })
        
        # Réactivation si existant mais désactivé
        if not created:
            subscriber.is_active = True
            subscriber.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Merci pour votre inscription à notre newsletter !'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"Une erreur s'est produite: {str(e)}"
        })
        
def contact(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            
            
            send_mail(
                subject=f"Nouveau contact depuis EduLink: {name}",
                message=f"De: {name} <{email}>\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Votre message a été envoyé avec succès!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f"Erreur lors de l'envoi: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Méthode non autorisée'
    }, status=405)