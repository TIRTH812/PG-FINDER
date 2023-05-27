from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render

from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.views.generic import ListView
from django.views.generic import UpdateView

from .models import User
from pg_main.models import *

from .forms import GuestRegistrationForm,OwnerRegistrationForm, OwnerUpdationForm, GuestUpdationForm, AdminRegistrationForm, AdminUpdationForm
from pg_main.forms import PGCreationForm

from django.conf import settings
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.decorators import guest_required,owner_required

# ************************************************

# ********************************


# Create your views here.
# ----------------------------------------------------------------
# @login_required
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class OwnerDashboardView(ListView):   

    model = PG_PostAds,User
    # form_class = PGAvailStatusUpdationForm
        
    def get(self, request, *args, **kwargs):            
        
        PGObj = PG_PostAds.objects.filter(owner_id=self.request.user.id) 
        
        PG_AmenitiesObj = PG_Amenities.objects.all().values()
               
        # Searching logic        
        input = request.GET.get('input')
        print(input)
        # PGObj=[]
        if input:
            PGObj = PG_PostAds.objects.filter(pg_name__icontains=input)
            print(PGObj)
            return render(request, self.template_name,{
                'PG':PGObj,'PG_Amenities':PG_AmenitiesObj
            })            
        else:
            # PGObj = PG_PostAds.objects.all() 
            PGObj = PG_PostAds.objects.filter(owner_id=self.request.user.id)             
            PGObj =  PGObj.order_by('id')
            return render(request, self.template_name,{
                'PG':PGObj, 'PG_Amenities':PG_AmenitiesObj
            })               
         
      
        # return render(request, 'owner_dir/owner_dashboard.html',{
        #     'PG':PGObj, 'PG_Amenities':PG_AmenitiesObj
        # })
            
    template_name = 'owner_dir/owner_dashboard.html'
    
# ----------------------------------------------------------------
# owner dashboard
def pg_availstatus_change_view(request):
        
    if request.method == 'GET':
            
        pg_id = request.GET.get('pg_id', '')
        # print("PG ID: - "+pg_id)

        pg_avail_status = request.GET.get('pg_avail_status', '')
        # print("PG avail status: - "+pg_avail_status)

        pg = PG_PostAds.objects.filter(id=pg_id).first()
        pg.avail_status = pg_avail_status 
        pg.save()
        
        return redirect('/user/owner/dashboard')        

    else:        
        print('inside else')
       
    return render(request, 'owner_dir/owner_dashboard.html')

# ----------------------------------------------------------------
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class GuestDashboardView(ListView):    
    
    model = PG_PostAds,User

    def get(self, request, *args, **kwargs):         

        # PGObj = PG_PostAds.objects.select_related('owner').all()
        PGObj = PG_PostAds.objects.all()#.values()
        OnwerObj = User.objects.all().filter(is_owner=True)
        
        UserObj = User.objects.filter(id=self.request.user.id).values()

        # sorting logic
        sort_by = self.request.GET.get('sort_by', '') #price
        sort_direction = self.request.GET.get('sort_direction', '')
        
        if sort_direction == 'asc' and sort_by == 'price':
            PGObj =  PGObj.order_by(sort_by)            
        elif sort_direction == 'desc' and sort_by == 'price':
            PGObj = PGObj.order_by(f'-{sort_by}')
        elif sort_direction == 'asc' and sort_by == 'no_of_rooms':
            PGObj =  PGObj.order_by(sort_by)  
        elif sort_direction == 'desc' and sort_by == 'no_of_rooms':
            PGObj =  PGObj.order_by(f'-{sort_by}')
        else:
            PGObj = PG_PostAds.objects.all()

        # Searching logic        
        input = request.GET.get('input' )
        print(input)
        # PGObj=[]
        if input:
            PGObj = PG_PostAds.objects.filter(pg_name__icontains=input)
            print(PGObj)
            return render(request, self.template_name,{
                'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj
            })            
        else:
            # PGObj = PG_PostAds.objects.all() 
            # my_object_json = json.dumps({
            #         'id': PGObj.id,
            #         # 'name': PGObj.pg_name,
            #      # add more fields as needed
            #         })
            
            return render(request, self.template_name,{
                'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj,
                # 'serialized_data':my_object_json,
            })               
         

        # return render(request, self.template_name,{
        #         'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj
        # }) 
    template_name = 'guest_dir/guest_dashboard.html'


# ----------------------------------------------------------------
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class AdminDashboardView(ListView):    
    
    model = PG_PostAds,User, PG_Amenities

    def get(self, request, *args, **kwargs):    

        PGObj = PG_PostAds.objects.all().values()
        UserObj = User.objects.all().values()
        PGAmenitiesObj = User.objects.all().values()

        # =======================
        # pie chart for gender_prefence category
        # -----------------------
        boys_type_pg = int(PG_PostAds.objects.filter(gender_preference = 'Boys').count())
        # print(type(boys_type_pg))

        girls_type_pg = int(PG_PostAds.objects.filter(gender_preference = 'Girls').count())
        # print(type(girls_type_pg))

        both_type_pg = int(PG_PostAds.objects.filter(gender_preference = 'Both').count())
        # print(type(both_type_pg))

        gender_label = ['Male','Female','Both']
        gender_value = [boys_type_pg,girls_type_pg,both_type_pg]
        # -----------------------

        # =======================
        # pie chart for PG available status
        # -----------------------
        PGavail_true = int(PG_PostAds.objects.filter(avail_status = 'True').count())
        # print(type(avail_true))

        PGavail_false = int(PG_PostAds.objects.filter(avail_status = 'False').count())
        # print(type(avail_false))

        PGavail_label = ['Available','Not Available']
        PGavail_value = [PGavail_true,PGavail_false]
        # -----------------------

        # =======================
        # doughnut chart for PG Occupacy
        # -----------------------
        PGoccupacy1 = int(PG_PostAds.objects.filter(occupacy = 'Single-bed').count())
        # print(type(PGoccupacy1))

        PGoccupacy2 = int(PG_PostAds.objects.filter(occupacy = 'Double-bed').count())
        # print(type(PGoccupacy2))

        PGoccupacy3 = int(PG_PostAds.objects.filter(occupacy = 'Triple-bed').count())
        # print(type(PGoccupacy3))

        PGoccupacyother = int(PG_PostAds.objects.filter(occupacy = 'other').count())
        # print(type(PGoccupacyother))

        PGoccupacy_label = ['Single-bed','Double-bed','Triple-bed','other']
        PGoccupacy_value = [PGoccupacy1,PGoccupacy2,PGoccupacy3,PGoccupacyother]
        # -----------------------

        # =======================
        # doughnut chart for PG House Type
        # -----------------------
        PGtypeApp = int(PG_PostAds.objects.filter(pg_type = 'Appartment').count())
        # print(type(PGtypeApp))

        PGtypeBang = int(PG_PostAds.objects.filter(pg_type = 'Banglows').count())
        # print(type(PGtypeBang))

        PGtypeRoof = int(PG_PostAds.objects.filter(pg_type = 'Roofhouse').count())
        # print(type(PGtypeRoof))

        PGtypeRow = int(PG_PostAds.objects.filter(pg_type = 'Rowhouse').count())
        # print(type(PGtypeRow))

        PGtypeTen = int(PG_PostAds.objects.filter(pg_type = 'Tenament').count())
        # print(type(PGtypeTen))

        PGtype_label = ['Appartment','Banglows','Roofhouse','Rowhouse','Tenament']
        PGtype_value = [PGtypeApp,PGtypeBang,PGtypeRoof,PGtypeRow,PGtypeTen]
        # -----------------------


        return render(request, self.template_name,{
            'PG':PGObj,'user':UserObj,'PGAmenities':PGAmenitiesObj,
            'gender_label': gender_label, 'gender_value': gender_value,
            'PGavail_label':PGavail_label,'PGavail_value':PGavail_value,
            'PGoccupacy_label':PGoccupacy_label,'PGoccupacy_value':PGoccupacy_value,
            'PGtype_label':PGtype_label,'PGtype_value':PGtype_value,
        }) 

    template_name = 'admin_dir/admin_dashboard.html'



# --------------------- ----------------------------------------------------
class GuestRegistrationView(CreateView):
    model = User
    form_class = GuestRegistrationForm
    template_name = 'user_dir/guest_registration.html'    
    success_url = '/user/userlogin/'

    def form_valid(self,form):
        email = form.cleaned_data.get('email') # ??
        message = 'Thank you for your registration in PG Finder as new Guest!!!'
        mail_response = sendMail(email,message)        
        if mail_response > 0:
            user = form.save()
            login(self.request,user)
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page
       

# -------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),guest_required],name='dispatch')
class GuestProfileUpdationView(UpdateView):
    model = User
    form_class = GuestUpdationForm
    template_name = 'user_dir/guest_profile_updation.html'    
    success_url = '/user/guest/dashboard'

    def get_object(self, queryset=None):
        return self.request.user
     
# -------------------------------------------------------------------------
class OwnerRegistrationView(CreateView):
    model = User
    form_class = OwnerRegistrationForm
    template_name = 'user_dir/owner_registration.html'
    success_url = '/user/userlogin/'


    def form_valid(self,form):
        email = form.cleaned_data.get('email') # ?? silently failed validation
        message = 'Thank you for your registration in PG Finder as a PG Owner!!!'
        mail_response = sendMail(email,message)        
        if mail_response > 0:
            user = form.save()
            login(self.request,user)
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page

# -------------------------------------------------------------------------

@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class OwnerProfileUpdationView(UpdateView):
    model = User
    form_class = OwnerUpdationForm
    template_name = 'user_dir/owner_profile_updation.html'        
    success_url = '/user/owner/dashboard/'

    def get_object(self, queryset=None):
        return self.request.user

# -------------------------------------------------------------------------

class AdminRegistrationView(CreateView):
    model = User
    form_class = AdminRegistrationForm
    template_name = 'user_dir/admin_registration.html'
    success_url = '/user/userlogin/'


    def form_valid(self,form):
        email = form.cleaned_data.get('email') # ?? silently failed validation
        message = 'Thank you for registration in PG Finder as a Admin User!!!'
        mail_response = sendMail(email,message)        
        if mail_response > 0:
            user = form.save()
            login(self.request,user)
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page

# -------------------------------------------------------------------------

@method_decorator([login_required(login_url='/user/userlogin')],name='dispatch')
class AdminProfileUpdationView(UpdateView):
    model = User
    form_class = AdminUpdationForm
    template_name = 'user_dir/admin_profile_updation.html'        
    success_url = '/user/admin/dashboard/'

    def get_object(self, queryset=None):
        return self.request.user

# -------------------------------------------------------------------------
class UserRegistrationChoiceView(ListView):
    model = User
    template_name = 'user_dir/user_registration_choice.html'

# -------------------------------------------------------------------------
class UserLoginView(LoginView):
    template_name = 'user_dir/user_login.html'
    #success_url = "/"
    
    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_guest:
                return '/user/guest/dashboard/'
            elif self.request.user.is_owner:
                return '/user/owner/dashboard/' 
            elif self.request.user.is_admin:
                return '/user/admin/dashboard/'
            else:
                return '/error/'

# -------------------------------------------------------------------------
# it should be possible to enable the mail on/off by admin
def sendMail(email,message): #,request):
    subject = 'Registration mail'    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    mail_response = send_mail(subject,message,email_from,recipient_list) #recipient_list)
    
    return mail_response
    # if mail_response > 0:
    #     return HttpResponse('Mail Sent')
    # else:
    #     return HttpResponse('Failed to send mail')
    


# -------------------------------------------------------------------------
def landingPage2(request):
    return render(request, 'index.html')

# -------------------------------------------------------------------------
def landingPage(request):
    return render(request, 'index2.html')

# -------------------------------------------------------------------------
def contactus(request):
    return render(request, 'contact-us.html')

# -------------------------------------------------------------------------
def aboutus(request):
    return render(request, 'about-us.html')
