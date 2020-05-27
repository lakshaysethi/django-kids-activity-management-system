
from django.contrib import admin
from django.urls import path

from ams import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('child/profile/', views.child_profile, name='child-profile'),
    path('addactivity/', views.add_activity, name='add-activity'),
    path('myprofile/', views.my_profile, name='my-profile'),
    path('remove/child/', views.remove_child, name = 'remove-child'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register-user'),
    
    path('update/child/', views.updateChild, name = 'update-child'),
    path('calendar/', views.calendar, name = 'calendar'),
    path('supervise/', views.supervise, name = 'supervise'),


    path('distance/',views.distance, name = 'distance'),



    path('forgot/',
        auth_views.PasswordResetView.as_view(template_name="forgot.html"),
        name="forgot"),

    path('reset_password_sent/',
            auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
            name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
        name="password_reset_confirm"),

    path('reset_password_complete/',
            auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
            name="password_reset_complete"),

]
