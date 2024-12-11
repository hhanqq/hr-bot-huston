from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm


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
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
            return render(request, 'authorization.html')

    return render(request, 'authorization.html')

def registration_proof(request):
    return render(request, 'registration_proof.html')