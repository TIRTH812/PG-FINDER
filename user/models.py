# import django
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# --------------------------------------------------------------------
# user app
class User(AbstractUser):
    # role_id = models.ForeignKey(Role,on_delete=models.CASCADE) # doubt 
    # null = false ???? doubt
    mobile_no = models.CharField(max_length=10) 
    aadhar_no = models.CharField(max_length=12)
    birthdate = models.DateField() 
    profile_image = models.ImageField(upload_to='user_profile_img_dir/',null=True,blank=True) #blank=False # media setup needed

    is_admin = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)

    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'

