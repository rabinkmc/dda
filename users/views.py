from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms


# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("dashboard")
