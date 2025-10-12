from django.db import models
from django.conf import settings
from django.utils import timezone

class Pole(models.Model):
    code  = models.CharField(max_length=10, unique=True)
    name  = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default="#cccccc")

    class Meta:
        db_table = "pole"
        managed  = True

    def __str__(self):
        return self.name

class Ticket(models.Model):
    pole = models.ForeignKey(Pole, on_delete=models.CASCADE, related_name='tickets', null=True, blank=True)

    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('critical', 'Critique'),
    ]

    CATEGORY_CHOICES = [
        ('bug', 'Bug'),
        ('feature', 'Demande de fonctionnalité'),
        ('support', 'Support technique'),
        ('other', 'Autre'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tickets'
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='support')
    attachment = models.FileField(upload_to='tickets/attachments/', null=True, blank=True)
    problem_date = models.DateTimeField(verbose_name="Date du problème", default=timezone.now)

    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"[{self.get_status_display()}] {self.title}"

class Alert(models.Model):
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contenu[:50]
