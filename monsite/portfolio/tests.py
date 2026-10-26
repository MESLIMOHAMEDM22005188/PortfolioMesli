from django.test import TestCase
from django.urls import reverse


class CybersecurityPageSmokeTests(TestCase):
    """Basic route/template regression tests for the public portfolio pages."""

    def test_cybersecurity_pages_render_successfully(self):
        route_names = (
            "portfolio:cyber_home",
            "portfolio:cmdi_course",
            "portfolio:cmdi_exploit",
            "portfolio:web_fuzzing",
            "portfolio:web_fuzzing_exploit",
            "portfolio:server_side_attack",
            "portfolio:server_side_exploit",
            "portfolio:brute_force_html",
            "portfolio:foundations_lab",
            "portfolio:enterprise_lab",
            "portfolio:soc_lab",
            "portfolio:securecloudlab",
        )
        for route_name in route_names:
            with self.subTest(route=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)

    def test_command_injection_walkthrough_is_not_web_fuzzing_content(self):
        response = self.client.get(reverse("portfolio:cmdi_exploit"))
        self.assertContains(response, "OS Command Injection")
        self.assertContains(response, "Mesures correctives")
        self.assertNotContains(response, "Web Fuzzing (Exercice 1)")

    def test_cybersecurity_home_links_to_real_course_routes(self):
        response = self.client.get(reverse("portfolio:cyber_home"))
        self.assertContains(response, reverse("portfolio:cmdi_course"))
        self.assertContains(response, reverse("portfolio:web_fuzzing"))
        self.assertContains(response, reverse("portfolio:soc_lab"))
