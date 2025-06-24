from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
import random
import string
import pyotp
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import date, datetime, timezone
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import *
from django.utils import timezone
import xlwt
from django.core.paginator import Paginator
import pandas as pd
from datetime import datetime, timedelta
import itertools
import requests
from django.db import transaction
import logging
from django.contrib.sessions.models import Session
from django.core.management.base import BaseCommand
from django.http import JsonResponse
####################  Admin  ########################

def front_layout(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['mobile_number']
        address = request.POST['address']
        message = request.POST['message']
        email_sent = "manish@gmail.com"
        portalname = "Parkgo"

        data = {
            "name" : name,
            "email" : email,
            "email_sent" : email_sent,
            "mobile" : mobile_number,
            "address" : address,
            "portalname" : portalname,
            "message" : message
        }

        url = "https://singhtek.com/php_api/contact_form.php"
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTcyNzU0MjN9.vH/8f1JfAQQhq81xx9i6f0SlA7P5Da1krV4G6RINXU0="

        # Append the token as a query parameter
        url_with_token = f"{url}?token={token}"

        response = requests.post(url_with_token, json=data)
        print(response.content, 'AAAAAAAAAAAAAAAaa')

        if response.status_code == 200:
            api_response = response.json()

            admin = UserEnquiry.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                address=address,
                message=message,
            )

            if admin:
                email_message = f"Name: {name}\nEmail: {email}\nAddress: {address}\nMobile_Number: {mobile_number}\nMessage: {message}"
                send_mail(
                    'Parking Enquiry',
                    email_message,
                    'noreply@parking.justapay.in',
                    ['noreply@parking.justapay.in'],
                    fail_silently=False,
                )

            messages.success(request, "Message Sent Successfully")
        else:
            # Handle the API error, if needed
            messages.error(request, "Failed to send data to the API")
    return render(request, 'front-layout/index.html')



@login_required(login_url='login')
def addsuperadmin(request):

    if request.method == 'GET':
        adminuser = Admin.objects.all()
        return render(request, 'parking_dashboard/index.html', {'admin': adminuser})

    if request.method == 'POST':
        print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")

        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        company_name = request.POST['company_name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        
        print(name, mobile, 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')

        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('addsuperadmin')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('addsuperadmin')

        user = User.objects.create(username=username, password=password, email=username, name=name, mobile=mobile, is_admin=True)
        user.set_password(password)
        user.save()
        
        admin = Admin.objects.create(
            user=request.user, 
            email=username,
            name=name,
            company_name=company_name,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
        )

        messages.success(request, "Admin Created Successfully.")
        return redirect('addsuperadmin')
    
    context = {
        'messages': messages.get_messages(request),
    }     

    return render(request, 'parking_dashboard/index.html', context)



@login_required(login_url='login')
def admin_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = Admin.objects.get(email=request.user.username)
            return render(request, 'parking_dashboard/admin_dashboard/merchant-user-profile.html', {'admin': admin})

    if request.method == 'POST':
        admin = Admin.objects.get(email=request.user.username)
        new_email = request.POST['email']

        username = request.user.username
        user = User.objects.get(username=username)

        if new_email != admin.email and Admin.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('adminuserprofile')
        
        user.name = request.POST['name']
        user.mobile =request.POST['mobile']
        user.email = request.POST['email']
        user.username = request.POST['email']
        
        admin.name = request.POST['name']
        admin.email = new_email
        admin.mobile = request.POST['mobile']
        admin.company_name = request.POST['company_name']
        admin.address = request.POST['address']
        admin.country = request.POST['country']
        admin.city = request.POST['city']
        admin.state = request.POST['state']
        admin.pincode = request.POST['pincode']
        admin.save()
        user.save()
        
        messages.success(request, 'Your profile has been successfully updated.')
        return redirect('adminuserprofile')   
    return render(request, 'parking_dashboard/admin_dashboard/merchant-user-profile.html')

@login_required(login_url='login')
def adminedit(request, id):
    try:
        instance = Admin.objects.get(id=id)
    except Admin.DoesNotExist:
        messages.error(request, 'Admin not found')
        return redirect('addsuperadmin')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']
        country = request.POST['country']
    
        instance.name = name
        instance.email = email
        instance.mobile = mobile
        instance.company_name = company_name
        instance.address = address
        instance.city = city
        instance.pincode = pincode
        instance.state = state
        instance.country = country
        instance.save()
        # user.save()
        messages.success(request, 'Your Admin Edit successfully updated.') 
        return redirect('addsuperadmin')    
    return render(request, 'parking_dashboard/index.html', {'instance': instance})


########################## Merchant Login #####################

def add_merchant(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        bike_price = request.POST.get('bike_price')
        auto_price = request.POST.get('auto_price')
        car_price = request.POST.get('car_price')
        pickup_price = request.POST.get('pickup_price')
        ev_price = request.POST.get('ev_price')
        truck_price = request.POST.get('truck_price')
        custom_hours = request.POST.get('custom_hours')
        # profile_img = request.POST['profile_img']
        profile_img = request.FILES.get('profile_img')
        description = request.POST['description']


        if bike_price is None:
            messages.error(request, "Bike Price Required")
            return redirect('merchantapproved')
        
        if auto_price is None:
            messages.error(request, "Auto Price Required")
            return redirect('merchantapproved')
        
        if car_price is None:
            messages.error(request, "Car Price Required")
            return redirect('merchantapproved')
        
        if pickup_price is None:
            messages.error(request, "Pickup Price Required")
            return redirect('merchantapproved')
        
        if ev_price is None:
            messages.error(request, "Ev Price Required")
            return redirect('merchantapproved')
        
        if truck_price is None:
            messages.error(request, "Truck Price Required")
            return redirect('merchantapproved')
        
        if custom_hours is None:
            messages.error(request, "Custom Hours Required")
            return redirect('merchantapproved')
        
        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('merchantapproved')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('merchantapproved')

        user = User.objects.create(username=username, password=password, email=username, name=name, mobile=mobile, is_merchant=True)
        user.set_password(password)
        user.save()
        
        admin = request.user.id
        admin = request.user.username
        admin1 = Admin.objects.get(email=admin)
        merchant = MerchantUser.objects.create(
            admin=admin1,
            user=user, 
            email=username,
            name=name,
            mobile=mobile,
            company_name=company_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
            bike_price=bike_price,
            auto_price=auto_price,
            car_price=car_price,
            pickup_price=pickup_price,
            ev_price=ev_price,
            truck_price=truck_price,
            custom_hours=custom_hours,
            profile_img=profile_img,
            description=description,   
            is_merchant=True
        )
        ab = Label.objects.create(merchant_id=merchant)

        messages.success(request, "Merchant Created Successfully.")
        return redirect('merchantpending')
    
    context = {
        'messages': messages.get_messages(request),
    }  
    
    return render(request, 'parking_dashboard/admin_dashboard/index.html', context)

# ###############################multi merchant ###################################################


def multi_merchant(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        bike_price = request.POST.get('bike_price')
        auto_price = request.POST.get('auto_price')
        car_price = request.POST.get('car_price')
        pickup_price = request.POST.get('pickup_price')
        ev_price = request.POST.get('ev_price')
        truck_price = request.POST.get('truck_price')
        custom_hours = request.POST.get('custom_hours')
        profile_img = request.FILES.get('profile_img')
        description = request.POST['description']
        
        if bike_price is None:
            messages.error(request, "Bike Price Required")
            return redirect('merchantapproved')
        
        if auto_price is None:
            messages.error(request, "Auto Price Required")
            return redirect('merchantapproved')
        
        if car_price is None:
            messages.error(request, "Car Price Required")
            return redirect('merchantapproved')
        
        if pickup_price is None:
            messages.error(request, "Pickup Price Required")
            return redirect('merchantapproved')
        
        if ev_price is None:
            messages.error(request, "Ev Price Required")
            return redirect('merchantapproved')
        
        if truck_price is None:
            messages.error(request, "Truck Price Required")
            return redirect('merchantapproved')
        
        if custom_hours is None:
            messages.error(request, "Custom Hours Required")
            return redirect('merchantapproved')
        
        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('merchantapproved')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('merchantapproved')
        
        
        user = User.objects.create(username=username,password=password, email=username, name=name, mobile=mobile, is_customer=True)
        user.name = name
        user.mobile = mobile
        user.save()
        admin = request.user.id
        admin = request.user.username
        admin1 = Admin.objects.get(email=admin)
        
        selected_merchants = request.POST['selected_merchants']
        select = get_object_or_404(User, email=selected_merchants)
        merchant = MerchantUser.objects.create(
            admin=admin1,
            user=select,
            email=username,
            name=name,
            mobile=mobile,
            company_name=company_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
            bike_price=bike_price,
            auto_price=auto_price,
            car_price=car_price,
            pickup_price=pickup_price,
            ev_price=ev_price,
            truck_price=truck_price,
            custom_hours=custom_hours,
            profile_img=profile_img,
            description=description,
            is_merchant=True,
            is_customer=True
        )
    
        ab = Label.objects.create(merchant_id=merchant)
        messages.success(request, "Multi Merchant Created Successfully.")
        return redirect('merchantpending')

    context = {
        'messages': messages.get_messages(request),
    }

    return render(request, 'parking_dashboard/admin_dashboard/index.html', context)


###################Merchant Status################################


@login_required(login_url='login')
def admin_merchant_appro(request):
    if request.method == 'GET':
        user = request.user
        user = user.username
        admin = Admin.objects.filter(email=user)
        merchant_approvds = MerchantUser.objects.filter(status='Approved',admin=admin.first())
        user1 = request.user
        users = User.objects.get(email=user1)
        merchants = MerchantUser.objects.filter(status='Approved', admin=admin.first())
        return render(request, 'parking_dashboard/admin_dashboard/index.html', {'merchant_approvds': merchant_approvds,'admin':admin})

def admin_merchant_pen(request):
    if request.method == 'GET':
        user = request.user
        user = user.username
        admin = Admin.objects.filter(email=user)
        merchant_penddings = MerchantUser.objects.filter(status='Pending',admin=admin.first())
        user1 = request.user
        users = User.objects.get(email=user1)
        merchants = MerchantUser.objects.filter(status='Pending', admin=admin.first())
        return render(request, 'parking_dashboard/admin_dashboard/merchant_pending.html', {'merchant_penddings': merchant_penddings,'admin':admin})

def admin_merchant_can(request):
    if request.method == 'GET':
        user = request.user
        user = user.username
        admin = Admin.objects.filter(email=user)
        merchant_cancels = MerchantUser.objects.filter(status='Cancel',admin=admin.first())
        user1 = request.user
        users = User.objects.get(email=user1)
        merchants = MerchantUser.objects.filter(status='Cancel', admin=admin.first())
        return render(request, 'parking_dashboard/admin_dashboard/merchant_cancel.html', {'merchant_cancels': merchant_cancels,'admin':admin})

def dashboard_merchant_update_status(request):
    if request.method == 'POST':
        merchant_id = request.POST.get('merchant_id')
        
        if merchant_id:
            new_status = request.POST.get('new_status')

            merchant_user = MerchantUser.objects.get(id=merchant_id)
            merchant_user.status = new_status
            merchant_user.save()

            return redirect('merchantapproved')
        
        merchant_users = MerchantUser.objects.filter(user=request.user, created_on__lte=timezone.now()).order_by('-created_on')
        context = {'merchant_user': merchant_users}
        return render(request, 'parking_dashboard/admin_dashboard/merchant_approve.html', context)
    

###################### edit ############################################################################
@login_required(login_url='login')
def indexedit(request, id):
    try:
        instance = MerchantUser.objects.get(id=id)
    except MerchantUser.DoesNotExist:
        messages.error(request, 'Merchant not found')
        return redirect('merchantapproved')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']
        country = request.POST['country']
        bike_price = request.POST['bike_price']
        auto_price = request.POST['auto_price']
        car_price = request.POST['car_price']
        pickup_price = request.POST['pickup_price']
        ev_price = request.POST['ev_price']
        truck_price = request.POST['truck_price']
        custom_hours = request.POST['custom_hours']
        # profile_img = request.POST['profile_img']
        profile_img = request.FILES.get('profile_img')
        description = request.POST['description']

        instance.name = name
        instance.email = email
        instance.mobile = mobile
        instance.company_name = company_name
        instance.address = address
        instance.city = city
        instance.pincode = pincode
        instance.state = state
        instance.country = country
        instance.bike_price = bike_price
        instance.auto_price = auto_price
        instance.car_price = car_price
        instance.pickup_price = pickup_price
        instance.ev_price = ev_price
        instance.truck_price = truck_price
        instance.custom_hours = custom_hours
        instance.profile_img = profile_img
        instance.description = description
        
        instance.save()
        # user.save()
        messages.success(request, 'Your Merchant Edit successfully updated.') 
        return redirect('merchantapproved')    
    return render(request, 'parking_dashboard/admin_dashboard/index.html', {'instance': instance})




def all_user_profile(request):
    if request.user.is_authenticated:
        try:
            merchant = MerchantUser.objects.get(email=request.user.username)
        except MerchantUser.DoesNotExist:
            merchant = None
    else:
        merchant = None

    return {'merchant': merchant}


@login_required(login_url='login')
def merchant_user_profile(request):
    if request.method == 'GET':
        if request.user:
            merchant = MerchantUser.objects.get(email=request.user.username)
            return render(request, 'parking_dashboard/admin_dashboard/parkinguser/reseller-merchant-user-profile.html', {'merchant': merchant})

    if request.method == 'POST':
        merchant = MerchantUser.objects.get(email=request.user.username)
        new_email = request.POST.get('email')

        user = request.user
        username = user.username
        user = User.objects.get(username=username)

        if new_email != merchant.email and MerchantUser.objects.filter(email=new_email).exclude(id=merchant.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('parkinguserprofile')
        
        user.email = request.POST['email']
        user.name = request.POST['name']
        user.mobile =  request.POST['mobile']
        user.username = request.POST['email']


        merchant.name = request.POST['name']
        merchant.email = new_email
        merchant.mobile = request.POST['mobile']
        merchant.company_name = request.POST['company_name']
        merchant.address = request.POST['address']
        merchant.country = request.POST['country']
        merchant.city = request.POST['city']
        merchant.state = request.POST['state']
        merchant.pincode = request.POST['pincode']
        merchant.bike_price = request.POST['bike_price']
        merchant.auto_price = request.POST['auto_price']
        merchant.car_price = request.POST['car_price']
        merchant.pickup_price = request.POST['pickup_price']
        merchant.ev_price = request.POST['ev_price']
        merchant.truck_price = request.POST['truck_price']
        merchant.custom_hours = request.POST['custom_hours']
        profile_img = request.FILES.get('profile_img')
        merchant.description = request.POST['description']

        if profile_img:
            merchant.profile_img = profile_img
            merchant.save()
            user.save()
            messages.success(request, 'Your profile has been successfully updated.')
            return redirect('parkinguserprofile')
        
        merchant.save()
        user.save()
        messages.error(request, 'Your profile has been successfully updated.')
        return redirect('parkinguserprofile')
    
    return render(request, 'parking_dashboard/admin_dashboard/parkinguser/reseller-merchant-user-profile.html')

    
################# reseller URL ####################    

def add_reseller(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']  
    
        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('resellerapproved')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('resellerapproved')

        user = User.objects.create(username=username, password=password, email=username, name=name, mobile=mobile, is_reseller=True)
        user.set_password(password)
        user.save()
        
        admin = request.user.id
        admin3 = request.user.username
        admin1 = Admin.objects.get(email=admin3)

        reseller = Resellers.objects.create(
            admin=admin1,
            user=user, 
            email=username,
            name=name,
            mobile=mobile,
            company_name=company_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
        )
        messages.success(request, "Reseller Created Successfully.")
        return redirect('resellerpending')
    context = {
        'messages': messages.get_messages(request),
    }  
    return render(request, 'parking_dashboard/admin_dashboard/reseller_approve.html', context)

@login_required(login_url='login')
def reseller_profile(request):
    if request.method == 'GET':
        user = request.user
        user_id = user.id
        if request.user.is_reseller:
            user = request.user
            username = user.username
            merchant = Resellers.objects.get(email=username)
            return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller-user-profile.html', {'reseller': merchant})
        else:
            messages.error(request, "You Cant access")
            return redirect("reselleruserprofile")
    
    if request.method == 'POST':
        user = request.user
        user_id = user.id
        username = user.username
        user = Resellers.objects.get(email=username)
        user1 = User.objects.get(username=username)
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        pincode= request.POST['pincode']
        state = request.POST['state']
        country = request.POST['country']

        user1.name=name
        user1.email=email
        user1.mobile=mobile

        user.name=name
        user.email=email
        user.mobile=mobile
        user.company_name=company_name
        user.address=address
        user.city=city
        user.pincode=pincode
        user.state=state
        user.country=country
        user.save()
        user1.save()
        user1.username=email
        user1.save()

        messages.success(request, 'Your profile has been successfully updated.')
        return redirect('reselleruserprofile')
    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller-user-profile.html')



@login_required(login_url='login')
def admin_reseller_appro(request):
    if request.method == 'GET':
        user = request.user
        user = user.username
        admin = Admin.objects.filter(email=user)
        reseller_approvds = Resellers.objects.filter(status='Approved',admin=admin.first())
        return render(request, 'parking_dashboard/admin_dashboard/reseller_approve.html', {'reseller_approvds': reseller_approvds,'admin':admin})

@login_required(login_url='login')
def admin_reseller_pen(request):
    if request.method == 'GET':
        user = request.user
        user = user.username
        admin = Admin.objects.filter(email=user)
        reseller_penddings = Resellers.objects.filter(status='Pending',admin=admin.first())
        return render(request, 'parking_dashboard/admin_dashboard/reseller_pending.html', {'reseller_penddings': reseller_penddings,'admin':admin})

@login_required(login_url='login')
def admin_reseller_can(request):
    if request.method == 'GET':
        user = request.user
        user = user.username
        admin = Admin.objects.filter(email=user)
        reseller_cancels = Resellers.objects.filter(status='Cancel',admin=admin.first())
        return render(request, 'parking_dashboard/admin_dashboard/reseller_cancel.html', {'reseller_cancels': reseller_cancels,'admin':admin})

@login_required(login_url='login')
def dashboard_reseller_update_status(request):
    if request.method == 'POST':
        reseller_id = request.POST.get('reseller_id')
        if reseller_id:
            new_status = request.POST.get('new_status')
            reseller_user = Resellers.objects.get(id=reseller_id)
            reseller_user.status = new_status
            reseller_user.save()
            return redirect('resellerapproved')
        reseller_users = Resellers.objects.filter(user=request.user, created_on__lte=timezone.now()).order_by('-created_on')
        context = {'reseller_user': reseller_users}
        return render(request, 'parking_dashboard/admin_dashboard/reseller_approve.html', context)


@login_required(login_url='login')
def reselleredit(request, id):
    try:
        instance = Resellers.objects.get(id=id)
    except Resellers.DoesNotExist:
        messages.error(request, 'Reseller not found')
        return redirect('resellerapproved')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']
        country = request.POST['country']

        instance.name = name
        instance.email = email
        instance.mobile = mobile
        instance.company_name = company_name
        instance.address = address
        instance.city = city
        instance.pincode = pincode
        instance.state = state
        instance.country = country
        instance.save()
        # user.save()
        messages.success(request, 'Your Reseller Edit successfully updated.') 
        return redirect('resellerapproved')    
    return render(request, 'parking_dashboard/admin_dashboard/reseller_approve.html', {'instance': instance})


################### Resller Merchant User ###########################

@login_required(login_url='login')
def add_reseller_merchant(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        bike_price = request.POST.get('bike_price')
        auto_price = request.POST.get('auto_price')
        car_price = request.POST.get('car_price')
        pickup_price = request.POST.get('pickup_price')
        ev_price = request.POST.get('ev_price')
        truck_price = request.POST.get('truck_price')
        custom_hours = request.POST.get('custom_hours')
        profile_img = request.FILES.get('profile_img')
        description = request.POST['description']
        # is_merchant = request.POST['is_merchant']
        # is_reseller = request.POST['is_reseller']
        
        if bike_price is None:
            messages.error(request, "Bike Price Required")
            return redirect('resellermerchantapprove')
        
        if auto_price is None:
            messages.error(request, "Auto Price Required")
            return redirect('resellermerchantapprove')
        
        if car_price is None:
            messages.error(request, "Car Price Required")
            return redirect('resellermerchantapprove')
        
        if pickup_price is None:
            messages.error(request, "Pickup Price Required")
            return redirect('resellermerchantapprove')
        
        if ev_price is None:
            messages.error(request, "Ev Price Required")
            return redirect('resellermerchantapprove')
        
        if truck_price is None:
            messages.error(request, "Truck Price Required")
            return redirect('resellermerchantapprove')
        
        if custom_hours is None:
            messages.error(request, "Custom Hours Required")
            return redirect('merchantapproved')
        
        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('resellermerchantapprove')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('resellermerchantapprove')

        user = User.objects.create(username=username, password=password, email=username, name=name, mobile=mobile, is_reseller_merchant=True)
        user.set_password(password)
        user.save()
        
        admin3 = request.user.username
        admin1 = Resellers.objects.get(email=admin3)
        reseller = MerchantUser.objects.create(
            resellers=admin1,
            user=user, 
            email=username,
            name=name,
            mobile=mobile,
            company_name=company_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
            bike_price=bike_price,
            auto_price=auto_price,
            car_price=car_price,
            pickup_price=pickup_price,
            ev_price=ev_price,
            truck_price=truck_price,
            custom_hours=custom_hours,
            profile_img=profile_img,
            description=description,
            is_reseller=True
            # is_merchant=is_merchant,
            # is_reseller=is_reseller,
        )
        ab = Label.objects.create(merchant_id=reseller)
        messages.success(request, "Reseller Merchant Created Successfully.")
        return redirect('resellermerchantpending')
    context = {
        'messages': messages.get_messages(request),
    }  
    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_approve.html', context)


def addmultiresellermerchant(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        bike_price = request.POST.get('bike_price')
        auto_price = request.POST.get('auto_price')
        car_price = request.POST.get('car_price')
        pickup_price = request.POST.get('pickup_price')
        ev_price = request.POST.get('ev_price')
        truck_price = request.POST.get('truck_price')
        custom_hours = request.POST.get('custom_hours')
        profile_img = request.FILES.get('profile_img')
        description = request.POST['description']
        
        if bike_price is None:
            messages.error(request, "Bike Price Required")
            return redirect('merchantapproved')
        
        if auto_price is None:
            messages.error(request, "Auto Price Required")
            return redirect('merchantapproved')
        
        if car_price is None:
            messages.error(request, "Car Price Required")
            return redirect('merchantapproved')
        
        if pickup_price is None:
            messages.error(request, "Pickup Price Required")
            return redirect('merchantapproved')
        
        if ev_price is None:
            messages.error(request, "Ev Price Required")
            return redirect('merchantapproved')
        
        if truck_price is None:
            messages.error(request, "Truck Price Required")
            return redirect('merchantapproved')
        
        if custom_hours is None:
            messages.error(request, "Custom Hours Required")
            return redirect('merchantapproved')
        
        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('merchantapproved')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('merchantapproved')
        
        
        user = User.objects.create(username=username,password=password, email=username, name=name, mobile=mobile, is_customer=True)
        user.name = name
        user.mobile = mobile
        user.save()
        admin = request.user.id
        admin = request.user.username
        admin1 = Resellers.objects.get(email=admin)
        
        selected_merchants = request.POST['selected_merchants']
        select = get_object_or_404(User, email=selected_merchants)
        reseller = MerchantUser.objects.create(
            resellers=admin1,
            user=select,
            email=username,
            name=name,
            mobile=mobile,
            company_name=company_name,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
            bike_price=bike_price,
            auto_price=auto_price,
            car_price=car_price,
            pickup_price=pickup_price,
            ev_price=ev_price,
            truck_price=truck_price,
            custom_hours=custom_hours,
            profile_img=profile_img,
            description=description,
            is_reseller=True,
            is_customer=True
        )
    
        ab = Label.objects.create(merchant_id=reseller)
        messages.success(request, " Multi Reseller Merchant Created Successfully.")
        return redirect('resellermerchantpending')
    context = {
        'messages': messages.get_messages(request),
    }

    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_approve.html', context)


@login_required(login_url='login')
def resller_merchant_approve(request):
    if request.method == 'GET':
        user = request.user.username
        re = Resellers.objects.get(email=user)
        reseller_merchant_approved = MerchantUser.objects.filter(resellers=re, status='Approved')
    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_approve.html', {'reseller_merchant_approved': reseller_merchant_approved}) 

@login_required(login_url='login')
def resller_merchant_pending(request):
    if request.method == 'GET':
        user = request.user.username
        re = Resellers.objects.get(email=user)
        reseller_merchant_pen = MerchantUser.objects.filter(resellers=re, status='Pending')
    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_pending.html',{'reseller_merchant_pen': reseller_merchant_pen}) 

@login_required(login_url='login')
def resller_merchant_cancel(request):
    if request.method == 'GET':
        user = request.user.username
        re = Resellers.objects.get(email=user)
        reseller_merchant_cancel = MerchantUser.objects.filter(resellers=re, status='Cancel')
    
    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_cancel.html', {'reseller_merchant_cancel': reseller_merchant_cancel}) 

@login_required(login_url='login')
def reseller_merchant_status(request):
    if request.method == 'POST':
        reseller_merchant = request.POST.get('reseller_merchant')
        if reseller_merchant:
            new_status = request.POST.get('new_status')
            reseller_user = MerchantUser.objects.get(id=reseller_merchant)
            reseller_user.status = new_status
            reseller_user.save()
            return redirect('resellermerchantapprove')
        reseller_users = MerchantUser.objects.filter(user=request.user, created_on__lte=timezone.now()).order_by('-created_on')
        context = {'reseller_user': reseller_users}
        return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_approve.html', context)



@login_required(login_url='login')
def resellermeredit(request, id):
    try:
        instance = MerchantUser.objects.get(id=id)
    except MerchantUser.DoesNotExist:
        messages.error(request, 'Reseller Merchant not found')
        return redirect('resellermerchantapprove')
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']
        country = request.POST['country']
        bike_price = request.POST['bike_price']
        auto_price = request.POST['auto_price']
        car_price = request.POST['car_price']
        pickup_price = request.POST['pickup_price']
        ev_price = request.POST['ev_price']
        truck_price = request.POST['truck_price']
        custom_hours = request.POST['custom_hours']
        # profile_img = request.POST['profile_img']
        profile_img = request.FILES.get('profile_img')
        description = request.POST['description']

        instance.name = name
        instance.email = email
        instance.mobile = mobile
        instance.company_name = company_name
        instance.address = address
        instance.city = city
        instance.pincode = pincode
        instance.state = state
        instance.country = country
        instance.bike_price = bike_price
        instance.auto_price = auto_price
        instance.car_price = car_price
        instance.pickup_price = pickup_price
        instance.ev_price = ev_price
        instance.truck_price = truck_price
        instance.custom_hours = custom_hours
        instance.profile_img = profile_img
        instance.description = description
        
        instance.save()
        # user.save()
        messages.success(request, 'Your Reseller Merchant Edit successfully updated.') 
        return redirect('resellermerchantapprove')    
    return render(request, 'parking_dashboard/admin_dashboard/reseller_merchant/reseller_approve.html', {'instance': instance})

################ Parking User  ####################

@login_required(login_url='login')
def parking(request):
    if request.method == 'GET':
        user = request.user        
        username = user.username
        ad = MerchantUser.objects.get(email=username)
        parking = ParkingUser.objects.filter(merchant_id=ad)
        items_per_page = 10
        parking = parking.order_by('created_on')
        paginator = Paginator(parking, items_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        today = date.today()
        out_data = ParkingUser.objects.filter(Q(merchant_id=ad) & Q(vehicle_out_time__date=today)& Q (time_status='Out')).count()
        total_amount_all = ParkingUser.objects.filter(Q(merchant_id=ad) & Q(vehicle_out_time__date=today), time_status='Out').aggregate(Sum('price'))['price__sum']
        in_data = ParkingUser.objects.filter(Q(merchant_id=ad) & Q (time_status='In')).count()
        existing_entries_in = ParkingUser.objects.filter(Q(merchant_id=ad), time_status='In')
        bike_status = 0
        auto_status = 0
        car_status = 0
        pickup_status = 0
        ev_status = 0
        truck_status = 0
        
        for entry in existing_entries_in:
            status = entry.status
            if status == 'Bike':
                bike_status += 1
            elif status == 'Auto':
                auto_status += 1
            elif status == 'Car':
                car_status += 1
            elif status == 'Pickup':
                pickup_status += 1
            elif status == 'Ev':
                ev_status += 1
            elif status == 'Truck':
                truck_status += 1
        total_amount_in = 0
        bike_status = 0
        auto_status = 0
        car_status = 0
        pickup_status = 0
        ev_status = 0
        truck_status = 0
        
        for existing_entry in existing_entries_in:
            vehicle_hour = float(ad.custom_hours)
            time_aware = existing_entry.created_on.replace(tzinfo=timezone.utc)
            difference = datetime.now(timezone.utc) - time_aware
            sec = difference.total_seconds()
            minutes = sec // 60
            hours = minutes // 60
            remaining_minutes = minutes % 60
            count_hour_one = 1
            total_hours = hours + count_hour_one
            if existing_entry.status == 'Bike':
                park2 = ad.bike_price 
                bike_status += 1
            elif existing_entry.status == 'Auto':
                park2 = ad.auto_price
                auto_status += 1
            elif existing_entry.status == 'Car':
                park2 = ad.car_price
                car_status += 1
            elif existing_entry.status == 'Pickup':
                park2 = ad.pickup_price
                pickup_status += 1
            elif existing_entry.status == 'Ev':
                park2 = ad.ev_price 
                ev_status += 1
            elif existing_entry.status == 'Truck':
                park2 = ad.truck_price  
                truck_status += 1
            else:
                park2 = 0.0

            if float(vehicle_hour) <= float(total_hours):
                calculate = str(float(park2) * total_hours)
                existing_entry.price = calculate
                existing_entry.vehicle_hour = total_hours
                existing_entry.save()
                total_amount_in += float(calculate) 
            else:
                existing_entry.vehicle_hour = vehicle_hour
                existing_entry.amount = park2
                existing_entry.save()
                total_amount_in += float(park2)
    return render(request, 'parking_dashboard/admin_dashboard/parkinguser/index.html', {'bike_status': bike_status, 'auto_status': auto_status, 'car_status': car_status, 'pickup_status':pickup_status, 'ev_status':ev_status,'truck_status':truck_status,'out_data': out_data, 'in_data':in_data,'total_amount_in': total_amount_in, 'total_amount_all': total_amount_all,'page': page})

def appcustomization(request):
    if request.method == 'GET':
        if request.user:
            user = request.user
            users = user.username
            merchant = MerchantUser.objects.get(email=users)
            ab = Label.objects.get(merchant_id=merchant)
            return render(request,'parking_dashboard/admin_dashboard/parkinguser/appcustomization.html', {'ab': ab})
    
    if request.method == 'POST':
        user = request.user
        users = user.username
        merchant = MerchantUser.objects.get(email=users)
        ab = Label.objects.get(merchant_id=merchant)
        new_email = request.POST.get('email')

        if new_email and new_email != users:
            if MerchantUser.objects.filter(email=new_email).exclude(id=merchant.id).exists():
                messages.error(request, "Email Already Exists")
                return redirect('appcustomization')

        ab.header_name = request.POST['header_name']
        ab.footer_home = request.POST['footer_home']
        ab.footer_enter_user = request.POST['footer_enter_user']
        ab.footer_profile = request.POST['footer_profile']
        ab.home_colection_price = request.POST['home_colection_price']
        ab.home_settled = request.POST['home_settled']
        ab.home_unsettled = request.POST['home_unsettled']
        ab.home_button_in = request.POST['home_button_in']
        ab.home_button_out = request.POST['home_button_out']
        ab.all_enter_user = request.POST['all_enter_user']

        if new_email:
            merchant.email = new_email
            merchant.save()

        ab.save()
        messages.success(request, 'Your App Customization has been successfully updated.')
        return redirect('appcustomization')

    return render(request, 'parking_dashboard/admin_dashboard/parkinguser/appcustomization.html')



def setting(request):
    if request.method == 'GET':
        user = request.user
        username = user.username
        setting = MerchantUser.objects.get(email=username)
        return render(request, 'parking_dashboard/admin_dashboard/parkinguser/setting.html', {'setting': setting})
    if request.method == 'POST':
        is_bike = request.POST.get('is_bike', False)
        is_car = request.POST.get('is_car', False)
        is_auto = request.POST.get('is_auto', False)
        is_pickup = request.POST.get('is_pickup', False)
        is_ev = request.POST.get('is_ev', 'False')
        is_truck = request.POST.get('is_truck', False) 
        name_visibility = request.POST.get('name_visibility', False) 
        name_mandatory = request.POST.get('name_mandatory', False) 
        mobile_visibility = request.POST.get('mobile_visibility', False) 
        mobile_mandatory = request.POST.get('mobile_mandatory', False) 
        captcha_visibility = request.POST.get('captcha_visibility', False) 
        captcha_mandatory = request.POST.get('captcha_mandatory', False) 
        setting = MerchantUser.objects.get(email=request.user.username)
        setting.is_bike = is_bike
        setting.is_car = is_car
        setting.is_auto = is_auto
        setting.is_pickup = is_pickup
        setting.is_ev = is_ev
        setting.is_truck = is_truck  
        setting.name_visibility = name_visibility        
        setting.name_mandatory = name_mandatory        
        setting.mobile_visibility = mobile_visibility        
        setting.mobile_mandatory = mobile_mandatory        
        setting.captcha_visibility = captcha_visibility        
        setting.captcha_mandatory = captcha_mandatory       
        setting.save()
        messages.success(request, 'Your setting has been successfully updated.')
        return redirect('setting')
    return render(request, 'parking_dashboard/admin_dashboard/parkinguser/setting.html')

@login_required(login_url='login')
def all_merchant_park(request):
    users = request.user.username
    admin_list = Admin.objects.get(email=users)
    resellers = Resellers.objects.filter(admin=admin_list, status='Approved')
    merchant_users = MerchantUser.objects.filter(admin=admin_list, status='Approved')
    combined_data = list(itertools.chain(merchant_users, resellers))
    return render(request, 'parking_dashboard/admin_dashboard/parking_users.html', {'merchant': combined_data})   


@login_required(login_url='login')
def merchant_parking_user_all(request, pk):
    parking_users = ParkingUser.objects.filter(merchant_id=pk)
    return render(request, 'parking_dashboard/admin_dashboard/merchant_parking_user.html', {'parking_users':parking_users})    

    


################ Login API  ####################

def login_in(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # recaptcha_field = ReCaptchaField(widget=ReCaptchaV2Checkbox())
        # try:
        #     is_recaptcha_valid = recaptcha_field.clean(recaptcha_response)
        # except ValidationError:
        #     messages.error(request, "reCAPTCHA is required.")
        #     return redirect('login')
        
        if user is None:
            messages.success(request, "Email/Custom or Password Incorrect")
            return redirect('login')
        
        if user is not None:
            login(request, user)
            request.session['is_logged_in'] = True
            # print(request.session['is_logged_in'], 'TTTTTTTTTTTTTTTTTTTTTTTTT')
            request.session['username'] = user.username
            # print(user.username, 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG')
            if user.is_superuser:
                username = user.username
                user = User.objects.get(username=username)
                messages.success(request, "Super User Login Successful")
                return redirect('addsuperadmin') 
            
            if user.is_admin:
                user1 = user.username
                merchant = Admin.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status=='Approved':
                    messages.success(request, "Admin Login successfully")
                    return redirect('merchantapproved')
                else:
                    messages.success(request, "Your Account Not Approved")
                    return redirect('login')
            
            if user.is_merchant:
                user1 = user.username
                merchant = MerchantUser.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status == 'Approved':
                    if user.is_login:
                        messages.error(request, "You are already logged in from another system.")
                        return redirect('login')

                    session_key = request.session.session_key
                    if not Session.objects.filter(session_key=session_key).exists():
                        user.is_login = False
                        user.save()

                    user.is_login = True
                    user.save()

                    messages.success(request, "Merchant Login successfully")
                    return redirect('parkinguser')
                else:
                    messages.success(request, "Your Account Not Approved")
                    return redirect('login')
                
            if user.is_reseller:
                user1 = user.username
                reseller = Resellers.objects.get(email=user1)
                reseller_status = reseller.status
                if reseller_status=='Approved':
                    messages.success(request, "Reseller Login successfully")
                    return redirect('resellermerchantapprove')
                else:
                    messages.success(request, "Your Account Not Approved")
                    return redirect('login')
                
            if user.is_reseller_merchant:
                user1 = user.username
                merchant = MerchantUser.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status=='Approved':
                    messages.success(request, "Reseller Merchant Login successfully")
                    return redirect('parkinguser')
                else:
                    messages.success(request, "Your Account Not Approved")
                    return redirect('login')
        
            if user.is_customer:
                user1 = user.username
                merchant = MerchantUser.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status=='Approved':
                    messages.success(request, "Multi Merchant Login successfully")
                    return redirect('parkinguser')
                else:
                    messages.success(request, "Your Account Not Approved")
                    return redirect('login')
    return render(request, 'parking_dashboard/login.html')



@login_required
def update_logout_status(request):
    if request.session.get('is_logged_in', False):
        request.session['is_logged_in'] = False
        request.user.is_login = False
        request.user.save()
        print(f"User '{request.user.username}' logged out.")

    return JsonResponse({'message': 'Logout status updated'})

# #####################register_merchant##########################

def register_merchant(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        name = request.POST['name']
        mobile = request.POST['mobile']
        company_name = request.POST['company_name']
        address = request.POST['address']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']

        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('register_merchant')

        if username:
            if User.objects.filter(email=username).exists():
                messages.error(request, "Email Already Exists")
                return redirect('register_merchant')

        user = User.objects.create(username=username, password=password, email=username, name=name, mobile=mobile, is_merchant=True)
        user.set_password(password)
        user.save()

        admin = MerchantUser.objects.create(
            email=username,
            name=name,
            company_name=company_name,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            country=country,
        )
    
    return render(request, 'parking_dashboard/register.html')

@login_required(login_url='login')
def logout_view(request):
    if request.user.is_merchant:
        request.user.is_login = False
        request.user.save()

    logout(request)
    messages.success(request, "Logout Successfully")
    return render(request, 'parking_dashboard/login.html')




############# Forget Password #####################


def generate_otp():
    otp = ''.join(random.choices(string.digits, k=5))
    return otp


# Send OTP via email
def send_otp_email(user, otp):
    subject = 'Password Reset OTP'
    message = f'Your OTP for password reset is: {otp}'
    from_email = 'noreplay@parking.justapay.in'
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            user.otp = otp
            user.save()

            send_otp_email(user, otp)
            messages.success(request, "OTP sent successfully")

            # Redirect to OTP verification page
            return redirect('verify_otp', user_id=user.id)
        except User.DoesNotExist:
            messages.error(request, "User Not Found")
            return redirect('forgot_password')

    return render(request, 'parking_dashboard/admin_dashboard/forgot-password.html')



def verify_otp(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        
        if user.otp == entered_otp:
            messages.success(request, "otp verified successfully")
            return render(request, 'parking_dashboard/admin_dashboard/reset_password.html', {'user': user})
        else:
            messages.error(request, "Invalid OTP")
    
    return render(request, 'parking_dashboard/admin_dashboard/otp-verification.html', {'user': user})

def reset_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        new_password = request.POST['new_password']
        user.set_password(new_password)
        user.otp = None
        user.save()
        messages.success(request, "Password reset successfully")
        return redirect('login')

    return render(request, 'parking_dashboard/admin_dashboard/reset_password.html', {'user': user})


################# Date according Download #####################

def user_report_xls(request):
    user = request.user
    username = user.username
    ad = MerchantUser.objects.get(email=username)
    data_queryset = ParkingUser.objects.filter(merchant_id=ad)

    data = list(data_queryset.values())
    for item in data:
        for key, value in item.items():
            if isinstance(value, timezone.datetime):
                item[key] = value.replace(tzinfo=None)

    data_df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="parking_user.xlsx"'

    data_df.to_excel(response, index=False)

    return response




def date_according_download(request):
    user = request.user
    username = user.username
    ad = MerchantUser.objects.get(email=username)

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        data_queryset = ParkingUser.objects.filter(merchant_id=ad, created_on__gte=start_date, created_on__lte=end_date)

        data = list(data_queryset.values())
        for item in data:
            for key, value in item.items():
                if isinstance(value, timezone.datetime):
                    item[key] = value.replace(tzinfo=None)

        data_df = pd.DataFrame(data)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="parking_user_on_date.xlsx"'

        data_df.to_excel(response, index=False)

        return response

    return render(request, 'parking_dashboard/admin_dashboard/parkinguser/index.html')



###########################  Bulk Data Upload for merchant-user/parking-user  #######################

# def bulk_add_merchant(request):
#     if request.method == 'POST':
#         admin_id = 1

#         admin1 = Admin.objects.get(id=admin_id)

#         for i in range(1000):
#             username = f"merchant_{i}@gmail.com"
#             password = "admin"
#             name = "Merchant Name"
#             mobile = "1234567890"
#             company_name = "Company Name"
#             address = "Merchant Address"
#             city = "City"
#             state = "State"
#             pincode = "123456"
#             country = "Country"
#             bike_price = 10
#             auto_price = 20
#             car_price = 30
#             pickup_price = 40
#             ev_price = 50
#             truck_price = 60
#             custom_hours = 8
#             profile_img = "https://buffer.com/library/content/images/2023/10/free-images.jpg"
#             description = "Here where you control information."

#             user = User.objects.create(username=username, email=username, name=name, mobile=mobile, is_merchant=True)
#             user.set_password(password)
#             user.save()

#             merchant = MerchantUser.objects.create(
#                 admin=admin1,
#                 user=user,
#                 email=username,
#                 name=name,
#                 mobile=mobile,
#                 company_name=company_name,
#                 address=address,
#                 city=city,
#                 state=state,
#                 pincode=pincode,
#                 country=country,
#                 bike_price=bike_price,
#                 auto_price=auto_price,
#                 car_price=car_price,
#                 pickup_price=pickup_price,
#                 ev_price=ev_price,
#                 truck_price=truck_price,
#                 custom_hours=custom_hours,
#                 profile_img=profile_img,
#                 description=description,
#                 is_merchant=True
#             )

#         messages.success(request, "1000 Merchants Created Successfully.")
#         return redirect('merchantpending')

#     context = {
#         'messages': messages.get_messages(request),
#     }

#     return render(request, 'parking_dashboard/admin_dashboard/index.html', context)


# def change_merchant_status(request):
#     merchants_to_approve = MerchantUser.objects.filter(status='Pending')

#     for merchant in merchants_to_approve:
#         merchant.status = 'Approved'
#         merchant.save()

#     return redirect('merchantapproved')


# def all_merchant_parking(request):
#     merchants = MerchantUser.objects.all()
#     print(merchants, 'BBBBBBBBBBBBBBBBBBBBBBBBBBBB')

#     for merchant in merchants:
#         for i in range(500):
#             vehicle_number = f"RJ14CR4{i}"
#             name = "Parking Name"
#             mobile = "1234567890"
#             status = "Car"
#             time_status = "In"
#             price = 20
#             vehicle_hour = 12

#             parking = ParkingUser.objects.create(
#                 merchant_id=merchant,
#                 name=name,
#                 mobile=mobile,
#                 vehicle_number=vehicle_number,
#                 status=status,
#                 time_status=time_status,
#                 price=price,
#                 vehicle_hour=vehicle_hour
#             )
            
#             print(parking, 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
#     messages.success(request, "500 Parking Created Successfully.")
#     return redirect('merchantapproved')