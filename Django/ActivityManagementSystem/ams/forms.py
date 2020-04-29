from django.forms import ModelForm
from .models import Child, Activity
from django import forms
from Assignment_1 import settings


# Create the form class.


class DateInput(forms.DateInput):
    input_type = 'date'


class ChildForm(ModelForm):
    class Meta:
        model = Child
        fields = ['name', 'age', 'date_of_birth',
                  'address', 'contact']
        widgets = {
            'date_of_birth': DateInput(),
        }


# class ChildUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Child
#         fields = ['name', 'age', 'date_of_birth', 'address', 'contact']
#         widgets = {
#             'date_of_birth': DateInput(),
#         }

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class ActivityForm(ModelForm):
    class Meta:
        model = Activity

        fields = ['name', 'start_time', 'end_time']
        widgets = {
            'start_time': DateTimeInput(),
            'end_time': DateTimeInput(),
        }