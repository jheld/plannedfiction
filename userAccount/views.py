from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response
# Create your views here.
    

def my_login(request):
    print(request.POST)
    username = ''
    if 'username' in request.POST:
        username = request.POST['username']
    else:
        username = 'jason'
    password = ''
    if 'password' in request.POST:
        password = request.POST['password']
    else:
        password = 'letmein88'
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return render(request,'pieces.html',{})
        else:
            # Return a 'disabled account' error message
            return render(request,'registration/login.html',{'error':'disabled account'})
    else:
        # Return an 'invalid login' error message.
        return render(request,'registration/login.html',{'error':'invalid login','next':'/'})

def my_logout(request):    
    logout(request)
    return render(request,'registration/login.html',{})
