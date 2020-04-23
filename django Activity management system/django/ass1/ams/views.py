from django.shortcuts import render



def home(request):
    return render(request,'home.html')



def child_profile(request):
    return render(request,'child-profile.html')


