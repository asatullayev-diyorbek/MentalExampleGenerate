from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Kirish muvaffaqiyatli!')
            return redirect('menu')
        else:
            messages.error(request, 'Login yoki parol noto\'g\'ri. Iltimos, qaytadan urinib ko\'ring.')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('menu')
