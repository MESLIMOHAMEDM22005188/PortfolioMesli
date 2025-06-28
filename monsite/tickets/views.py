from datetime import datetime, time, date

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.admin.views.decorators import staff_member_required

from .forms import RegisterForm, TicketForm
from .models import Ticket, Pole, Alert

User = get_user_model()


# ---------------------- UTILITAIRES ----------------------

def is_admin(user):
    """Vérifie si l’utilisateur est membre du staff (admin)."""
    return user.is_staff


# ---------------------- AUTHENTIFICATION ----------------------

def login_view(request):
    """
    Affiche le formulaire de connexion et authentifie l’utilisateur.
    Si la méthode est POST et que le couple (username, password) est valide,
    on redirige vers la vue 'tickets:home'.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('tickets:home')

    return render(request, 'tickets/login.html')


def register_view(request):
    """
    Affiche le formulaire d’inscription. Si valide, crée l’utilisateur
    et redirige vers la page de connexion.
    """
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('tickets:login')

    return render(request, 'tickets/register.html', {'form': form})


# ---------------------- RÉINITIALISATION DU MOT DE PASSE ----------------------

def password_reset_request(request):
    """
    Gère la demande de réinitialisation de mot de passe.
    Envoie un email contenant un lien de reset si l’email existe.
    """
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = request.build_absolute_uri(f"/tickets/reset/{uid}/{token}/")

                subject = "Réinitialisation de votre mot de passe"
                message_body = render_to_string('tickets/password_reset_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(subject, message_body, 'no-reply@votresite.tld', [user.email])

                request.session['pwd_reset_user'] = user.username
                request.session['pwd_reset_link'] = reset_link

            return redirect('tickets:password_reset_done')
    else:
        form = PasswordResetForm()

    return render(request, 'tickets/password_reset.html', {'form': form})


def password_reset_email_page(request):
    """
    Affiche la page de confirmation d’envoi d’email de réinitialisation,
    en récupérant l’utilisateur et le lien stockés en session.
    """
    username = request.session.pop('pwd_reset_user', None)
    reset_link = request.session.pop('pwd_reset_link', None)
    context = {}

    if username and reset_link:
        context['user'] = User.objects.filter(username=username).first()
        context['reset_link'] = reset_link

    return render(request, 'tickets/password_reset_email.html', context)


def password_reset_confirm(request, uidb64, token):
    """
    Vérifie le token et l’UID, puis permet à l’utilisateur de saisir un nouveau mot de passe.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, 'tickets/password_reset_invalid.html')

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('tickets:password_reset_complete')
    else:
        form = SetPasswordForm(user)

    return render(request, 'tickets/password_reset_confirm.html', {'form': form})


# ---------------------- GESTION DES TICKETS ----------------------

@login_required
def ticket_list(request):
    """
    Affiche la liste des tickets auxquels l’utilisateur est créateur ou assigné.
    Corrige aussi le champ created_at si nécessaire.
    """
    qs = Ticket.objects.filter(
        Q(creator=request.user) | Q(assigned_to=request.user)
    ).order_by('-created_at')

    for t in qs:
        # Si created_at est mal lu comme date naïve, on le rend aware
        if isinstance(t.created_at, date) and not isinstance(t.created_at, datetime):
            try:
                naive_datetime = datetime.combine(t.created_at, time.min)
                t.created_at = timezone.make_aware(naive_datetime)
            except Exception:
                print(f"Erreur lors de la conversion de created_at pour le ticket {t.id}")

    return render(request, 'tickets/ticket_list.html', {'tickets': qs})


@login_required
def pole_dashboard(request):
    """
    Affiche un dashboard par pôle, avec tous les tickets préchargés pour chaque pôle.
    """
    poles = Pole.objects.prefetch_related('tickets').all()
    return render(request, 'tickets/pole_dashboard.html', {'poles': poles})


@login_required
def ticket_create(request):
    """
    Permet de créer un ticket.
    Par défaut, on n’affecte pas de pôle (ticket.pole = None).
    Si besoin, on peut assigner un pôle par défaut ou faire choisir l’utilisateur.
    """
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user
            ticket.pole = None  # Aucun pôle par défaut, ou Pole.objects.first()
            ticket.save()
            return redirect('tickets:ticket_list')
    else:
        form = TicketForm()

    return render(request, 'tickets/ticket_create.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def ticket_close(request, pk):
    """
    Ferme un ticket : passe le statut à 'closed' et redirige vers la liste des tickets.
    Accessible seulement aux utilisateurs staff (admins).
    """
    t = get_object_or_404(Ticket, pk=pk)
    t.status = 'closed'
    t.save()
    return redirect('tickets:ticket_list')


@login_required
def home(request):
    """
    Page d’accueil après connexion : affiche uniquement les tickets créés par l’utilisateur.
    """
    tickets = Ticket.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'tickets/home.html', {'tickets': tickets})


# ---------------------- ALERTES ----------------------

def create_alert(request):
    """
    Méthode factice pour créer une alerte via un formulaire.
    À remplacer si on utilise réellement le modèle Alert.
    """
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        # Si tu souhaites réellement stocker l’alerte, remplace le print par :
        # Alert.objects.create(contenu=contenu)
        print("Alerte créée :", contenu)
        messages.success(request, "Alerte envoyée avec succès.")
        return redirect('tickets:admin_dashboard')

    return render(request, 'tickets/create_alert.html')


@login_required
@staff_member_required
def admin_dashboard(request):
    """
    Tableau de bord administrateur :
    - Liste de tous les tickets
    - Liste de tous les pôles
    - Liste de tous les utilisateurs (avec leur pôle)
    - Liste des dernières alertes
    Accessible uniquement aux membres du staff.
    """
    tickets = Ticket.objects.all().order_by('-created_at')
    poles = Pole.objects.all()
    users = User.objects.select_related('pole').all()
    alerts = Alert.objects.order_by('-created_at')[:10]

    context = {
        'tickets': tickets,
        'poles': poles,
        'users': users,
        'alerts': alerts,
    }
    return render(request, 'tickets/dashboard.html', context)


@login_required
@staff_member_required
def pole_description(request, pole_id):
    """
    Affiche la page de détail d’un pôle.
    Accessible uniquement aux membres du staff.
    """
    pole = get_object_or_404(Pole, pk=pole_id)
    return render(request, 'tickets/pole_description.html', {'pole': pole})

