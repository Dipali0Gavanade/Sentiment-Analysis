from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from account.models import Role, Profile
from django.db.models import Q
from django.contrib import messages

# Create your views here.
def insertRoles():
    roles = Role.objects.count()
    if(roles < 1):
        role = Role()
        role.name = 'Admin'
        role.save()
        role = Role()
        role.name = 'User'
        role.save()

def insertAdmin():
    profiles = Profile.objects.count()
    if(profiles < 1):
        profile = Profile()
        profile.name = 'Admin'
        profile.username = 'admin'
        profile.password = 'admin@123'
        profile.role = Role.objects.get(pk = 1)
        profile.save()

def login(request):
    content = {}
    insertRoles()
    insertAdmin()
    content['title'] = 'Login'
    if(request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        profile = Profile.objects.filter(username = username, password = password).first()
        if(profile):
            request.session['account_name'] = profile.name
            request.session['account_id'] = profile.id
            request.session['account_role'] = profile.role_id
            if(profile.role_id == 1):
                return HttpResponseRedirect(reverse('admin-train'))
            else:
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "Credentials provided does not matched in our records.")
    return render(request, 'account/login.html', content)

def signup(request):
    content = {}
    insertRoles()
    insertAdmin()
    content['title'] = 'Sign up'
    if(request.method == 'POST'):
        username = request.POST['username']
        name = request.POST['name']
        password = request.POST['password']

        checkUsername = Profile.objects.filter(username = username).first()
        if(checkUsername):
            messages.error(request, f"{username} already exists.")
        else:
            profile = Profile()
            profile.name = name.title()
            profile.username = username.lower()
            profile.password = password
            profile.role = Role.objects.get(pk=2)
            profile.save()
            messages.success(request, 'Accout created. You can login now')
            return HttpResponseRedirect(reverse('account-login'))
    return render(request, 'account/signup.html', content)


def logout(request):
    del request.session['account_name']
    del request.session['account_role']
    del request.session['account_id']
    messages.success(request, "You are logged out!.")
    return HttpResponseRedirect(reverse('account-login'))
