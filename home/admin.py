from django.contrib import admin
from .models import *


class AdminUser(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'admin_id', 'status', 'created_on']
    search_fields = ('user',)

class AllUser(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_admin', 'is_merchant', 'is_reseller','is_reseller_merchant', 'is_customer','created_date']
    search_fields = ('name',)

class MerchantU(admin.ModelAdmin):
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'resellers', 'admin'),
        }),
        ('Merchant Information', {
            'fields': ('merchant_id', 'name', 'email', 'mobile', 'status'),
        }),
        ('Company Information', {
            'fields': ('company_name', 'address', 'city', 'pincode', 'state', 'country'),
        }),
        ('Pricing Information', {
            'fields': ('bike_price', 'auto_price', 'car_price', 'pickup_price', 'ev_price', 'truck_price'),
        }),
        ('Additional Information', {
            'fields': ('custom_hours', 'description', 'profile_img'),
        }),
        ('User Type', {
            'fields': ('is_merchant', 'is_reseller', 'is_customer' ),
        }),
        ('Vehicle Available', {
            'fields': ('is_bike', 'is_car', 'is_auto', 'is_pickup', 'is_ev', 'is_truck',),
        }),
        ('Permission Field', {
            'fields': ('name_visibility', 'name_mandatory', 'mobile_visibility', 'mobile_mandatory', 'captcha_visibility', 'captcha_mandatory',),
        }),
    )
    list_display = ['name', 'user','admin','resellers','custom_id','bike_price','auto_price','car_price','email', 'merchant_id', 'status', 'is_merchant','is_reseller', 'is_customer', 'created_on']
    search_fields = ('name',)
    
    # def save_model(self, obj):
    #     obj.save()
    #     if obj.user:
    #         obj.user.save()
    
class ResellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'admin', 'email', 'reseller_id','created_on']

class Parking(admin.ModelAdmin):
    list_display = ['vehicle_number','name', 'mobile', 'captcha', 'parking_id', 'time_status', 'merchant_id', 'created_on']
    search_fields = ('name','vehicle_number',)

class EnqieryUser(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile_number', 'address', 'created_on']

class AllLabel(admin.ModelAdmin):
    list_display = ['merchant_id','header_name', 'footer_home', 'footer_enter_user', 'footer_profile', 'home_colection_price']


# Register your models here.
admin.site.register(User, AllUser)
admin.site.register(UserEnquiry, EnqieryUser)
admin.site.register(Admin, AdminUser)
admin.site.register(MerchantUser, MerchantU)
admin.site.register(Resellers,ResellerAdmin)
admin.site.register(Label,AllLabel)
admin.site.register(ParkingUser, Parking)