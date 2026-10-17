"""Inject the language switcher into public HTML responses."""

import re

from django.template.loader import render_to_string
from django.templatetags.static import static


class LanguageSwitcherMiddleware:
    """Add a translation selector to rendered HTML pages site-wide."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.path == "/admin"
            or request.path.startswith("/admin/")
            or response.status_code != 200
            or response.streaming
            or "text/html" not in response.get("Content-Type", "").lower()
            or response.get("Content-Encoding")
        ):
            return response

        try:
            html = response.content.decode(response.charset or "utf-8")
        except (AttributeError, UnicodeDecodeError):
            return response

        if "site-language-bar" in html or not re.search(r"<body\b", html, re.IGNORECASE):
            return response

        language_match = re.search(
            r"<html\b[^>]*\blang\s*=\s*['\"]([a-zA-Z-]+)['\"]",
            html,
            re.IGNORECASE,
        )
        source_language = (
            language_match.group(1).split("-")[0].lower()
            if language_match
            else "en"
        )

        assets = (
            f'\n<link rel="stylesheet" href="{static("assets/css/language-switcher.css")}?v=20261017-2">'
            f'\n<script src="{static("assets/js/language-switcher.js")}?v=20261017-2" defer></script>\n'
        )
        html, head_count = re.subn(
            r"</head\s*>",
            lambda match: assets + match.group(0),
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        if not head_count:
            return response

        switcher = render_to_string(
            "includes/site_language_switcher.html",
            {"source_lang": source_language},
        )
        html, body_count = re.subn(
            r"(<body\b[^>]*>)",
            lambda match: match.group(1) + "\n" + switcher + "\n",
            html,
            count=1,
            flags=re.IGNORECASE,
        )
        if not body_count:
            return response

        response.content = html.encode(response.charset or "utf-8")
        return response
