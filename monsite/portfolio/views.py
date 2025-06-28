from django.http import Http404
from django.shortcuts import render
PROJECTS = {
    "Concurrency, Synchronization, Performance": {
        "description": "Projet sur la concurrence en C++ avec gestion des threads.",
        "gallery": [
            "assets/img/proj1.png",
            "assets/img/proj2.png",
        ],
        "hashtags": ["#C++", "#Multithreading", "#Performance"],
        "github": "https://github.com/moncompte/concurrency-project"
    },
    # Tu pourras en ajouter d'autres ici
}

def project_detail(request):
    title = request.GET.get('title')
    if not title or title not in PROJECTS:
        raise Http404("Projet introuvable")

    project = PROJECTS[title]
    return render(request, 'project_detail.html', {
        'title': title,
        'description': project['description'],
        'gallery': project['gallery'],
        'hashtags': project['hashtags'],
        'github': project['github']
    })
def accueil(request):
    return render(request, 'accueil.html')

def ticketHub(request):
    return render(request, 'ticketHub.html')

def mesPetitsCours(request):
    return render(request, 'mesPetitsCours.html')
def primaire(request):
    return render(request, 'primaire.html')

def cp(request):
    return render(request, 'cp.html')

def ce1(request):
    return render(request, 'ce1.html')

def ce2(request):
    return render(request, 'ce2.html')

def cm1(request):
    return render(request, 'cm1.html')

def cm2(request):
    return render(request, 'cm2.html')
def concurrency(request):
    return render(request, 'projects/concurrency.html')

def nim_ai(request):
    return render(request, 'projects/nim_ai.html')

def file_crud(request):
    return render(request, 'projects/file_crud.html')

def javafx_ui(request):
    return render(request, 'projects/javafx_ui.html')

def tickethub_ui(request):
    return render(request, 'projects/tickethub_ui.html')

def social_network(request):
    return render(request, 'projects/social_network.html')

def secretary_app(request):
    return render(request, 'projects/secretary_app.html')

def cybersecurity_insights(request):
    return render(request, 'projects/cybersecurity_insights.html')

def portfolio_site(request):
    return render(request, 'projects/portfolio_site.html')

def task_management(request):
    return render(request, 'projects/task_management.html')

def smartbudget_tracker(request):
    return render(request, 'projects/smartbudget_tracker.html')

def mailcli_sender(request):
    return render(request, 'projects/mailcli_sender.html')

def taskflow_poo(request):
    return render(request, 'projects/taskflow_poo.html')

def solar_system(request):
    return render(request, 'projects/solar_system.html')

def earthquake_analyzer(request):
    return render(request, 'projects/earthquake_analyzer.html')