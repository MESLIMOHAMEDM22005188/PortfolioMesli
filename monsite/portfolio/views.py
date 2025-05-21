from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')

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
