from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import User,Role,Activity,Child
from django.db import IntegrityError
from datetime import datetime,timedelta
from datetime import time
from ams import forms
from django.utils import timezone
from django.http import JsonResponse

current_week = timezone.now().isocalendar()[1] -1

def current_week_setter(current_week,request):
    if request.method == 'POST'  and request.POST.get('week') is not None:
        week = request.POST.get('week')
        current_week = request.POST['current_week']
        print('beforer the week was '+current_week)

        if week == 'next-week':
            current_week = str(int(current_week) +1)
        if week == 'last-week':
            current_week = str(int(current_week) -1)
    return current_week


def supervise(request):
    if request.method == 'POST':
        try:
            activityId = request.POST.get('activityId')
            selectedActivity = Activity.objects.filter(id=activityId).first()
            request.user.myActivities.add(selectedActivity)
            messages.add_message(request,messages.SUCCESS, f'You are now a supervisor for {selectedActivity}')
        except ValueError:
            console.log('failed')
            messages.add_message(request,messages.INFO, f'Failed to supervise')
            return redirect('home')
    return redirect('my-profile')



def home(request):
    current_week2 = current_week
    try:
        userrole = request.user.roles.first().id
    except:
        userrole = '3'
    af = forms.ActivityForm()
    allActivities = Activity.objects.all()
   
    context = dict()

    current_activities =[]
    if request.method == 'GET'
		for activity in allActivities:
			if str(activity.get_week()) == str(int(current_week)+1):
				current_activities.append(activity)
		
    try:
        print('in the all activities the first activity is in the week of'+ str(allActivities.first().get_week()))
    except:
        print('no activities')
    
    
    
    if request.method == 'POST':
        if request.method == 'POST' and request.POST.get('week') is not None:
            current_week2 =current_week_setter(current_week,request)
            for activity in allActivities:
                if str(activity.get_week()) == str(int(current_week2)+1):
                    current_activities.append(activity)
        if request.POST.get('form-type') == 'remove-activity' and request.POST.get('form-type') is not None:
            activityId = request.POST.get('activityId')
            
            activity = Activity.objects.filter(id=activityId).delete()
            if activity is not None:
                messages.add_message(request, messages.SUCCESS, "Activity Delete Successful")
            else:
                messages.add_message(request, messages.INFO, "Activity Delete Unsuccessful")
            return redirect('home')
            
        if request.POST.get('form-type') == 'update-activity' and request.POST.get('form-type') is not None:
            activityId = request.POST.get('activityId')
            a1 = Activity.objects.filter(id=activityId).first()
            a1name = a1.name
            af = forms.ActivityForm(request.POST, instance=a1)
            if  af.is_valid():       
                a2 = af.save()
                messages.add_message(request,messages.SUCCESS, f'{a1name}\'s details have been Updated Successfully to {a2.name}!')
                return redirect('home')
            else:
                af = forms.ActivityForm()
                messages.add_message(request,messages.INFO, 'Failed to update activity details.')


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
            
        if request.POST.get('duration') is not None:
            print("adding activity...")
            af = forms.ActivityForm(request.POST)
            if af.is_valid():
                activity = af.save()
                messages.add_message(request, messages.SUCCESS,"Activity added successfully")
            else:
                messages.add_message(request, messages.INFO,"Activity  Failed")
    
            #print(activity,activity.get_week())
    print('current activities are :'  )
    print(current_activities)
    if current_week2 is not None:
        print('now the week is '+str(current_week2))

    context = {'userrole':userrole,'includeNav':True,'form':af}
    context['allActivities'] = current_activities
    context['current_week'] = current_week2

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
    current_week2 = current_week 
    myCurrentWeeksActivities=[]
    if request.method == 'GET':
        for activity in request.user.myActivities.all():
            if str(activity.get_week()) == str(int(current_week)+1):
                print(f'matched!! for {activity} loll')
                myCurrentWeeksActivities.append(activity)
   
    
    cf = forms.ChildForm()
    if request.method == 'POST' and request.POST.get('date_of_birth')is not None:
        cf = forms.ChildForm(request.POST)
        if cf.is_valid():
            child = cf.save()
            request.user.myChildren.add(child)
            messages.add_message(request, messages.SUCCESS, "Child Added Successfully")
        else:
            messages.add_message(request, messages.INFO, "Child Add Failed")
    myChildren = request.user.myChildren.all()
    if request.method == 'POST' and request.POST.get('week') is not None:
        cwfpr = request.POST.get('current_week')
        # current week from post request = cwfpr
        current_week2 = current_week_setter(str(cwfpr),request)
        for activity in request.user.myActivities.all():
            if str(activity.get_week()) == str(int(current_week2)+1):
                myCurrentWeeksActivities =[]
                print('matched!! loll')
                myCurrentWeeksActivities.append(activity)  
    context= {'userrole':userrole,'includeNav': True, 'myChildren': myChildren,'form':cf}
    context['myCurrentWeeksActivities'] = myCurrentWeeksActivities
    context['current_week'] = current_week2
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
    except ValueError:
        messages.add_message(request, messages.INFO, "Please Enter your details")
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





def calendar(request):
    # set sratrdate should be from request params but for now chill
    start_date = datetime.today()

    # set variable to start at start_date
    day = start_date 
    
    # row wise data
    rwd = []

    five_week_days = []
    five_week_days_strings =[]
    
    
    # populating the 5 days
    for number in range(0,5):
        five_week_days.append(day)
        day_str = day.strftime('%d-%m-%Y')
        five_week_days_strings.append(day_str)
        day += timedelta(days=1)
    
    for hour in range(8,22):
        
        time_str = f'{hour}:00 - {hour+1}:00'
        if hour <10:
            hour =f'0{hour}'
        else:
            hour = f'{hour}'
        start_time_being_checked = time.fromisoformat(hour+':00:00')
        row = {'time':time_str}
        count = 1
        for aday in five_week_days:
            allActivitiesOnThisDay = Activity.objects.filter(date=aday)
            for activity in allActivitiesOnThisDay:
                if activity.start_time.hour == start_time_being_checked.hour:
                    row[f'a{count}']=activity
            count +=1
        rwd.append(row)
    dates_for_nav={'start_date':start_date}
    end_date = start_date+timedelta(days=4)
    dates_for_nav['end_date'] = end_date

    context = {'row_wise_data':rwd,'next_five_week_days':five_week_days_strings,'includeNav':True,'dates':dates_for_nav}
    return render(request,'calendar.html',context)




