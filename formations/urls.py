from django.urls import path
from . import views
from .views import register, login_view, dashboard, liste_formateurs, detail_formateur, logout_view, edit_profile
from .views import newsletter_subscribe, contact


urlpatterns = [
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    path('contact/', contact, name='contact'),
    path("formateurs/<int:formateur_id>/", detail_formateur, name="detail_formateur"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("formateurs/", liste_formateurs, name="liste_formateurs"),
    path("logout/", logout_view, name="logout"),
    path('edit-profile/', edit_profile, name="edit_profile")
]
