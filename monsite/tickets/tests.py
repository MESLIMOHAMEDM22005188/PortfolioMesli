from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

User = get_user_model()


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetSecurityTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reset-test-user",
            email="reset-test@example.com",
            password="A-strong-test-password-934!",
        )

    def test_reset_request_sends_email_but_does_not_store_link_in_session(self):
        response = self.client.post(
            reverse("tickets:reset"),
            {"email": self.user.email},
        )

        self.assertRedirects(response, reverse("tickets:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("pwd_reset_link", self.client.session)
        self.assertNotIn("pwd_reset_user", self.client.session)
        self.assertIn(self.user.email, mail.outbox[0].to)

    def test_reset_confirmation_page_never_displays_reset_link(self):
        response = self.client.get(reverse("tickets:password_reset_done"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "reset_link")
        self.assertNotContains(response, "reset-test-user")

    def test_unknown_email_gets_same_confirmation_redirect_without_email(self):
        response = self.client.post(
            reverse("tickets:reset"),
            {"email": "not-registered@example.com"},
        )

        self.assertRedirects(response, reverse("tickets:password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_login_rejects_external_next_redirect(self):
        response = self.client.post(
            reverse("tickets:login"),
            {
                "username": self.user.username,
                "password": "A-strong-test-password-934!",
                "next": "https://attacker.example/",
            },
        )

        self.assertRedirects(response, reverse("tickets:home"))

    def test_alert_creation_requires_staff_login(self):
        response = self.client.get(reverse("tickets:create_alert"))

        self.assertRedirects(
            response,
            f"{reverse('tickets:login')}?next={reverse('tickets:create_alert')}",
        )

    def test_closing_ticket_rejects_get_requests(self):
        staff_user = User.objects.create_user(
            username="ticket-admin",
            email="ticket-admin@example.com",
            password="A-strong-test-password-934!",
            is_staff=True,
        )
        self.client.force_login(staff_user)

        response = self.client.get(reverse("tickets:ticket_close", args=[999]))

        self.assertEqual(response.status_code, 405)
