
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authontication.forms import RegisterForm,loginform,UpdateProfileForm,Password_change_form
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request,'Rregistration successful!!')
            return redirect('signin')
    else:
        form=RegisterForm()     
    return render(request,'signup.html',{'form':form})

def signin(request):
    if request.method=='POST':
        form=loginform(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Welcome,{user.username} ')
                return redirect('profile')
            else:
                messages.error(request,'Invalid username or password')
    else:
        form=loginform()
    return render(request,'signin.html',{'form':form})

@login_required(login_url='signin')
def profile(request):
    return render(request,'profile.html')

@login_required(login_url='signin')
def update_profile(request):
    if request.method=='POST':
        form=UpdateProfileForm(request.POST,instance=request.user)  #it will take curently active that is update thats use of instance
        if form.is_valid():
            form.save()
            messages.success(request,'Profile update successfully')
            return redirect('profile')
    else:
        form=UpdateProfileForm(instance=request.user)
    return render(request,'update_profile.html',{'form':form})

#update Password
@login_required
def update_password(request):
    if request.method=='POST':
        form=Password_change_form(user=request.user ,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request.user) #make this user to stay as logged in
            messages.success(request,'Password Update successfully')
            return redirect('profile')
    else:
        form=Password_change_form(user=request.user)
    return render(request,'update_password.html',{'form':form})

@login_required(login_url='signin')
def signout(request):
    return render(request,'profile.html',{'user':request})
def signout(request):
    logout(request)
    return redirect('signin')

@login_required
def redirect_dashboard(request):
    user = request.user
    if user.is_farmer:
        return render(request, 'farmer_dashboard.html')
    elif user.is_consumer:
        return render(request, 'consumer_dashboard.html')
    else:
        return render(request, 'main.html')
