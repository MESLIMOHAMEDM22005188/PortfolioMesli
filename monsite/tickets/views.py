from datetime import datetime, time, date

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode, urlsafe_base64_encode

from .forms import RegisterForm, TicketForm
from .models import Alert, Pole, Ticket

User = get_user_model()


# ---------------------- UTILITAIRES ----------------------

def is_admin(user):
    """Vérifie si l’utilisateur est membre du staff (admin)."""
    return user.is_staff


# ---------------------- AUTHENTIFICATION ----------------------

def login_view(request):
    error = None
    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ne jamais rediriger vers un hôte externe fourni par le navigateur.
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect("tickets:home")

        error = "Identifiants incorrects."

    return render(request, "tickets/login.html", {
        "error": error,
        "next": next_url,
    })


def register_view(request):
    """Crée un compte à partir du formulaire d’inscription."""
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("tickets:login")

    return render(request, "tickets/register.html", {"form": form})


# ---------------------- RÉINITIALISATION DU MOT DE PASSE ----------------------

def password_reset_request(request):
    """
    Envoie un lien temporaire par e-mail. La réponse reste identique que
    l’adresse existe ou non, afin de limiter l’énumération des comptes.
    Le lien n’est jamais stocké dans la session ni rendu dans une page web.
    """
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]

            # Utilise le filtrage Django : compte actif et mot de passe utilisable.
            for user in form.get_users(email):
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_path = reverse(
                    "tickets:password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
                reset_link = request.build_absolute_uri(reset_path)
                message_body = render_to_string(
                    "tickets/password_reset_email.html",
                    {"user": user, "reset_link": reset_link},
                )
                send_mail(
                    subject="Réinitialisation de votre mot de passe",
                    message=message_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

            return redirect("tickets:password_reset_done")
    else:
        form = PasswordResetForm()

    return render(request, "tickets/password_reset.html", {"form": form})


def password_reset_email_page(request):
    """Confirmation générique : aucun compte ni lien sensible n’est révélé."""
    return render(request, "tickets/password_reset_done.html")


def password_reset_confirm(request, uidb64, token):
    """Vérifie le jeton avant d’autoriser la définition d’un nouveau mot de passe."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        return render(request, "tickets/password_reset_invalid.html")

    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("tickets:password_reset_complete")
    else:
        form = SetPasswordForm(user)

    return render(request, "tickets/password_reset_confirm.html", {"form": form})


# ---------------------- GESTION DES TICKETS ----------------------

@login_required
def ticket_list(request):
    """Affiche les tickets créés par l’utilisateur ou qui lui sont assignés."""
    qs = Ticket.objects.filter(
        Q(creator=request.user) | Q(assigned_to=request.user)
    ).order_by("-created_at")

    for ticket in qs:
        if isinstance(ticket.created_at, date) and not isinstance(ticket.created_at, datetime):
            try:
                ticket.created_at = timezone.make_aware(
                    datetime.combine(ticket.created_at, time.min)
                )
            except (TypeError, ValueError):
                # Ne pas exposer de données potentiellement sensibles dans les logs.
                continue

    return render(request, "tickets/ticket_list.html", {"tickets": qs})


@login_required
def pole_dashboard(request):
    """Affiche le tableau des pôles."""
    poles = Pole.objects.prefetch_related("tickets").all()
    return render(request, "tickets/pole_dashboard.html", {"poles": poles})


@login_required
def ticket_create(request):
    """Crée un ticket en imposant le créateur à l’utilisateur connecté."""
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator = request.user
            ticket.pole = None
            ticket.save()
            return redirect("tickets:ticket_list")
    else:
        form = TicketForm()

    return render(request, "tickets/ticket_create.html", {"form": form})


@login_required
@user_passes_test(is_admin)
@require_POST
def ticket_close(request, pk):
    """Ferme un ticket ; cette action d’écriture exige une requête POST."""
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = "closed"
    ticket.save(update_fields=["status", "updated_at"])
    return redirect("tickets:ticket_list")


@login_required
def home(request):
    """Affiche les tickets créés par l’utilisateur connecté."""
    tickets = Ticket.objects.filter(creator=request.user).order_by("-created_at")
    return render(request, "tickets/home.html", {"tickets": tickets})


# ---------------------- ALERTES ----------------------

@login_required
@staff_member_required
def create_alert(request):
    """Permet uniquement au personnel autorisé de créer une alerte."""
    if request.method == "POST":
        contenu = (request.POST.get("contenu") or "").strip()
        if contenu:
            Alert.objects.create(contenu=contenu)
            messages.success(request, "Alerte créée avec succès.")
        else:
            messages.error(request, "Le contenu de l’alerte ne peut pas être vide.")
        return redirect("tickets:admin_dashboard")

    return render(request, "tickets/create_alert.html")


@login_required
@staff_member_required
def admin_dashboard(request):
    """Tableau de bord réservé au personnel autorisé."""
    tickets = Ticket.objects.all().order_by("-created_at")
    poles = Pole.objects.all()
    users = User.objects.all()
    alerts = Alert.objects.order_by("-created_at")[:10]

    return render(request, "tickets/dashboard.html", {
        "tickets": tickets,
        "poles": poles,
        "users": users,
        "alerts": alerts,
    })


@login_required
@staff_member_required
def pole_description(request, pole_id):
    """Affiche le détail d’un pôle aux membres du personnel."""
    pole = get_object_or_404(Pole, pk=pole_id)
    return render(request, "tickets/pole_description.html", {"pole": pole})
