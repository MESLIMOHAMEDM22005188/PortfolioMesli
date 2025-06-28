# tickets/notifications.py
from django.core.mail import send_mail
from django.conf import settings


def send_ticket_created_notification(ticket):
    subject = f"Nouveau ticket créé : {ticket.title}"
    message = f"""
    Un nouveau ticket a été créé :

    Titre: {ticket.title}
    Créé par: {ticket.creator.username}
    Priorité: {ticket.get_priority_display()}

    Description:
    {ticket.description}
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],  # ou ticket.assigned_to.email si assigné
        fail_silently=True,
    )