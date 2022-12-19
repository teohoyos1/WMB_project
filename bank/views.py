from django.http import HttpResponse
from django.shortcuts import render, redirect   
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Person

# Create your views here.
def index(request):
    return render(request, 'home.html')


def signup_view(request):
    
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        print(request.POST)
        if request.POST['password'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'], email=request.POST['email'],
                                            first_name=request.POST['name'])
                user.save() 
            except Exception as e:
                print(f"ERROR BRO {e}")
                return render(request, 'signup.html', context)
            try:
                person = Person.objects.create(user=user, phone=request.POST['phone'])
                person.save()
            except Exception as e:
                print(f"ERROR BRO {e}")
                return render(request, 'signup.html', context) 
            
            #auth new user
            login(request, user)
            return redirect(index)
        else:
            return render(request, 'signup.html', context) 
        
    else:
        context={
                 'form': UserCreationForm
                }
        return render(request, 'signup.html', context)

def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('/')
        
    
    if request.method == 'POST':
        
        username = request.POST['username']
        pswd = request.POST['password']
        
        user = authenticate(request, username=username, password=pswd)
        if user is not None:
            login(request, user)
            return redirect(index)
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect(index)

        
    
        

    


    

    

#Se crearon los models en base a la imagen en desktop
#Sigue crear CRUD
#Integrar con Wpp
#Readme