import os
import sys
from datetime import datetime, time, date
from django.utils import timezone

# Ajouter le chemin du projet à PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
import django
django.setup()

from tickets.models import Ticket

def run():
    for t in Ticket.objects.all():
        changed = False

        if isinstance(t.created_at, date) and not isinstance(t.created_at, datetime):
            t.created_at = timezone.make_aware(datetime.combine(t.created_at, time.min))
            changed = True

        if isinstance(t.problem_date, date) and not isinstance(t.problem_date, datetime):
            t.problem_date = timezone.make_aware(datetime.combine(t.problem_date, time.min))
            changed = True

        if changed:
            print(f"Correction appliquée au ticket {t.id}")
            t.save()
