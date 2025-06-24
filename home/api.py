from django.shortcuts import render
import datetime
from django.utils import timezone
from home.models import User, MerchantUser, Resellers
from .serializers import *
from django.http.response import Http404
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework import status as tstatus
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view
import random
import string
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime, timezone

from rest_framework import viewsets
from rest_framework.decorators import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework import status
from rest_framework.response import Response
############### Swagger  ###########################
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_field

from rest_framework.authentication import TokenAuthentication

############### Admin API ######################
@extend_schema(
    request=AdminSerializer,
    responses={200: AdminSerializer}
)
class AdminAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request):
        res = {}
        try:
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            name = request.data.get('name', None)

            if email is None:
                res['status'] = False
                res['message'] = "Email is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
                res['status'] = False
                res['message'] = "Account already exist with this Email"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if name is None:
                res['status'] = False
                res['message'] = "Name is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if password is None:
                res['status'] = False
                res['message'] = "Password not Match!"
                res['data'] = []
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['username'] = email

            serializer = UserSerializer(
                data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save(is_admin=True)
                res_data = serializer.data
                user = User.objects.filter(id=res_data['id']).last()
                user.set_password(password)
                user.save()

                res['status'] = True
                res['message'] = "Admin Create successfully"
                res['data'] = res_data

            if request.user:
                    user = request.user.id
                    data = request.data
                    data["user"] = user
                    serializer = AdminSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        response = Response()
                        response.data = {
                            'message': 'Admin Created Successfully',
                            'data': serializer.data
                        }
                        return Response(res, status=status.HTTP_200_OK)

            else:
                res['status'] = False
                error = next(iter(serializer.errors))
                res['message'] = serializer.errors[str(error)][0]
                res['data'] = res_data
                return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

# Edit/Put

    def put(self, request):
        user = request.user
        user_to_update = User.objects.get(user=user)
        serializer = UserSerializer(instance=user_to_update,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {
            'message': 'User Updated Successfully',
            'data': serializer.data
        }
        return response

# Delete

    def delete(self, request):
        user = request.user
        user_to_delete =  User.objects.get(user=user)
        user_to_delete.delete()
        return Response({
            'message': 'User Deleted Successfully'
        })


############### Merchant API ######################
@extend_schema(
    request=MerchantSerializer,
    responses={200: MerchantSerializer}
)
class MerchantAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        user = request.user

        if user:
            email = user.username
            if email is None:
                return HttpResponseBadRequest("Email parameter is missing")
            mer = MerchantUser.objects.get(email=email)
            if mer:
                serializer = MerchantSerializer(mer)
                serialized_data = serializer.data
                res_data = serialized_data
                res['status'] = True
                res['message'] = "Merchant found successfully"
                res['data'] = res_data
                return Response(res, status=status.HTTP_200_OK)

            else:
                res['status'] = False
                res['message'] = "Merchant not found"
                return Response(res, status=status.HTTP_404_NOT_FOUND)
        else:
            res['status'] = False
            res['message'] = "User not authenticated"
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        res = {}
        try:
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            name = request.data.get('name', None)
            bike_price = request.data.get('bike_price', None)
            auto_price = request.data.get('auto_price', None)
            car_price = request.data.get('car_price', None)

            if email is None:
                res['status'] = False
                res['message'] = "Email is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
                res['status'] = False
                res['message'] = "Account already exist with this Email"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if name is None:
                res['status'] = False
                res['message'] = "Name is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if bike_price is None:
                res['status'] = False
                res['message'] = "Bike Price is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if auto_price is None:
                res['status'] = False
                res['message'] = "Auto Price is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if car_price is None:
                res['status'] = False
                res['message'] = "Car Price is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if password is None:
                res['status'] = False
                res['message'] = "Password not Match!"
                res['data'] = []
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['username'] = email

            user_id = request.user.id
            user = User.objects.get(id=user_id)
            
            serializer = UserSerializer(
                data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                if user.is_reseller:
                    serializer.validated_data['is_reseller_merchant'] = True
                elif user.is_admin:
                    serializer.validated_data['is_merchant'] = True
                instance = serializer.save()
                password = data.get('password')
                if password:
                    instance.set_password(password)
                    instance.save()

                res_data = serializer.data

                res = {
                    'status': True,
                    'message': "Merchant Created successfully",
                    'data': res_data
                }

            if request.user:
                    email = request.user.email
                    if request.user.is_reseller:
                        user1 = Resellers.objects.get(email=email)
                        userem = user1.id
                        data = request.data
                        data["resellers"] = userem

                    # admins_with_email = Admin.objects.filter(email=email)
                    if request.user.is_admin:
                        user1 = Admin.objects.get(email=email)
                        # user1 = admins_with_email.first()
                        userem = user1.id
                        data = request.data
                        data["admin"] = userem
                        serializer = MerchantSerializer(data=data)

                    serializer = MerchantSerializer(data=data)
                    if serializer.is_valid():
                        if user.is_reseller:
                            serializer.validated_data['is_reseller'] = True
                        elif user.is_admin:
                            serializer.validated_data['is_merchant'] = True
                        serializer.save()
                        response = Response()
                        response.data = {
                            'message': 'Merchant Created Successfully',
                            'data': serializer.data
                        }
                        return Response(res, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                res['status'] = False
                error = next(iter(serializer.errors))
                res['message'] = serializer.errors[str(error)][0]
                res['data'] = res_data
                return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

# Edit/Put

    def put(self, request):

        user = request.user.username
        user_to_update = MerchantUser.objects.get(email=user)
        serializer = MerchantSerializer(instance=user_to_update,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {
            'message': 'Merchant Updated Successfully',
            'data': serializer.data
        }
        return response

# Delete

    def delete(self, request):
        user = request.user
        user_to_delete =  MerchantUser.objects.get(user=user)
        print('deleted successfull', user_to_delete)
        user_to_delete.delete()
        print('print-2 user', user_to_delete)
        return Response({
            'message': 'Merchant Deleted Successfully'
        })

class LabelAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        if request.user:
            user_email = request.user.email
            merchant = MerchantUser.objects.get(email=user_email)
            label = Label.objects.get(merchant_id=merchant)
            serializer_class = LabelSerializer(label)
            serialized_data = serializer_class.data
            res['status'] = True
            res['message'] = "Data Get Successfully"
            res['data'] = serialized_data
            return Response(res, status=status.HTTP_200_OK)
        
        else:
            res['status'] = False
            res['message'] = "This Data not found"
            return Response(res, status=status.HTTP_404_NOT_FOUND)
    

############### Reseller Merchant API ######################

# class ResellerMerchantAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         res = {}
#         try:
#             email = request.data.get("email", None)
#             password = request.data.get("password", None)
#             name = request.data.get('name', None)

#             if email is None:
#                 res['status'] = False
#                 res['message'] = "Email is Required"
#                 res['data'] = []
#                 return Response(res, status=status.HTTP_404_NOT_FOUND)

#             if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
#                 res['status'] = False
#                 res['message'] = "Account already exist with this Email"
#                 res['data'] = []
#                 return Response(res, status=status.HTTP_404_NOT_FOUND)

#             if name is None:
#                 res['status'] = False
#                 res['message'] = "Name is Required"
#                 res['data'] = []
#                 return Response(res, status=status.HTTP_404_NOT_FOUND)

#             if password is None:
#                 res['status'] = False
#                 res['message'] = "Password not Match!"
#                 res['data'] = []
#                 return Response(res, status=status.HTTP_400_BAD_REQUEST)

#             data = request.data
#             try:
#                 data._mutable = True
#             except:
#                 pass
#             data['username'] = email

#             serializer = UserSerializer(
#                 data=data, context={'request': request})
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save(is_reseller_merchant=True)
#                 res_data = serializer.data
#                 user = User.objects.filter(id=res_data['id']).last()
#                 user.set_password(password)
#                 user.save()

#                 res['status'] = True
#                 res['message'] = "Reseller Merchant Create successfully"
#                 res['data'] = res_data

#             if request.user:
#                     user = request.user.id
#                     email = request.user.email
#                     user1= Resellers.objects.get(email=email)
#                     userem = user1.id
#                     data = request.data
#                     data["resellers"] = userem
#                     serializer = ResellerMerchantSerializer(data=data)
#                     if serializer.is_valid():
#                         serializer.save()
#                         response = Response()
#                         response.data = {
#                             'message': 'Reseller Merchant Created Successfully',
#                             'data': serializer.data
#                         }
#                         return Response(res, status=status.HTTP_200_OK)

#             else:
#                 res['status'] = False
#                 error = next(iter(serializer.errors))
#                 res['message'] = serializer.errors[str(error)][0]
#                 res['data'] = res_data
#                 return Response(res, status=status.HTTP_200_OK)

#         except Exception as e:
#             res['status'] = False
#             res['message'] = str(e)
#             res['data'] = []
#             return Response(res, status=status.HTTP_400_BAD_REQUEST)


#     def put(self, request):
#         user = request.user
#         user_to_update = ResellerMerchant.objects.get(user=user)
#         serializer = ResellerMerchantSerializer(instance=user_to_update,data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         response = Response()
#         response.data = {
#             'message': 'Reseller Merchant Updated Successfully',
#             'data': serializer.data
#         }
#         return response


#     def delete(self, request):
#         user = request.user
#         user_to_delete =  ResellerMerchant.objects.get(user=user)
#         print('deleted successfull', user_to_delete)
#         user_to_delete.delete()
#         print('print-2 user', user_to_delete)
#         return Response({
#             'message': 'Reseller Merchant Deleted Successfully'
#         })

############### Cunsumer API ######################
@extend_schema(
    request=ResellersSerializer,
    responses={200: ResellersSerializer}
)
class ResellerAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        res = {}
        try:
            email = request.data.get("email", None)
            password = request.data.get("password", None)
            name = request.data.get('name', None)

            if email is None:
                res['status'] = False
                res['message'] = "Email is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
                res['status'] = False
                res['message'] = "Account already exist with this Email"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if name is None:
                res['status'] = False
                res['message'] = "Name is Required"
                res['data'] = []
                return Response(res, status=status.HTTP_404_NOT_FOUND)

            if password is None:
                res['status'] = False
                res['message'] = "Password not Match!"
                res['data'] = []
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            data = request.data
            try:
                data._mutable = True
            except:
                pass
            data['username'] = email


            serializer = UserSerializer(
                data=data, context={'request': request})
            if serializer.is_valid(raise_exception=True):
                serializer.save(is_reseller=True)
                res_data = serializer.data
                user = User.objects.filter(id=res_data['id']).last()
                user.set_password(password)
                user.save()

                res['status'] = True
                res['message'] = "Reseller Create successfully"
                res['data'] = res_data


            if request.user:
                    user = request.user.id
                    email = request.user.email
                    user1= Admin.objects.get(email=email)
                    userem = user1.id
                    data["admin"] = userem
                    serializer = ResellersSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        response = Response()
                        response.data = {
                            'message': 'Reseller in Created Successfully',
                            'data': serializer.data
                        }
                    return Response(res, status=status.HTTP_200_OK)

            else:
                res['status'] = False
                error = next(iter(serializer.errors))
                res['message'] = serializer.errors[str(error)][0]
                res['data'] = res_data
                return Response(res, status=status.HTTP_200_OK)

        except Exception as e:
            res['status'] = False
            res['message'] = str(e)
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        user_to_update = Resellers.objects.get(user=user)
        serializer = ResellersSerializer(instance=user_to_update,data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {
            'message': 'Reseller Updated Successfully',
            'data': serializer.data
        }
        return response

#################### Delete  ###############

    def delete(self, request):
        user = request.user
        user_to_delete = Resellers.objects.get(user=user)
        print('deleted successfull', user_to_delete)
        user_to_delete.delete()
        print('print-2 user', user_to_delete)
        return Response({
            'message': 'Merchant Deleted Successfully'
        })
        
############### Vehiclelist User API ######################
# class VehicleListAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         res = {}
#         if request.user:
#             user_email = request.user.email
#             merchant = MerchantUser.objects.get(email=user_email)
#             print(merchant,'kkkkkkkkkkkkkkkkkkkk')
            
#             if merchant:
#                 serializer = MerchantSerializer(merchant)
#                 serialized_data = serializer.data
#                 res_data = serialized_data
#                 res['status'] = True
#                 res['message'] = "VehicleList successfully"
#                 res['data'] = res_data
#                 return Response(res,status=status.HTTP_200_OK) 
#         else:        
#             res['status'] = False
#             res['message'] = "VehicleList Not Found"
#             return Response(res,status=status.HTTP_404_NOT_FOUND) 
                


############## Permission Field  #####################


class PermissionField(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        res = {}
        if request.user:
            users = request.user.email
            merchantuser = MerchantUser.objects.get(email=users)

            serializer_class = MerchantSerializer(merchantuser)
            serializeds = serializer_class.data
            res['status'] = True
            res['message'] = "Permission Field "
            res['data'] = serializeds
            return Response(res, status=status.HTTP_200_OK)

        else:
            res['status'] = False
            res['message'] = "Permission Field not found"
            return Response(res, status=status.HTTP_404_NOT_FOUND)



############### Parking User API ######################

@extend_schema(
    request=ParkinguserSerializer,
    responses={200: ParkinguserSerializer}
)
class ParkinguserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request,):
        res = {}
        if request.user:
            user = request.user
            park1 = MerchantUser.objects.get(email=user.email)
            vehicle_number = request.GET.get('vehicle_number', None)
            time_status = request.GET.get('time_status', None)
            merchant_id = request.GET.get('merchant_id', None)
            vehicle_date_range_str = request.GET.get('vehicle_date_range', None)
            parking_id = request.GET.get('parking_id', None)
            park = ParkingUser.objects.filter(vehicle_number=vehicle_number).first()

            # park2 = ParkingUser.objects.filter(merchant_id=merchant_id).first()
            # park3 = ParkingUser.objects.filter(parking_id=parking_id).first()
            
            if vehicle_number is None and time_status is None and merchant_id is None and parking_id is None :
                merchant_user = get_object_or_404(MerchantUser, email=user.email)
                queryset = ParkingUser.objects.filter(merchant_id=merchant_user, time_status='In')
                if queryset.exists():
                    park1 = user
                    bike_price = float(merchant_user.bike_price)
                    auto_price = float(merchant_user.auto_price)
                    car_price = float(merchant_user.car_price)
                    pickup_price = float(merchant_user.pickup_price)
                    ev_price = float(merchant_user.ev_price)
                    truck_price = float(merchant_user.truck_price)

                    for park in queryset:
                        time = park.created_on
                        time_aware = time.replace(tzinfo=timezone.utc)
                        difference = datetime.now(timezone.utc) - time_aware
                        sec = difference.total_seconds()
                        minutes = sec // 60
                        hours = minutes // 60
                        remaining_minutes = minutes % 60
                        value_zero_convert = remaining_minutes * 0
                        convert_value_add = value_zero_convert + 60
                        count_hour_one = convert_value_add / 60
                        total_hours = hours + count_hour_one

                        if park.status == 'Bike':
                            calculate = str(bike_price * total_hours)
                        elif park.status == 'Auto':
                            calculate = str(auto_price * total_hours)
                        elif park.status == 'Car':
                            calculate = str(car_price * total_hours)
                        elif park.status == 'Pickup':
                            calculate = str(pickup_price * total_hours)
                        elif park.status == 'Ev':
                            calculate = str(ev_price * total_hours)
                        elif park.status == 'Truck':
                            calculate = str(truck_price * total_hours)
                        else:
                            calculate = "0.0"

                        park.price = calculate
                        park.vehicle_hour = total_hours

                    ParkingUser.objects.bulk_update(queryset, ['price', 'vehicle_hour'])

                    serializer_class = ParkinguserSerializer(queryset, many=True)
                    serializeds = serializer_class.data
                    res['status'] = True
                    res['message'] = "In Data Get Successfully"
                    res['data'] = serializeds
                    return Response(res, status=status.HTTP_200_OK)

            if merchant_id and vehicle_date_range_str:
                input_date = datetime.strptime(vehicle_date_range_str, '%Y-%m-%d')
                merchant = ParkingUser.objects.filter(merchant_id=merchant_id,vehicle_out_time__date=input_date.date(),time_status='Out')

                if merchant:
                    serializer_class = ParkinguserSerializer(merchant, many=True)
                    serializeds = serializer_class.data
                    res['status'] = True
                    res['message'] = "Out Data Get Successfully"
                    res['data'] = serializeds
                    return Response(res, status=status.HTTP_200_OK)
        
            if vehicle_number and time_status == "In":
                if vehicle_number:
                    try:
                        serializer_class = ParkingUser.objects.filter(vehicle_number=vehicle_number, time_status='In')
                        serializeds = ParkinguserSerializer(serializer_class, many=True)
                        park = serializer_class.first()

                        if not park:
                            res['status'] = False
                            res['message'] = "This in Data is Already Out"
                            return Response(res, status=status.HTTP_404_NOT_FOUND)
                    
                        if park.status == 'Bike':
                            pa = park.id

                            vehicle_hour = float(park1.custom_hours)
                            price = float(park1.bike_price)

                            park = ParkingUser.objects.get(id=pa, time_status=time_status)
                            time = park.created_on
                            time_aware = time.replace(tzinfo=timezone.utc)
                            difference = datetime.now(timezone.utc) - time_aware
                            sec = difference.total_seconds()
                            minutes = sec // 60
                            hours = minutes // 60
                            remaining_minutes = minutes % 60
                            
                            value_zero_convert = remaining_minutes * 0
                            convert_value_add = value_zero_convert + 60
                            count_houre_one = convert_value_add/60
                            total_houres = hours + count_houre_one

                            if (float(vehicle_hour) == float(total_houres)) or (float(vehicle_hour) < float(total_houres)):
                                
                                hours_multiple = total_houres / vehicle_hour

                                integer_part = int(hours_multiple)
                                fractional_part = 1
                                result_float = float(integer_part + fractional_part)
                                final_result = result_float * price
                                park.price = final_result
                                park.vehicle_hour = total_houres
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data

                                res['status'] = True
                                res['message'] = "Bike Price and Houres Data Get Update Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            else:
                                park.vehicle_hour = vehicle_hour
                                park.price = price
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Bike Data Get Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            
                        if park.status == 'Auto':
                            pa = park.id
                            vehicle_hour = float(park1.custom_hours)
                            price = float(park1.auto_price)
                            park = ParkingUser.objects.get(id=pa, time_status=time_status)
                            time = park.created_on
                            time_aware = time.replace(tzinfo=timezone.utc)
                            difference = datetime.now(timezone.utc) - time_aware
                            sec = difference.total_seconds()
                            minutes = sec // 60
                            hours = minutes // 60
                            remaining_minutes = minutes % 60
                            
                            value_zero_convert = remaining_minutes * 0
                            convert_value_add = value_zero_convert + 60
                            count_houre_one = convert_value_add/60
                            total_houres = hours + count_houre_one
                                
                            if (float(vehicle_hour) == float(total_houres)) or (float(vehicle_hour) < float(total_houres)):
                                hours_multiple = total_houres / vehicle_hour
                                integer_part = int(hours_multiple)
                                fractional_part = 1
                                result_float = float(integer_part + fractional_part)
                                final_result = result_float * price
                                park.price = final_result
                                park.vehicle_hour = total_houres
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data

                                res['status'] = True
                                res['message'] = "Auto Price and Houres Data Get Update Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            else:
                                park.vehicle_hour = vehicle_hour
                                park.price = price
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Auto Data Get Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)


                        if park.status == 'Car':
                            pa = park.id
                            vehicle_hour = float(park1.custom_hours)
                            price = float(park1.car_price)
                            park = ParkingUser.objects.get(id=pa, time_status=time_status)
                            time = park.created_on
                            time_aware = time.replace(tzinfo=timezone.utc)
                            difference = datetime.now(timezone.utc) - time_aware
                            sec = difference.total_seconds()
                            minutes = sec // 60
                            hours = minutes // 60
                            remaining_minutes = minutes % 60
                            
                            value_zero_convert = remaining_minutes * 0
                            convert_value_add = value_zero_convert + 60
                            count_houre_one = convert_value_add/60
                            total_houres = hours + count_houre_one
                            
                            if (float(vehicle_hour) == float(total_houres)) or (float(vehicle_hour) < float(total_houres)):
                                hours_multiple = total_houres / vehicle_hour
                                integer_part = int(hours_multiple)
                                fractional_part = 1
                                result_float = float(integer_part + fractional_part)
                                final_result = result_float * price
                                park.price = final_result
                                park.vehicle_hour = total_houres
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Car Price and Houres Data Get Update Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            else:
                                park.vehicle_hour = vehicle_hour
                                park.price = price
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Car Data Get Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)

                        if park.status == 'Pickup':
                            pa = park.id
                            vehicle_hour = float(park1.custom_hours)
                            price = float(park1.pickup_price)
                            park = ParkingUser.objects.get(id=pa, time_status=time_status)
                            time = park.created_on
                            time_aware = time.replace(tzinfo=timezone.utc)
                            difference = datetime.now(timezone.utc) - time_aware
                            sec = difference.total_seconds()
                            minutes = sec // 60
                            hours = minutes // 60
                            remaining_minutes = minutes % 60
                            
                            value_zero_convert = remaining_minutes * 0
                            convert_value_add = value_zero_convert + 60
                            count_houre_one = convert_value_add/60
                            total_houres = hours + count_houre_one
                            
                            if (float(vehicle_hour) == float(total_houres)) or (float(vehicle_hour) < float(total_houres)):
                                hours_multiple = total_houres / vehicle_hour
                                integer_part = int(hours_multiple)
                                fractional_part = 1
                                result_float = float(integer_part + fractional_part)
                                final_result = result_float * price
                                park.price = final_result
                                park.vehicle_hour = total_houres
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Pickup Price and Houres Data Get Update Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            else:
                                park.vehicle_hour = vehicle_hour
                                park.price = price
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Pickup Data Get Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            
                        if park.status == 'Ev':
                            pa = park.id
                            vehicle_hour = float(park1.custom_hours)
                            price = float(park1.ev_price)
                            park = ParkingUser.objects.get(id=pa, time_status=time_status)
                            time = park.created_on
                            time_aware = time.replace(tzinfo=timezone.utc)
                            difference = datetime.now(timezone.utc) - time_aware
                            sec = difference.total_seconds()
                            minutes = sec // 60
                            hours = minutes // 60
                            remaining_minutes = minutes % 60
                            
                            value_zero_convert = remaining_minutes * 0
                            convert_value_add = value_zero_convert + 60
                            count_houre_one = convert_value_add/60
                            total_houres = hours + count_houre_one
                            
                            if (float(vehicle_hour) == float(total_houres)) or (float(vehicle_hour) < float(total_houres)):
                                hours_multiple = total_houres / vehicle_hour
                                integer_part = int(hours_multiple)
                                fractional_part = 1
                                result_float = float(integer_part + fractional_part)
                                final_result = result_float * price
                                park.price = final_result
                                park.vehicle_hour = total_houres
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Ev Price and Houres Data Get Update Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            else:
                                park.vehicle_hour = vehicle_hour
                                park.price = price
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Ev Data Get Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            
                        if park.status == 'Truck':
                            pa = park.id
                            vehicle_hour = float(park1.custom_hours)
                            price = float(park1.truck_price)
                            park = ParkingUser.objects.get(id=pa, time_status=time_status)
                            time = park.created_on
                            time_aware = time.replace(tzinfo=timezone.utc)
                            difference = datetime.now(timezone.utc) - time_aware
                            sec = difference.total_seconds()
                            minutes = sec // 60
                            hours = minutes // 60
                            remaining_minutes = minutes % 60
                            
                            value_zero_convert = remaining_minutes * 0
                            convert_value_add = value_zero_convert + 60
                            count_houre_one = convert_value_add/60
                            total_houres = hours + count_houre_one
                            
                            if (float(vehicle_hour) == float(total_houres)) or (float(vehicle_hour) < float(total_houres)):
                                hours_multiple = total_houres / vehicle_hour
                                integer_part = int(hours_multiple)
                                fractional_part = 1
                                result_float = float(integer_part + fractional_part)
                                final_result = result_float * price
                                park.price = final_result
                                park.vehicle_hour = total_houres
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Truck Price and Houres Data Get Update Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)
                            else:
                                park.vehicle_hour = vehicle_hour
                                park.price = price
                                park.save()
                                serializer = ParkinguserSerializer(park)
                                serialized_data = serializer.data
                                res['status'] = True
                                res['message'] = "Truck Data Get Successfully"
                                res['data'] = serialized_data
                                return Response(res, status=status.HTTP_200_OK)

                    except ParkingUser.DoesNotExist:
                        res['status'] = False
                        res['message'] = "No Data Found for this Vehicle Number"
                        return Response(res, status=status.HTTP_200_OK)
                
                    res['status'] = False
                    res['message'] = "this Data Get not found"
                    res['data'] = []
                    return Response(res, status=status.HTTP_200_OK)
            res['status'] = False
            res['message'] = "This Data not found"
            return Response(res, status=status.HTTP_200_OK)
            

        res['status'] = False
        res['message'] = "Parking Data Not Found"
        return Response(res, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        res = {}
        if request.user:
            vehicle_type = request.POST.get('status')
            user = request.user.id
            email = request.user.email
            user1 = MerchantUser.objects.get(email=email)
            userem = user1.id
            data = request.data
            data = request.POST.copy()
            vehicle_number = data.get('vehicle_number')

            existing_entry = ParkingUser.objects.filter(vehicle_number=vehicle_number, time_status='In').first()
            if existing_entry:
                res['status'] = False
                res['message'] = "Vehicle with the same number is already parked"
                return Response(res)
            
            vehicle_hour = user1.custom_hours
        
            selected_vehicle_type = vehicle_type
            available_vehicle_types = ("Bike", "Auto", "Car","Pickup","Ev","Truck")
            if selected_vehicle_type in available_vehicle_types:
                if selected_vehicle_type == "Bike":
                    price = user1.bike_price
                elif selected_vehicle_type == "Auto":
                    price = user1.auto_price
                elif selected_vehicle_type == "Car":
                    price = user1.car_price
                elif selected_vehicle_type == "Pickup":
                    price = user1.pickup_price
                elif selected_vehicle_type == "Ev":
                    price = user1.ev_price
                elif selected_vehicle_type == "Truck":
                    price = user1.truck_price
            else:
                price = None

            data["price"] = price
            data["vehicle_hour"] = vehicle_hour
            
            data["merchant_id"] = userem
            captcha_files = request.FILES.getlist('captcha')
            if captcha_files:
                captcha_file = captcha_files[0]
                data["captcha"] = captcha_file
            serializer = ParkinguserSerializer(data=data)
            if serializer.is_valid():
                existing_vehicle = ParkingUser.objects.filter(vehicle_number=vehicle_number).first()
                if existing_vehicle:
                    existing_vehicle.time_status = 'Out'
                    existing_vehicle.save()
                serializer.save()

            serialized_data = serializer.data
            user = ParkingUser.objects.get(id=serialized_data['id'])
            
            user.price = price
            user.time_status='In'
            user.save()

            res['status'] = True
            res['message'] = "Parking User Create successfully"
            res['data'] = serialized_data
            return Response(res, status=status.HTTP_200_OK)
        
    
#######  Delete Parking Data  ######

    def delete(self, request):
        user = request.user
        user_to_delete = ParkingUser.objects.get(user=user)
        print('deleted successfull', user_to_delete)
        user_to_delete.delete()
        print('print-2 user', user_to_delete)
        return Response({
            'message': 'Merchant Deleted Successfully'
        })

######## Put ParkingEdit #########

    def put(self, request):
        num = request.GET.get('vehicle_number')
        user = request.user.username

        try:
            user_to_update = MerchantUser.objects.get(email=user)

            parking_users = ParkingUser.objects.filter(merchant_id=user_to_update.id, vehicle_number=num, time_status='In')

            if not parking_users.exists():
                return Response({'message': 'All Ready Updated'},
                status=status.HTTP_404_NOT_FOUND)

            for parking_user in parking_users:
                parking_user.time_status = 'Out'
                parking_user.save()

            response = Response()
            response.data = {
                'message': 'Parkingusers Updated Successfully',
                'data': ParkinguserSerializer(parking_users, many=True).data
            }
            return response

        except MerchantUser.DoesNotExist:
            return Response({'message': 'MerchantUser does not exist'}, status=status.HTTP_404_NOT_FOUND)



############# Login API  ####################
@extend_schema(
    request=UserSerializer,
    responses={200: UserSerializer}
)
class LoginApiView(APIView):
    """ API for login """
    permission_classes = [AllowAny]

    def post(self, request):
        res = {}
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        if username is None:
            res['status'] = False
            res['message'] = "Email is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if password is None:
            res['status'] = False
            res['message'] = "Password is required"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            res['status'] = False
            res['message'] = "Invalid Email or Password!"
            res['data'] = []
            return Response(res, status=status.HTTP_205_RESET_CONTENT)
        serializer = UserSerializer(
            user, read_only=True, context={'request': request})

        if serializer:
            if user.is_superuser:
                print(user.is_superuser, 'PPPPPPPPPPPPPPPPPPP')
                res['status'] = True
                res['message'] = "Superuser Login successfully"
                res['data'] = serializer.data
                return Response(res, status=status.HTTP_200_OK)

            if user.is_admin:
                user1 = user.username
                merchant = Admin.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status=='Approved':
                    res['status'] = True
                    res['message'] = "Admin Login successfully"
                    res['admin_id'] = merchant.id
                else:
                    res['message'] = "Your Account Not Approved"
                    return Response(res)

            if user.is_merchant:
                if user.is_login:
                    res['message'] = "You are already logged in from another system."
                    return Response(res)
                user.is_login = True
                user.save()
                print(user, 'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLl')

                user1 = user.username
                merchant = MerchantUser.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status=='Approved':
                    res['status'] = True
                    res['message'] = "Merchant Login successfully"
                    res['merchant_id'] = merchant.id

                else:
                    res['message'] = "Your Account Not Approved"
                    return Response(res)

            if user.is_reseller:
                user1 = user.username
                reseller = Resellers.objects.get(email=user1)
                reseller_status = reseller.status
                if reseller_status=='Approved':
                    res['status'] = True
                    res['message'] = "reseller Login successfully"
                    res['reseller_id'] = reseller.id
                else:
                    res['message'] = "Your Account Not Approved"
                    return Response(res)

            if user.is_reseller_merchant:
                user1 = user.username
                merchant = MerchantUser.objects.get(email=user1)
                merchant_status = merchant.status
                if merchant_status=='Approved':
                    res['status'] = True
                    res['message'] = "Resller Merchant Login successfully"
                    res['merchant_id'] = merchant.id
                else:
                    res['message'] = "Your Account Not Approved"
                    return Response(res)

            res['data'] = serializer.data
            return Response(res, status=status.HTTP_200_OK)

        else:
            res['status'] = False
            res['message'] = "No recored found for entered data"
            res['data'] = []
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

# ##############ForgotPasswordAPI########################################

@csrf_exempt
def send_otp_email(request):
    res = {}
    if request.method == 'POST' :
        email = request.POST.get('username')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        otp = ''.join(random.choices(string.digits, k=5))
        user.otp = otp
        user.save()
        subject = 'Your OTP Code'
        message = f'Your OTP code is: {otp}'
        from_email = 'manishkumawat303007@gmail.com'
        recipient_list = [email]
        valu = send_mail(subject, message, from_email, recipient_list)
        res['status'] = True
        res['message'] = "OTP sent successfully"
        res['user_id'] = user.id 
        res['data'] = valu
        
        return JsonResponse(res,status=status.HTTP_200_OK)
    

@csrf_exempt
def verify_otp(request):
    res = {}
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            user = User.objects.get(otp=otp)
            print(user, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAa')
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.otp == otp:
            user.otp = None
            user.save()
            res['status'] = True
            res['message'] = "OTP verified successfully"
            res['user_id'] = user.id 
            return JsonResponse(res, status=status.HTTP_200_OK)
        else:
            res['status'] = False
            res['message'] = "Invalid OTP"
            return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)
        
@csrf_exempt
def reset_password(request):
    res = {}
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_password = request.POST.get('new_password')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if user.otp is None:
            # OTP has been verified
            user.set_password(new_password)
            user.save()
            res['status'] = True
            res['message'] = "Password reset successfully"
            res['user_id'] = user.id 
            return JsonResponse(res, status=status.HTTP_200_OK)
        else:
            res['status'] = False
            res['message'] = "OTP verification required before resetting password"
            return JsonResponse(res, status=status.HTTP_400_BAD_REQUEST)

