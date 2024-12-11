from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm,CustomUserAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('proof')
        else:
            return HttpResponseRedirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            form = CustomUserAuthenticationForm()

    return render(request, 'authorization.html')

def registration_proof(request):
    return render(request, 'registration_proof.html')