/* Global page translation powered by Google Translate. */
(function () {
    "use strict";

    function initializeLanguageSwitcher() {
        var switcher = document.querySelector(".site-language-bar");
        var widget = document.getElementById("google_translate_element");

        if (!switcher || !widget || switcher.dataset.initialized === "true") {
            return;
        }
        switcher.dataset.initialized = "true";

        var sourceLanguage = (switcher.dataset.sourceLanguage || document.documentElement.lang || "en")
            .toLowerCase()
            .split("-")[0];
        var buttons = Array.prototype.slice.call(
            switcher.querySelectorAll("[data-language]")
        );
        var status = switcher.querySelector(".site-language-status");
        var requestedLanguage = null;
        var languageNames = { fr: "French", en: "English", es: "Spanish", de: "German" };

        function setActiveLanguage(language) {
            buttons.forEach(function (button) {
                var active = button.dataset.language === language;
                button.setAttribute("aria-pressed", active ? "true" : "false");
            });
        }

        function getSavedLanguage() {
            var match = document.cookie.match(/(?:^|;\s*)googtrans=\/[^/]+\/([^;]+)/);
            if (!match) {
                return sourceLanguage;
            }
            try {
                return decodeURIComponent(match[1]).split("-")[0].toLowerCase();
            } catch (error) {
                return sourceLanguage;
            }
        }

        function applyLanguage(language, attempt) {
            requestedLanguage = language;
            var select = document.querySelector("#google_translate_element select.goog-te-combo")
                || document.querySelector("select.goog-te-combo");

            if (!select) {
                if (attempt < 50) {
                    window.setTimeout(function () {
                        applyLanguage(language, attempt + 1);
                    }, 120);
                } else if (status) {
                    status.textContent = "Translation service unavailable. Check your connection and try again.";
                }
                return;
            }

            select.value = language;
            select.dispatchEvent(new Event("change", { bubbles: true }));
            setActiveLanguage(language);

            if (status) {
                status.textContent = "";
            }
        }

        buttons.forEach(function (button) {
            button.addEventListener("click", function () {
                applyLanguage(button.dataset.language, 0);
            });
        });

        var savedLanguage = getSavedLanguage();
        setActiveLanguage(["fr", "en", "es", "de"].indexOf(savedLanguage) !== -1
            ? savedLanguage
            : sourceLanguage);

        window.googleTranslateElementInit = function () {
            if (!window.google || !window.google.translate || !window.google.translate.TranslateElement) {
                if (status) {
                    status.textContent = "Translation service unavailable.";
                }
                return;
            }

            new window.google.translate.TranslateElement({
                pageLanguage: sourceLanguage,
                includedLanguages: "fr,en,es,de",
                autoDisplay: false
            }, "google_translate_element");

            if (requestedLanguage) {
                applyLanguage(requestedLanguage, 0);
            }
        };

        var googleScript = document.createElement("script");
        googleScript.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
        googleScript.async = true;
        googleScript.onerror = function () {
            if (status) {
                status.textContent = "Translation service unavailable. Check your connection.";
            }
        };
        document.head.appendChild(googleScript);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializeLanguageSwitcher, { once: true });
    } else {
        initializeLanguageSwitcher();
    }
})();