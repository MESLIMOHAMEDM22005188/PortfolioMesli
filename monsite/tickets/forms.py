# tickets/forms.py
from django import forms
from datetime import datetime, time
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Ticket, Pole
User = get_user_model()

class PoleForm(forms.ModelForm):
    class Meta:
        model = Pole
        fields = ['code', 'name', 'color']
class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Adresse e-mail",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'votre@mail.fr'})
    )

    class Meta:
        model = get_user_model()   # <— utilise users.User
        fields = ["username", "email", "password1", "password2"]

    # … le reste reste identique …


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class TicketForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),  # ou tout autre filtre approprié
        required=False,
        label="Assigner à (optionnel)"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajout des astérisques et modification des labels
        self.fields['title'].label = "Titre du ticket *"
        self.fields['description'].label = "Description détaillée *"
        self.fields['category'].label = "Catégorie *"
        self.fields['priority'].label = "Niveau d'urgence *"
        self.fields['attachment'].label = "Fichier joint (optionnel)"
        self.fields['problem_date'].label = "Date du problème *"
        self.fields['assigned_to'].label = "Assigner à (optionnel)"
        # Placeholders en français
        self.fields['title'].widget.attrs['placeholder'] = "Résumez votre problème en quelques mots"
        self.fields['description'].widget.attrs[
            'placeholder'] = "Décrivez le problème en détail, étapes pour le reproduire, etc."

    def save(self, commit=True, creator=None, **kwargs):
        instance = super().save(commit=False)
        if creator:
            instance.creator = creator
        if isinstance(instance.problem_date, datetime) is False:
            instance.problem_date = timezone.make_aware(datetime.combine(instance.problem_date, time.min))
        if commit:
            instance.save()
            self.save_m2m()  # Important pour les relations many-to-many si vous en avez

        return instance

    class Meta:
        model = Ticket
        fields = ["title", "description", "category", "priority", "attachment", "problem_date"]
        widgets = {
            "problem_date": forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }, format='%Y-%m-%dT%H:%M'),
        }