from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from users.forms import CustomUserCreationForm, CustomAuthenticationForm


class RegisterView(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your desired redirect URL
        return render(request, 'register.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book-list-create')  # Change 'home' to your desired redirect URL
        return render(request, 'login.html', {'form': form})
