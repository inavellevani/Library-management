from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.views import View
from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User


class RegisterView(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')  # Change 'home' to your desired redirect URL
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
            if user.is_staff:
                return redirect('book-list-create')  # Redirect staff to book-list-create
            else:
                return redirect('user-profile')  # Redirect regular users to book-list
        return render(request, 'login.html', {'form': form})


class LogoutView(LogoutView):
    def logout_view(self, request):
        if request.method == 'POST':
            request.user.auth_token.delete()
            return JsonResponse({'success': True, 'message': 'Logged out successfully.'})
        return JsonResponse({'error': 'Invalid request method.'}, status=400)