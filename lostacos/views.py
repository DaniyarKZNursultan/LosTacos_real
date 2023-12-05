from django.shortcuts import render

def index(request):
    data = {
        'title': 'Открытие новой точки!',
        'values': ['Some', 'hello', '123']
    }
    return render(request, 'lostacos/main.html', data)

def about(request):
    return render(request, 'lostacos/about.html')

def profile_view(request):
    return render(request, 'lostacos/profile.html')

def login(request):
    return render(request, 'registration/login.html')
