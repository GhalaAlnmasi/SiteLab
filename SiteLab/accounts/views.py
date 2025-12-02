import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Profile, User


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 💡 يتم الآن تشفير كلمة المرور وحفظها بالكامل هنا
            user = form.save() 
            
            # إنشاء الملف الشخصي بعد حفظ المستخدم بنجاح
            Profile.objects.create(user=user) 
            
            messages.success(request, "Account created successfully!")
            return redirect("accounts:login_view")
    else:
        form = RegisterForm()

    return render(request, "accounts/sign-up.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts:profile_view")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login_view")


@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:

                with transaction.atomic():
                    form.save()

                messages.success(request, "Profile updated successfully!")
                return redirect("accounts:profile_view")
            except Exception:
                messages.error(request, "Error while updating profile. Please try again.")
    else:
        form = ProfileForm(instance=profile)

    colors = ['#F87171','#FBBF24','#34D399','#60A5FA','#A78BFA','#F472B6']
    random_color = random.choice(colors)

    return render(request, "accounts/profile.html", {
        "form": form,
        "random_color": random_color
    })

