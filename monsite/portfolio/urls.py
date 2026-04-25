# portfolio/urls.py
from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.accueil, name="accueil"),

    # Cisco
    path("cisco-labs/", views.cisco_labs, name="cisco_labs"),


    path("cybersecurity/", views.cyber_home, name="cyber_home"),

    # Redirection ancienne URL
    path(
        "MesPetisCours/",
        RedirectView.as_view(
            pattern_name="portfolio:mespetitscours",
            permanent=True
        ),
    ),

path("cybersecurity/web-fuzzing/", views.web_fuzzing, name="web_fuzzing"),
path("cybersecurity/web-fuzzing/exploit.html/", views.web_fuzzing_exploit, name="web_fuzzing_exploit"),

path("cybersecurity/command-injection/", views.cmdi_course, name="cmdi_course"),
path("cybersecurity/command-injection/exploit.html/", views.cmdi_exploit, name="cmdi_exploit"),

path("cybersecurity/server-side-attack/", views.server_side_attack, name="server_side_attack"),
path("cybersecurity/server-side/", views.server_side_exploit, name="server_side_exploit"),


path("cybersecurity/brute_force/", views.brute_force_html, name="brute_force_html"),

    path("mes-petits-cours/", views.mesPetitsCours, name="mespetitscours"),

    # Pages scolaires
    path("primaire/", views.primaire, name="primaire"),
    path("primaire/cp/", views.cp, name="cp"),
    path("primaire/ce1/", views.ce1, name="ce1"),
    path("primaire/ce2/", views.ce2, name="ce2"),
    path("primaire/cm1/", views.cm1, name="cm1"),
    path("primaire/cm2/", views.cm2, name="cm2"),

    # Projects
    path("projects/concurrency/", views.concurrency, name="concurrency"),
    path("projects/nim-ai/", views.nim_ai, name="nim_ai"),
    path("projects/file-crud/", views.file_crud, name="file_crud"),
    path("projects/javafx-ui/", views.javafx_ui, name="javafx_ui"),
    path("projects/tickethub-ui/", views.tickethub_ui, name="tickethub_ui"),
    path("projects/social-network/", views.social_network, name="social_network"),
    path("projects/secretary-app/", views.secretary_app, name="secretary_app"),
    path("projects/cybersecurity-insights/", views.cybersecurity_insights, name="cybersecurity_insights"),
    path("projects/portfolio-site/", views.portfolio_site, name="portfolio_site"),
    path("projects/task-management/", views.task_management, name="task_management"),
    path("projects/smartbudget-tracker/", views.smartbudget_tracker, name="smartbudget_tracker"),
    path("projects/mailcli-sender/", views.mailcli_sender, name="mailcli_sender"),
    path("projects/taskflow-poo/", views.taskflow_poo, name="taskflow_poo"),
    path("projects/solar-system/", views.solar_system, name="solar_system"),
    path("projects/earthquake-analyzer/", views.earthquake_analyzer, name="earthquake_analyzer"),
    path("projects/rsa-algorithm/", views.rsa_algorithm, name="rsa_algorithm"),
    path("projects/bandit/", views.bandit, name="bandit"),

    path("project-detail/", views.project_detail, name="project_detail"),
    path("ticketHub/", views.ticketHub, name="ticketHub"),
]
