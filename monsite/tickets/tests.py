from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Alert, Ticket

User = get_user_model()


class TicketHubSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="portfolio-test-user",
            email="portfolio-test@example.com",
            password="Test-password-2026!",
        )
        self.staff_user = User.objects.create_user(
            username="portfolio-test-staff",
            email="portfolio-staff@example.com",
            password="Test-password-2026!",
            is_staff=True,
        )

    def test_password_reset_link_is_sent_by_email_only(self):
        response = self.client.post(
            reverse("tickets:reset"),
            {"email": self.user.email},
        )

        self.assertRedirects(response, reverse("tickets:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/tickets/reset/", mail.outbox[0].body)
        self.assertNotIn("pwd_reset_link", self.client.session)
        self.assertNotIn("pwd_reset_user", self.client.session)

    def test_password_reset_done_page_never_exposes_reset_link(self):
        session = self.client.session
        session["pwd_reset_link"] = "https://attacker.example/reset/secret"
        session["pwd_reset_user"] = self.user.username
        session.save()

        response = self.client.get(reverse("tickets:password_reset_done"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "attacker.example")
        self.assertNotContains(response, "secret")

    def test_login_rejects_external_next_redirect(self):
        response = self.client.post(
            reverse("tickets:login"),
            {
                "username": self.user.username,
                "password": "Test-password-2026!",
                "next": "https://attacker.example/phishing",
            },
        )

        self.assertRedirects(response, reverse("tickets:home"))

    def test_non_staff_cannot_create_alert(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("tickets:create_alert"),
            {"contenu": "Test alert"},
        )

        self.assertIn(response.status_code, (302, 403))
        self.assertEqual(Alert.objects.count(), 0)

    def test_staff_can_create_alert(self):
        self.client.force_login(self.staff_user)
        response = self.client.post(
            reverse("tickets:create_alert"),
            {"contenu": "Test alert"},
        )

        self.assertRedirects(response, reverse("tickets:admin_dashboard"))
        self.assertTrue(Alert.objects.filter(contenu="Test alert").exists())

    def test_ticket_close_requires_post(self):
        ticket = Ticket.objects.create(
            title="Test ticket",
            description="Ticket for security tests",
            creator=self.staff_user,
        )
        self.client.force_login(self.staff_user)

        response = self.client.get(reverse("tickets:ticket_close", args=[ticket.pk]))

        self.assertEqual(response.status_code, 405)
        ticket.refresh_from_db()
        self.assertNotEqual(ticket.status, "closed")
