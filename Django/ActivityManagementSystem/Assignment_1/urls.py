
from django.contrib import admin
from django.urls import path
from ams import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('child/profile', views.child_profile, name='child-profile'),
    path('addactivity', views.add_activity, name='add-activity'),
    path('myprofile/', views.my_profile, name='my-profile'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('remove/child/', views.remove_child, name='remove-child'),
    path('update/child/', views.updateChild, name='update-child')




]
