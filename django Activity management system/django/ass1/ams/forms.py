from django.forms import ModelForm
from django import forms
from .models import Child
from ass1 import settings





class DateInput(forms.DateInput):
    input_type = 'date'
   

    

class ChildForm(ModelForm):
     class Meta:
        model = Child
        
        # date_of_birth = forms.DateField(
        # widget=forms.DateInput(format='%d-%m-%Y'),
        # input_formats=('%d-%m-%Y', )
        # )
        fields = ['name','age','date_of_birth','address','contact']
        
        widgets = {
            'date_of_birth': DateInput(),
        }
