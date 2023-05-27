from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def guest_required(function =None, redirect_field_name =REDIRECT_FIELD_NAME,login_url='userlogin'):
    #actual_decorator user defined function
    actual_decorator = user_passes_test(lambda user:user.is_active and user.is_guest,login_url=login_url,redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator

def owner_required(function =None, redirect_field_name =REDIRECT_FIELD_NAME,login_url='userlogin'):
    #actual_decorator user defined function
    actual_decorator = user_passes_test(lambda user:user.is_active and user.is_owner,login_url=login_url,redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator



def superuser_required(function =None, redirect_field_name =REDIRECT_FIELD_NAME,login_url='userlogin'):
    #actual_decorator user defined function
    actual_decorator = user_passes_test(lambda user:user.is_active and user.is_superuser,login_url=login_url,redirect_field_name=redirect_field_name)
    if function:
        return actual_decorator(function)
    return actual_decorator