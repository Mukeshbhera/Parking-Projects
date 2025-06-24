from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import *
from drf_spectacular.utils import extend_schema_field
from .models import User, MerchantUser,Resellers
from enum import Enum
from .enums import StatusEnum


@extend_schema_field(StatusEnum)
class UserSerializer(serializers.ModelSerializer):
    token_detail = serializers.SerializerMethodField("get_token_detail")

    class Meta:
        model = User
        fields = ('id', 'name', 'mobile', 'email', 'username', 'is_admin', 'is_merchant', 'is_reseller', 'is_reseller_merchant', 'created_date', 'token_detail',)
        extra_kwargs = {
            'token_detail': {'read_only': True}
        }

    def get_token_detail(self, obj) -> str:
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def get_user(self, request):
        user = request
        return user


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id','user','name','admin_id','mobile','email','status','company_name','address','city','pincode','state','country','created_on')


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantUser
        fields = ['id','admin','resellers','merchant_id','name','email','mobile','status','company_name','address','city','pincode','state','country','description','bike_price','auto_price','car_price','pickup_price','ev_price','truck_price','custom_hours', 
                  'profile_img','is_bike','is_car','is_auto','is_pickup','is_ev','is_truck','name_visibility','name_mandatory','mobile_visibility','mobile_mandatory','captcha_visibility','captcha_mandatory','created_on',]

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id','merchant_id','header_name','footer_home','footer_enter_user','footer_profile','home_colection_price','home_settled','home_unsettled','home_button_in','home_button_out','all_enter_user','created_date','updated_date']


class ResellersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resellers
        fields = ['id','admin','name','email','mobile','status','company_name','address','city','pincode','state','country','created_on']



# class ParkingUserListSerializer(serializers.ListSerializer):
#     def update(self, instances, validated_data):
#         instance_mapping = {instance.id: instance for instance in instances}

#         for item in validated_data:
#             instance_id = item['id']
#             instance = instance_mapping.get(instance_id, None)
#             if instance:
#                 self.child.update(instance, item)
#         return instances
    
class ParkinguserSerializer(serializers.ModelSerializer):
    class Meta:
        # list_serializer_class = ParkingUserListSerializer
        model = ParkingUser
        fields = ['id','merchant_id','parking_id','name','mobile','captcha','vehicle_number','price','vehicle_hour','status','time_status','vehicle_out_time','created_on']
    
