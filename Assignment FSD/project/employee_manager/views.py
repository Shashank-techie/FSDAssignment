from django.shortcuts import render, redirect
from .forms import UserLoginDetails, UserRegistrationDetails
from .models import manager_login
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.utils.timezone import now

def register(request):
    form = UserRegistrationDetails()

    if request.method == "POST":
        form = UserRegistrationDetails(request.POST)

        if form.is_valid():
            try:
                existingUser = manager_login.find_one({
                    'userEmail': form.cleaned_data['userEmail']
                })

                if existingUser:
                    messages.error(request, "Email already registered")
                    return render(request, "employee_manager/register.html", {"form": form})

                user = {
                    "f_name": form.cleaned_data["userName"],
                    "f_email": form.cleaned_data["userEmail"],
                    "f_pwd": make_password(form.cleaned_data["userPassword"]),
                    "created_at": now(),
                }

                manager_login.insert_one(user)
                messages.success(request, "Registration Successful!!")
                return redirect("login")

            except Exception as err:
                messages.error(request, f'An error occurred: {str(err)}')
                return render(request, 'user_auth/register.html', {'form': form})

    return render(request, "employee_manager/register.html", {"form": form})

def login(request):
    form = UserLoginDetails()

    if request.method == "POST":
        form = UserLoginDetails(request.POST)

        if form.is_valid():
            userName = form.cleaned_data['userName']
            userPassword = form.cleaned_data['userPassword']

            user = manager_login.find_one({'f_name': userName})
            print("Found user:", user)

            if user:
                stored_password = user.get('f_pwd')  # Changed from userPassword to f_pwd
                if check_password(userPassword, stored_password):
                    request.session["userInfo"] = {
                        "f_name": user["f_name"],
                        "f_pwd": user["f_pwd"],
                    }

                messages.success(request, "Login Successful!!")
                return redirect("home")
            else:
                messages.error(request, "Invalid Username or Password")
                return render(request, "employee_manager/login.html", {'form': form})    

    return render(request, "employee_manager/login.html", {'form': form})


# Function which will be called when the user is logging out
def logout(request):
    if 'userInfo' in request.session:
        del request.session['userInfo']
        messages.success(request, "Logged out successfully!")
    return redirect('login')