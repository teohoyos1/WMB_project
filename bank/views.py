from django.http import HttpResponse
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect   
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Person, Wallet,Bank, Movement_wallet, Payment_category

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

#  wallet_f = models.ForeignKey(Bank, on_delete=models.CASCADE)
#     record_date = models.DateTimeField('record date')
#     before_value = models.IntegerField()
#     actual_value = models.IntegerField()
#     type_movement = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     payment_category_f

@login_required
def payment_page(request):
    
    if request.method == "POST":
        paid_value = request.POST['paid_value']
        description = request.POST['description']
        category_id = request.POST['category']
        
        if paid_value == "" and category_id == "":
            return render(request, 'payment.html')
        
        person = Person.objects.get(user=request.user)
        try:
            wallet = Wallet.objects.get(person_f=person)
            payment_category = Payment_category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            wallet = None
            payment_category=None
            
        if wallet is not None and payment_category is not None:
            before_value = 0
            type_movement = 1
            date_now = timezone.now()
            payment_object = Movement_wallet(wallet_f=wallet,record_date=date_now,before_value=before_value,actual_value=paid_value,type_movement=type_movement,description=description,payment_category_f=payment_category)
            payment_object.save()
            
        return redirect(payment_page)
    
    
    try:
        movement_wallet_object = Movement_wallet.objects.all()
    except Movement_wallet.DoesNotExist:
        movement_wallet_object = None
    
    try:
        category_object = Payment_category.objects.all()
    except Payment_category.DoesNotExist:
        category_object = None
        
    context = {
        'payment_category' : category_object,
        'movement_wallet' : movement_wallet_object
    }
        
    return render(request, 'payment.html',context=context)    

@login_required
def wallet_page(request):
    context = {}
    if request.method == "POST":
        balance = request.POST['balance']
        print(balance)
        if balance == "":
            return redirect(wallet_page)   
    
        try: 
            person_object = Person.objects.get(user=request.user)
            wallet_obj = Wallet.objects.get(person_f=person_object)
            
            wallet_obj.balance = balance
            wallet_obj.save()
            #wallet_object = Wallet.objects.all()[:1].get()
        except ObjectDoesNotExist:
            
            bank_object = Bank.objects.get(name='Bancolombia')
            person_object = Person.objects.get(user=request.user)
            wallet_object = Wallet(bank_f=bank_object,person_f=person_object,balance=balance)
            
            wallet_object.save()
            
            return redirect(wallet_page)
        
    try:
        person_object = Person.objects.get(user=request.user)
        wallet_object = Wallet.objects.get(person_f=person_object)
    except ObjectDoesNotExist:
        wallet_object = None
        
    context = {
        'wallet_object': wallet_object
    }

    return render(request, 'wallet.html',context=context)   
    
@login_required
def payment_category_page(request):
    
    if request.method == "POST":
        category_name = request.POST['category']
        
        if category_name == "":
            return render(request, "payment_category.html")
        
        category_object = Payment_category(name=category_name)
        category_object.save()
        
        return redirect(payment_category_page)    
    try:
        category_object = Payment_category.objects.all()
    except Payment_category.DoesNotExist:
        category_object = None
        
    context = {
        'category_object' : category_object
    }
    
    return render(request, "payment_category.html", context=context)

    

    
#SE CREO EL LOGIN Y REGISTRO
#SE CREO WALLET Y PAYMENT PAGES. 
#SE HACEN FUNCIONAR LOS FORMULARIOS DE WALLET Y PAYMENT
#CREAR LA INTEGRACION CON WPP O TELGRAM
#ORGANIZAR TODO EL DASHBOARD Y DEFINIR LAS ESTADISTICAS
#Readme