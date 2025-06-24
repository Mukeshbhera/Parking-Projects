from django.db import models
from home.models import *
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from django.conf import settings
import random


class User(AbstractUser):
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, unique=True)
    is_admin = models.BooleanField(default=False)
    is_merchant = models.BooleanField(default=False)
    is_reseller = models.BooleanField(default=False)
    is_reseller_merchant = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    created_date = models.DateField(auto_now=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    token = models.CharField(max_length=500, null=True, default="")
    otp = models.CharField(max_length=5, null=True, blank=True)
    
    is_login = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    # def __str__(self):
        # return "{} -{}".format(self.username, self.email)
    

class Admin(models.Model):
    ADMIN_STATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Cancel', 'Cancel')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    admin_id = models.CharField(max_length=200,unique=True, default=uuid4)
    email = models.CharField(max_length=200, unique=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, default='Approved', choices=ADMIN_STATUS)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    pincode =models.CharField(max_length=6, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.email
    

class Resellers(models.Model):
    RESELLER_STATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Cancel', 'Cancel')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    reseller_id = models.CharField(max_length=200, unique=True, default=uuid4)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, unique=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, default='Pending', choices=RESELLER_STATUS)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    pincode =models.CharField(max_length=6, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.email

class MerchantUser(models.Model):
    MERCHANT_STATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Cancel', 'Cancel') 
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    resellers = models.ForeignKey(Resellers, on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True, blank=True)
    merchant_id = models.CharField(max_length=200, unique=True, default=uuid4)
    custom_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, unique=True, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, default='Pending', choices=MERCHANT_STATUS)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=25, null=True, blank=True)
    pincode =models.CharField(max_length=6, null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    bike_price = models.CharField(max_length=200, null=True, blank=True, default="0")
    auto_price = models.CharField(max_length=200, null=True, blank=True, default="0")
    car_price = models.CharField(max_length=200, null=True, blank=True, default="0")
    pickup_price = models.CharField(max_length=200, null=True, blank=True, default="0")
    ev_price = models.CharField(max_length=200, null=True, blank=True, default="0")
    truck_price = models.CharField(max_length=200, null=True, blank=True, default="0")
    custom_hours = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    profile_img = models.ImageField(upload_to='merchant-profile-images/', null=True, blank=True)
    is_merchant = models.BooleanField(default=False)
    is_reseller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    

    is_bike = models.BooleanField(default=True)
    is_car = models.BooleanField(default=True)
    is_auto = models.BooleanField(default=False)
    is_pickup = models.BooleanField(default=False)
    is_ev = models.BooleanField(default=False)
    is_truck = models.BooleanField(default=False)

    name_visibility = models.BooleanField(default=False)
    name_mandatory = models.BooleanField(default=False)
    mobile_visibility = models.BooleanField(default=False)
    mobile_mandatory = models.BooleanField(default=False)
    captcha_visibility = models.BooleanField(default=False)
    captcha_mandatory = models.BooleanField(default=False)

    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return self.email
    @staticmethod
    def generate_custom_id():
        while True:
            custom_id = str(random.randint(100000, 999999))
            if not MerchantUser.objects.filter(custom_id=custom_id).exists():
                return custom_id

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.custom_id = self.generate_custom_id()
        super(MerchantUser, self).save(*args, **kwargs)

class ParkingUser(models.Model):
    VEHICALE_TYPE = (
        ('Bike', 'Bike'),
        ('Auto', 'Auto'),
        ('Car', 'Car'),
        ('Pickup', 'Pickup'),
        ('Ev', 'Ev'),
        ('Truck', 'Truck')
    )
    TIME_TYPE=(
        ("In", "In"),
        ("Out", "Out"),
    )

    merchant_id = models.ForeignKey(MerchantUser, on_delete=models.CASCADE, null=True, blank=True)
    parking_id = models.CharField(max_length=25, unique=True, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    captcha = models.FileField(upload_to='vehicle_Image/', null=True, blank=True)
    vehicle_number = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, default='Car', choices=VEHICALE_TYPE)
    time_status = models.CharField(max_length=10, default='In', choices=TIME_TYPE)
    price = models.CharField(max_length=200, null=True, blank=True)
    vehicle_hour = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    vehicle_out_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehicle_number
    
    def save(self, *args, **kwargs):
        if not self.parking_id:
            self.parking_id = self.generat_parking_id()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generat_parking_id():
        while True:
            parking_id = str(random.randint(1000000000, 9999999999))
            if not ParkingUser.objects.filter(parking_id=parking_id).exists():
                return parking_id
            

class Label(models.Model):
    merchant_id = models.ForeignKey(MerchantUser, on_delete=models.CASCADE, null=True, blank=True)
    label_id = models.CharField(max_length=200, unique=True, default=uuid4)
    header_name = models.CharField(max_length=100, null=True, blank=True, default='Welcome Parking',)
    footer_home = models.CharField(max_length=30, null=True, blank=True, default="Home")
    footer_enter_user = models.CharField(max_length=30, null=True, blank=True, default="Enter User")
    footer_profile = models.CharField(max_length=30, null=True, blank=True, default="Profile")
    home_colection_price = models.CharField(max_length=30, null=True, blank=True, default="Collection Price")
    home_settled = models.CharField(max_length=30, null=True, blank=True, default="Settled")
    home_unsettled = models.CharField(max_length=30, null=True, blank=True, default="Unsettled")
    home_button_in = models.CharField(max_length=30, null=True, blank=True, default="In")
    home_button_out = models.CharField(max_length=30, null=True, blank=True, default="Out")
    all_enter_user = models.CharField(max_length=30, null=True, blank=True, default="All Entered Users")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



        
class UserEnquiry(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    mobile_number = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email