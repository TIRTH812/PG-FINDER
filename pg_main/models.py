import uuid
from django.db import models
from user.models import User
# from geoposition.fields import GeopositionField

# Create your models here.

# -----------------------------------------------------------------------------------------------
class PG_Facility_Master(models.Model):
    facility_name = models.CharField(max_length=20)

    def __str__(self):
        return self.facility_name

    class Meta:
        db_table = 'pg_facility_master'


# -----------------------------------------------------------------------------------------------

gender_preference_choice = (
        ('select','select'),
        ('Boys','Boys'), 
        ('Girls','Girls'),
        ('Both','Both'), 
    )
occupacy_choice = (
        ('select','select'),
        ('Single-bed','Single-bed'), 
        ('Double-bed','Double-bed'), 
        ('Triple-bed','Triple-bed'), 
        ('other','other'), 
    )
pg_type_choice = (
        ('select','select'),
        ('Tenament','Tenament'), 
        ('Appartment','Appartment'), 
        ('Banglows','Banglows'), 
        ('Rowhouse','Rowhouse'), 
        ('Roofhouse','Roofhouse')
    )

class PG_PostAds(models.Model):
    # pg_id =  models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    
    pg_name = models.CharField(max_length=50,null=False)
    avail_status = models.BooleanField(default=False)
    gender_preference = models.CharField(max_length=15,null=False,choices=gender_preference_choice,default='select') # Boys, Girls, Both
    no_of_rooms = models.PositiveIntegerField(null=False)
    occupacy = models.CharField(max_length=10,null=False,choices=occupacy_choice,default='select') # single, double, triple, other
    price = models.PositiveIntegerField(null=False)
    description = models.TextField(null=True, blank=True)
    pg_type = models.CharField(max_length=15,choices=pg_type_choice,default='select') # predefine (Tenament, Appartment, Banglows, Rowhouse, Roofhouse,) choices = SEMESTER_CHOICES,
    
    website = models.CharField(max_length=50,null=True,blank=True)
    profile_image = models.ImageField(upload_to='pg_profile_img_dir/',null=True,blank=True)
    instructions_docs = models.FileField(upload_to='pg_instruct_file_dir/',null=True,blank=True)

    address = models.TextField(null = False)
    street = models.TextField(null = True)
    area = models.TextField(null = False)
    city = models.CharField(max_length=15,null=False)
    state = models.CharField(max_length=15,null=False)
    country = models.CharField(max_length=15,null=False)
    zipcode = models.CharField(max_length=10,null=False)
    
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pg_name
    
    @property
    def ownerEmail(self):
        return self.owner.email
    
    class Meta:
        db_table = 'pg_post_ads'


# ----------------------------------------------------------------

class PG_Amenities(models.Model):
       
    pg = models.ForeignKey(PG_PostAds,on_delete=models.CASCADE)
    
    ac = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    attached_washroom = models.BooleanField(default=False)
    room_cleaning = models.BooleanField(default=False)
    washing_machine = models.BooleanField(default=False)
    full_water_supply = models.BooleanField(default= False)
    food = models.BooleanField(default=False)
    kitchen_appliances = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    wardrobe = models.BooleanField(default=False)
    furnished_room = models.BooleanField(default=False)
    cctv_security = models.BooleanField(default=False) # cctv or security
    other = models.CharField(max_length=20,null=True,default="Other")

    # def __str__(self):
    #     return self.pg

    class Meta:
        db_table = 'pg_amenities'

# ----------------------------------------------------------------

class PG_Facility(models.Model):
    pg = models.ForeignKey(PG_PostAds,on_delete=models.CASCADE)
    facility_master = models.ForeignKey(PG_Facility_Master,on_delete=models.CASCADE)

    def __str__(self):
        return self.facility_master.facility_name
    
    class Meta:
        db_table = 'pg_facility'

    
# ----------------------------------------------------------------

class PG_Images(models.Model):
    pg = models.ForeignKey(PG_PostAds,on_delete=models.CASCADE)
    pg_images = models.ImageField(upload_to='pg_images_dir/',null=True,blank=True)
    
    # def __str__(self):
    #     return self.pg_images
    
    class Meta:
        db_table = 'pg_images'

# # ----------------------------------------------------------------
# # on hold
# class PG_Address_LatLong(models.Model):
#     pg = models.ForeignKey(PG_PostAds,on_delete=models.CASCADE)
#     geo_position = GeopositionField()
    
#     def __str__(self):
#         return self.geo_position
    
#     class Meta:
#         db_table = 'pg_address_latlong'


# ----------------------------------------------------------------
class PG_Comments(models.Model):
    pg = models.ForeignKey(PG_PostAds,on_delete=models.CASCADE)
    guest = models.ForeignKey(User,on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(null=True)
    comment = models.TextField(null=False)
    
    def _str_(self):
        return self.comment
    
    class Meta:
        db_table = 'pg_comments'