from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .decorator import *
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@unauthenticated_user
def Login(request):
    try:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("myDrive")
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials!'})
        return render(request,"login.html")
    except Exception as e:
        print(e)
        return HttpResponse(404)

@unauthenticated_user
def SignUp(request):
    try:
        if request.method == "POST":
            username=request.POST.get('username')
            email=request.POST.get('email')
            password1=request.POST.get('psw1')
            password2=request.POST.get('pasw2')
            # print(password1,password2)
            
            if password1 != password2:
                return render(request, 'signup.html', {'error_message': 'Miss match password!'})
            elif username == "" or email == "":
                return render(request, 'signup.html', {'error_message': 'all field needed!'})
            else:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                return redirect("login")
        return render(request,"signup.html")
    except Exception as e:
        print(e)
        return HttpResponse(404)

def MyDrive(request, parent_id=None):
    try:
        user=request.user #requesting authorised user
        if request.method == 'POST':
            name = request.POST.get('name') #requesting folder name
            file=request.FILES.get('file') #requesting file
            # print(file)
            parent_id = request.POST.get("parent_id")
            parent = None
            if parent_id: #checking id 
                parent = Folder.objects.get(id=parent_id)
            if file:
                folder = Folder(parent=parent,file=file,user=user)
            else:
                folder = Folder(name=name, parent=parent,user=user)
            # folder = Folder(name=name, parent=parent)
            folder.save() #saving file or folder  against user
            return redirect('myDrive', parent_id=parent_id) if parent_id else redirect('myDrive')

        parent = Folder.objects.get(id=parent_id) if parent_id else None #sending parent folders
        folders = Folder.objects.filter(parent=parent,user=user) #sending child folder against authorised user and parent folder
        return render(request, 'folders.html', {'parent': parent, 'folders': folders})
    except Exception as e:
        print(e)
        return HttpResponse(404)

def Delete(request,parent_id): #getting id from parameters
    try:
        # print(parent_id)
        folder=Folder.objects.get(id=parent_id)
        folder.delete()
        return redirect('myDrive')
    except Exception as e:
        print(e)
        return HttpResponse(404)

def Update(request,parent_id): #getting id from parameters
    try:
        # print(parent_id)
        if request.method=="POST":
            name = request.POST.get('name') #requesting updating name
            # print(name)
            folder=Folder.objects.get(id=parent_id)
            # print(folder.name)
            folder.name=name
            folder.save()
            return redirect("myDrive")
        else:
            folder=Folder.objects.get(id=parent_id)
            return render(request,"update.html",{"folder":folder}) #sending file details
    except Exception as e:
        print(e)
        return HttpResponse(404)

def Logout(request):
    logout(request)
    return redirect("login")