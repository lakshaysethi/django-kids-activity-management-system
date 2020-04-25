from django.forms import ModelForm
from django import forms
from .models import Child
from ass1 import settings



# class ChildUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Child
#         fields = ['name','age','date_of_birth','address','contact']
#         widgets = {
#             'date_of_birth': DateInput(),
#         }


class DateInput(forms.DateInput):
    input_type = 'date'
   

    

class ChildForm(ModelForm):
     class Meta:
        model = Child
        
        fields = ['name','age','date_of_birth','address','contact']
        
        widgets = {
            'date_of_birth': DateInput(),
        }
