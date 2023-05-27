from django.db import transaction
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from pg_main.models import PG_PostAds

# Create custom widget in your forms.py file.
class DateInput(forms.DateInput):
    input_type = 'date'

# -----------------------------------------------------------------------
class GuestRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User 
        fields = ('username','first_name','last_name','email','mobile_no','aadhar_no','birthdate','profile_image','password1','password2','password2')         
        widgets = {'birthdate': DateInput()}
                   
    @transaction.atomic
    def save(self):
        user = super(GuestRegistrationForm,self).save(commit=False)
        user.is_guest = True
        user.save()        
        return user
    
# -----------------------------------------------------------------------
class OwnerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User 
        fields = ('username','first_name','last_name','email','mobile_no','aadhar_no','birthdate','profile_image')          
        widgets = {'birthdate': DateInput()}
                   
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()        
        return user

# -----------------------------------------------------------------------
class AdminRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User 
        fields = ('username','first_name','last_name','email','mobile_no','aadhar_no','birthdate','profile_image')          
        widgets = {'birthdate': DateInput()}
                   
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_admin = True
        user.save()        
        return user

# -----------------------------------------------------------------------
class GuestUpdationForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username','first_name','last_name','email','mobile_no','aadhar_no','birthdate','profile_image')         
        widgets = {'birthdate': DateInput()}

# -----------------------------------------------------------------------
class OwnerUpdationForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username','first_name','last_name','email','mobile_no','aadhar_no','birthdate','profile_image')
        widgets = {'birthdate': DateInput()}

# -----------------------------------------------------------------------
class AdminUpdationForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = ('username','first_name','last_name','email','mobile_no','aadhar_no','birthdate','profile_image')
        widgets = {'birthdate': DateInput()}