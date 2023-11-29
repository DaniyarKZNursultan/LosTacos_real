from django.shortcuts import render

def index(request):
    return render(request, 'lostacos/main.html')

def about(request):
    return render(request, 'lostacos/about.html')
