from .models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import CustomerRegisterationForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from core.models import UserProfile

# Create your views here.
# def register(request):
#     if request.method == 'POST':
#         form = CustomerRegisterationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # messages.success(request, 'Registration successful')
#             return redirect('app:user-dashboard')
#     else:
#         form = CustomerRegisterationForm()
#     return render(request, 'user_register.html',locals())


# Shop Registration View
def doctor_register(request):
    if request.method == "POST":
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True  # Automatically set is_shop=True
            user.is_user = False  # Ensure is_user=False
            user.save()
            return redirect('core:doctor-dashboard')   # Redirect to shop login page after registration
    else:
        form = CustomerRegisterationForm()
    return render(request, 'doctor_register.html', {'form': form})

# User Registration View
def user_register(request):
    if request.method == "POST":
        form = CustomerRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_user = True  # Automatically set is_user=True
            user.is_shop = False  # Ensure is_shop=False
            user.save()
            return redirect('core:user-dashboard')  # Redirect to user login page after registration
    else:
        form = CustomerRegisterationForm()
    return render(request, 'user_register.html', {'form': form})

# User Login View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)

                if user.is_doctor:
                    return redirect('core:doctor-dashboard')
                elif user.is_user:
                    # Check if user profile is filled
                    try:
                        profile = UserProfile.objects.get(user=user)
                        if not profile.is_filled:
                            return redirect('core:complete-profile')
                    except UserProfile.DoesNotExist:
                        # Create empty profile if it doesn't exist
                        UserProfile.objects.create(user=user, is_filled=False)
                        return redirect('core:complete-profile')
                    return redirect('core:user-dashboard')
                else:
                    # This will handle admins and other user types, you might want to redirect admins to an admin dashboard
                    messages.error(request, "Invalid user type.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('users:login')  # Redirect to login page after logout