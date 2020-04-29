from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User,Role,Activity,Child
from django.db import IntegrityError

from ams import forms




def home(request):
    try:
        userrole = request.user.roles.first().id
    except:
        userrole = '3'
    af = forms.ActivityForm()
    allActivities = Activity.objects.all()
    if request.method == 'POST':
        if request.POST.get('childId') is not None:
            try:
                childId= request.POST.get('childId')
                activityId= request.POST.get('activityId')
                selectedChild = Child.objects.filter(id=childId).first()
                selectedActivity = Activity.objects.filter(id=activityId).first()
                selectedChild.enrolled_activities.add(selectedActivity)
                messages.add_message(request, messages.SUCCESS, f'{selectedChild.name} has been enrolled in {selectedActivity.name}')
            except:
                messages.add_message(request, messages.INFO, f'FAILED to enroll child')
            context = {'userrole':userrole,'includeNav':True,'child':selectedChild,'allActivities': allActivities}
            response = child_profile(request, context)
            return response
            
        else:
            af = forms.ActivityForm(request.POST)
            if af.is_valid():
                activity = af.save()
                messages.add_message(request, messages.SUCCESS,"Activity added successfully")
            else:
                messages.add_message(request, messages.INFO,"Activity  Failed")
    
    context = {'userrole':userrole,'includeNav':True,'form':af,'allActivities': allActivities}
    return render(request,'home.html',context)



def child_profile(request,newContext={}):
    context ={'includeNav':True}
    if request.method == 'POST':
        child = request.user.myChildren.all().filter(id=request.POST.get('childId')).first()
        context = {'includeNav':True,'child':child }
    
    return render(request,'child-profile.html',context)


def my_profile(request):
    try:
        userrole = request.user.roles.first().id
    except:
        userrole = '3'
    cf = forms.ChildForm()
    if request.method == 'POST':
        cf = forms.ChildForm(request.POST)
        if cf.is_valid():
            child = cf.save()
            request.user.myChildren.add(child)
            messages.add_message(request, messages.SUCCESS, "Child Added Successfully")
        else:
            messages.add_message(request, messages.INFO, "Child Add Failed")
    myChildren = request.user.myChildren.all()
    context= {'userrole':userrole,'includeNav': True, 'myChildren': myChildren,'form':cf}
    return render(request, 'my-profile.html',context)


def remove_child(request):
    if request.method == 'POST':
        childId= request.POST.get('childId')
        child = request.user.myChildren.filter(id=childId).delete()
        if child is not None:
            messages.add_message(request, messages.SUCCESS, "Child Delete Successful")
        else:
            messages.add_message(request, messages.INFO, "Child Delete Unsuccessful")
    return redirect('my-profile')

def add_activity(request):
    return render(request,'add-activity.html',{'includeNav':True})





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # A backend authenticated the credentials
            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, "please check your username and/or password")
    


    return render(request,'login.html',{'includeNav':False})





def logout_view(request):
    if (request.user.is_authenticated):
        logout(request)
    return redirect('login')

def register_view(request):
    if(request.user.is_authenticated):
        return redirect('home')
    try:
        if (request.method == 'POST'):
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            userType = request.POST.get("userType")
            user = User.objects.create_user(username, email, password)
            if user is not None:
               #messages.add_message(request, level, message, extra_tags='', fail_silently=False)
                user.roles.add(Role.objects.get(id=userType))
                messages.add_message(request, messages.INFO, "your account was created successfully please log in now")
                # A backend authenticated the credentials
                return redirect( 'login')
    except IntegrityError:
        messages.add_message(request, messages.INFO, "That Username is taken please try another username")

    return render(request,'register.html',{'includeNav':False})



def updateChild(request):
    if (not request.user.is_authenticated):
        return redirect('home')
    
    if request.method == 'POST':
        childId = request.POST.get('childId')
        child = request.user.myChildren.filter(id=childId).first()
        cf = forms.ChildForm(request.POST, instance=child)
        if  cf.is_valid():       
            cf.save()
            messages.add_message(request,messages.SUCCESS, f'{child.name}\'s details have been Updated Successfully!')
            return redirect('my-profile')
    else:
        cf = forms.ChildForm()
        messages.add_message(request,messages.INFO, 'Failed to update child details.')
    
    
    context = {'form': cf}

    return render(request,'my-profile.html',context)