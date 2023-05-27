import os

from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.views.generic import DeleteView,UpdateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .models import PG_Comments, PG_Facility_Master, PG_Amenities, PG_PostAds, PG_Images, PG_Facility, User
from .forms import FacilityMasterCreationForm,PGCreationForm,FacilityCreationForm, PGAmenitiesCreationForm, PGImagesCreationForm, PGCommentsCreationForm, ContactOwnerForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from user.decorators import guest_required,owner_required,superuser_required

from django.contrib.auth import login
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
# ==========================================================================
# PG_PostAds
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGCreateView(CreateView):
    form_class = PGCreationForm
    # second_form_class = PGAmenitiesCreationForm
    model = PG_PostAds, User #,PG_Amenities
    template_name = 'pg_dir/create_pg.html'
    success_url = '/user/owner/dashboard'    
   
    def form_valid(self,form):       
        email = self.request.user.email        
        message = 'Thank you for registering your PG in our PG Finder portal.'
        mail_response = sendMail(email,message)        
        if mail_response > 0:            
            form.instance.owner = self.request.user
            form.save()            
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page
    
# ------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGListView(ListView):

    model = PG_PostAds
    template_name = 'pg_dir/list_pg.html'
    context_object_name = 'pg_list'
    
    def get_queryset(self):
        return super().get_queryset().filter(owner_id=self.request.user.id)    
    
# ------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGDeleteView(DeleteView):
    model = PG_PostAds

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
      
    success_url = '/user/owner/dashboard'

# ------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGUpdateView(UpdateView):
    model = PG_PostAds
    form_class = PGCreationForm
    template_name = 'pg_dir/update_pg.html'
    success_url = '/user/owner/dashboard'

# ------------------------------------------------------------------------
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class PGDetailView(DetailView):
    model = PG_PostAds
    template_name = 'pg_dir/details_pg.html'
    context_object_name = 'pg_details'

    def get(self, request, *args, **kwargs):
        temp = []
        PGAmenities = PG_Amenities.objects.filter(pg_id=self.kwargs['pk']).values()
        
        if PGAmenities.exists():
            if PGAmenities[0]['ac'] == True:
                temp.append("AC , ")
            if PGAmenities[0]['wifi'] == True:
                temp.append("Wifi , ")
            if PGAmenities[0]['laundry'] == True:
                temp.append("Laundry , ")
            if PGAmenities[0]['attached_washroom'] == True:
                temp.append("Attached Washroom , ")
            if PGAmenities[0]['room_cleaning'] == True:
                temp.append("Room Cleaning , ")
            if PGAmenities[0]['washing_machine'] == True:
                temp.append("Washing Machine , ")
            if PGAmenities[0]['full_water_supply'] == True:
                temp.append("Full Water Supply , ")
            if PGAmenities[0]['food'] == True:
                temp.append("Food , ")
            if PGAmenities[0]['kitchen_appliances'] == True:
                temp.append("Kitchen Appliances , ")
            if PGAmenities[0]['parking'] == True:
                temp.append("Parking , ")
            if PGAmenities[0]['wardrobe'] == True:
                temp.append("Wardrobe , ")
            if PGAmenities[0]['furnished_room'] == True:
                temp.append("Furnished Room , ")
            if PGAmenities[0]['cctv_security'] == True:
                temp.append("CCTV Security , ")
        
        else:
            temp.append("Owner has not specified available amenities")

        return render(request, 'pg_dir/details_pg.html', {
            'pg_details': self.get_object(),            
            'PGAmenities':temp
        })

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGAmenitiesAddView(CreateView):
    model = PG_Amenities
    form_class = PGAmenitiesCreationForm
    template_name = 'pg_dir/add_pg_amenities.html'
    success_url = '/user/owner/dashboard'

    def form_valid(self, form):
        form.instance.pg = PG_PostAds.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

# ----------------------------------------------------------------

@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGAmenitiesUpdateView(UpdateView):

    model = PG_Amenities
    form_class = PGAmenitiesCreationForm
    template_name = 'pg_dir/update_pg_amenities.html'
    # success_url = '/user/owner/dashboard'

    def get_success_url(self):
        PGID = PG_Amenities.objects.filter(id=self.kwargs['pk']).values()
        # print("PG ***** ",PGID)
        # print("PGID ***** ",PGID[0]['pg_id'])
        return reverse_lazy('detail_pg_amenities', kwargs={'pk': PGID[0]['pg_id']})
    
# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGAmenitiesDetailView(DetailView):

    model = PG_Amenities
    template_name = 'pg_dir/detail_pg_amenities.html'
    context_object_name = 'pg_amenities_details'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        try:
            obj = self.model.objects.get(pg_id=pk)
        except PG_Amenities.DoesNotExist:
            obj = None

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['PGID'] = self.kwargs.get('pk')
        return context

# ----------------------------------------------------------------

@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGImagesAddView(CreateView):
    model = PG_Images
    form_class = PGImagesCreationForm
    template_name = 'pg_dir/add_pg_images.html'
    # success_url = '/user/owner/dashboard' # need to redirect to the same page

    def get_success_url(self):
        return reverse_lazy('add_pg_images', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.pg = PG_PostAds.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin')],name='dispatch')
class PGCommentView(CreateView, ListView):
    model = PG_Comments
    form_class = PGCommentsCreationForm
    template_name = 'pg_dir/add_comment.html'
    # success_url = reverse_lazy('pg_comments') # need to redirect to the same page

    # For CreateView
    def get_success_url(self):
        print('get_success_url')
        return reverse_lazy('pg_comments', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        print('form_valid')
        form.instance.pg = PG_PostAds.objects.get(pk=self.kwargs['pk'])
        form.instance.guest_id = self.request.user.id
        return super().form_valid(form)

    # For ListView
    context_object_name = 'PGComment'
    def get_queryset(self):
        return super().get_queryset().filter(pg=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().values()
        return context

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin')],name='dispatch')
class PGCommentsDeleteView(DeleteView):
    model = PG_Comments
    # success_url = '/pg_main/pg/comments'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
    
    def get_success_url(self):
        PGID = PG_Comments.objects.filter(id=self.kwargs['pk']).values()
        # print("PG *********** ",PGID)
        # print("PGID *********** ",PGID[0]['pg_id'])
        return reverse_lazy('pg_comments', kwargs={'pk': PGID[0]['pg_id']})
    
   
# ----------------------------------------------------------------

class ContactOwnerView(FormView):

    model = PG_PostAds,User
    template_name = 'guest_dir/contact_owner.html'
    form_class = ContactOwnerForm    
    success_url = '/pg_main/pg/contact_owner/success'       
            
    def form_valid(self, form):            
        print(form.cleaned_data)        
        # guest details
        guest_email = self.request.user.email                 
        guest_name = self.request.user.first_name                 

        # contact owner form message 
        guest_email_subject = form.cleaned_data.get('subject')                         
        guest_email_message = str(form.cleaned_data.get('message'))
        
        # owner email details and PG Details
        owner_id = PG_PostAds.objects.filter(id=self.kwargs['pk']).values('pg_name','owner_id')                      
        ownerObj = User.objects.filter(id=owner_id[0]['owner_id']).values()        
        owner_email = ownerObj[0]['email']
        # print(owner_email)
        
        # mail message merging
        email = owner_email        

        initial_message = "Greeting from PG Finder Admin!!! \nThere is a good news for you. \nCustomer "+ guest_name + " wants to contact you and negotiate with you regarding your PG " + owner_id[0]['pg_name']
        guest_details_message = "\n\nGuest details are as follow: \nName: - " + guest_name + "\nEmail: - " + guest_email + "\nSubject: - " + guest_email_subject + "\nMessage: - " + guest_email_message
        concluding_message = "\n\nKindly reply to their message. \nTherefore contact " + guest_name + " on their email ID: - " + guest_email + "\n\nThank You !!!"        
        message = initial_message + guest_details_message + concluding_message
                
        # send mail mechanism
        print(email)        
        print(message) 
        mail_response = sendMail(email,message)
        if mail_response > 0:            
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page
    
# ----------------------------------------------------------------
class ContactOwnerSuccessView(TemplateView):
    template_name = 'guest_dir/contact_owner_success.html'

# ----------------------------------------------------------------
# @method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
# class PGAvailStatusUpdateView(UpdateView):
#     model = PG_PostAds
#     form_class = PGCreationForm
#     template_name = 'owner_dir/owner_dashboard.html'
#     success_url = '/user/owner/dashboard'

    
        
# ----------------------------------------------------------------
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class AdminPGListView(ListView):    
    
    model = PG_PostAds,User, PG_Amenities

    def get(self, request, *args, **kwargs):    

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
            return render(request, self.template_name,{
                'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj
            })               
      
    template_name = 'admin_dir/admin_pg_list.html'

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin')],name='dispatch')
class PGImagesListView(ListView):
    model = PG_Images
    template_name = 'pg_dir/pg_images.html'
    context_object_name = 'PGImages'
    
    def get_queryset(self):
        return super().get_queryset().filter(pg=self.kwargs['pk'])    


# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGImagesDeleteView(DeleteView):
    model = PG_Images
    # success_url = '/pg_main/pg/comments'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
    
    def get_success_url(self):
        PGID = PG_Images.objects.filter(id=self.kwargs['pk']).values()
        # print("PG ***** ",PGID)
        # print("PGID ***** ",PGID[0]['pg_id'])
        return reverse_lazy('view_pg_images', kwargs={'pk': PGID[0]['pg_id']})







































































# -------------------------------------------------
def sendMail(email,message): #,request):
    subject = 'PGFinder Admin'      
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]    
    mail_response = send_mail(subject,message,email_from,recipient_list) #recipient_list)
    
    return mail_response
    # if mail_response > 0:
    #     return HttpResponse('Mail Sent')
    # else:
    #     return HttpResponse('Failed to send mail')


# ==========================================================================
# pg_facility_master
class FacilityCreateView(CreateView):
    
    form_class = FacilityMasterCreationForm
    model = PG_Facility_Master
    template_name = 'pg_dir/create_facility.html'
    success_url = '/pg_main/facility/list'

    def form_valid(self, form):
        return super().form_valid(form)

# ------------------------------------------------------------------------
class FacilityDeleteView(DeleteView):
    model = PG_Facility_Master

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
      
    success_url = '/pg_main/facility/list'

# ------------------------------------------------------------------------
class FacilityUpdateView(UpdateView):
    model = PG_Facility_Master
    form_class = FacilityMasterCreationForm
    template_name = 'pg_dir/update_facility.html'
    success_url = '/pg_main/facility/list'

# ------------------------------------------------------------------------
class FacilityListView(ListView):

    model = PG_Facility_Master
    template_name = 'pg_dir/list_facility.html'
    context_object_name = 'facility_list'
    
    def get_queryset(self):
        return super().get_queryset()  