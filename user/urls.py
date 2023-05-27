from django.contrib import admin
from django.urls import path,include
from .views import GuestRegistrationView,OwnerRegistrationView, UserLoginView, OwnerDashboardView, GuestDashboardView, UserRegistrationChoiceView,GuestProfileUpdationView, OwnerProfileUpdationView, AdminDashboardView, AdminProfileUpdationView, AdminRegistrationView, pg_availstatus_change_view
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from . import views # for mail

urlpatterns = [
    
    # registration
    path('guestregistration/',GuestRegistrationView.as_view(),name='guestregistration'),
    path('guestprofileupdation/',GuestProfileUpdationView.as_view(),name='guestprofileupdation'),
    
    path('ownerregistration/',OwnerRegistrationView.as_view(),name='ownerregistration'),
    path('ownerprofileupdation/',OwnerProfileUpdationView.as_view(),name='ownerprofileupdation'),

    path('adminregistration/',AdminRegistrationView.as_view(),name='adminregistration'),
    path('adminprofileupdation/',AdminProfileUpdationView.as_view(),name='adminprofileupdation'),

    # change password
    path('guest/changepassword/',PasswordChangeView.as_view(template_name = 'guest_dir/guest_changepassword.html', success_url = '/user/guest/changepassword/done'),name='guestchangepassword'),
    path('guest/changepassword/done',PasswordChangeDoneView.as_view(template_name = 'guest_dir/guest_changepassword_done.html'),name='guestchangepassworddone'),
    
    path('owner/changepassword/',PasswordChangeView.as_view(template_name = 'owner_dir/owner_changepassword.html', success_url = '/user/owner/changepassword/done'),name='ownerchangepassword'),
    path('owner/changepassword/done',PasswordChangeDoneView.as_view(template_name = 'owner_dir/owner_changepassword_done.html'),name='ownerchangepassworddone'),
    path('pg/availstatus/change',pg_availstatus_change_view, name = "pg_availstatus_change"),
    
    path('admin/changepassword/',PasswordChangeView.as_view(template_name = 'admin_dir/admin_changepassword.html', success_url = '/user/admin/changepassword/done'),name='adminchangepassword'),
    path('admin/changepassword/done',PasswordChangeDoneView.as_view(template_name = 'admin_dir/admin_changepassword_done.html'),name='adminchangepassworddone'),

    # authenticationn
    path('userlogin/',UserLoginView.as_view(),name='userlogin'),
    path('userlogout/',LogoutView.as_view(),name='userlogout'),
    path('userregistrationchoice/',UserRegistrationChoiceView.as_view(),name='userregistrationchoice'),
    # path('sendmail/',views.sendMail,name='sendmail'),

    # dashboard
    path('guest/dashboard/',GuestDashboardView.as_view(),name='guest_dashboard'),
    path('owner/dashboard/',OwnerDashboardView.as_view(),name='owner_dashboard'),
    path('admin/dashboard/',AdminDashboardView.as_view(),name='admin_dashboard'),
    
    # Forgot Password
    path('password_reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    
]
