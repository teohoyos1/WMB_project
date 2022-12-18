from django.shortcuts import render, redirect   
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    return render(request, 'home.html')

def sigup_view(request):
    return render(request, "signup.html")

def login_view(request):
    return render(request, "login.html")


def signup_add(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        
        return render(request, 'login.html', context={})
        

    


    

    

#Se crearon los models en base a la imagen en desktop
#Sigue crear CRUD
#Integrar con Wpp
#Readme