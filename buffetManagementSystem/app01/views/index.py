from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import LoginForm

def login(request):

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("username", "Username or Password is incorrect")
            return render(request, 'login.html', {'form': form})

        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}
        return redirect('/index/')
    return render(request, 'login.html', {'form': form})

def logout(request):
    """logout"""
    request.session.clear()
    return redirect('/login/')

def index(request):
    """index page"""
    return render(request, 'index.html')
