from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from museums.models import *
from django.contrib.auth.models import User


def home(request):
    museums = Museum.objects.all().order_by('name')
    return render(request,'index.html',{'museums':museums})

def login_view(request):
    '''
    For Sujoy, complete the login view.
    '''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = login(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password. Please enter carefully.'})
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})


def register_view(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
       
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                email = request.POST.get('email')
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=email,
                    password=form.cleaned_data['password1']
                )
                login(request, user)
                return redirect('home')
    else:
        form = UserCreationForm()
    return render(request,'registration/signup.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    return render(request,'profile.html')