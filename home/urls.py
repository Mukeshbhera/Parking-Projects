from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [

   ############## Front Page URL #################

   path('', views.front_layout, name='frontuser'),
   
   ############### Dashboard URl ########################

   path('login-user/', views.login_in, name='login'),
   path('forgot-password/', views.forgot_password, name='forgot_password'),
   path('otp-verification/<int:user_id>/', views.verify_otp, name='verify_otp'),
   path('reset_password/<int:user_id>/', views.reset_password, name='reset_password'),
   path('merchant-register/', views.register_merchant, name='register_merchant'),
   path('logout/', views.logout_view, name='logout'),
   path('admin-dashboard/', views.addsuperadmin, name='addsuperadmin'),
   # path('edit-admin/<int:id>/', views.adminedit, name='editadmin'),
   path('adminedit/<int:id>/', views.adminedit, name='editadmin'),
   path('admin-user-profile/', views.admin_profile, name='adminuserprofile'),
   

   ################# Merchant URL ####################

   path('add-merchant/', views.add_merchant, name='addmerchan'),
   path('update_logout_status/', views.update_logout_status, name='update_logout_status'),
   # path('bulk_add_merchant/', views.bulk_add_merchant, name='bulk_add_merchant'),
   # path('change_merchant_status/', views.change_merchant_status, name='change_merchant_status'),
   # path('bulk-parking-user-create/', views.all_merchant_parking, name='change_merchant_status'),
   path('merchant-user-profile/', views.merchant_user_profile, name='merchantuserprofile'),
   path('meredit/<int:id>/', views.indexedit, name='meredit'),

   
   path('merchant-user-profile/', views.admin_profile, name='merchantuserprofile'),
   path('merchant-approved/', views.admin_merchant_appro, name='merchantapproved'),
   path('merchant-pending/', views.admin_merchant_pen, name='merchantpending'),
   path('merchant-cancel/', views.admin_merchant_can, name='merchantcancel'),
   path('merchant_update_status/', views.dashboard_merchant_update_status, name='merchant_update_status'),
   path('addmultimerchant/', views.multi_merchant, name='addmultimerchant'),
   
   ################# Resellers URL ####################

   path('add-reseller/', views.add_reseller, name='addreseller'),
   path('reseller-user-profile/', views.reseller_profile, name='reselleruserprofile'),
   path('reseller-approved/', views.admin_reseller_appro, name='resellerapproved'),
   path('reseller-pending/', views.admin_reseller_pen, name='resellerpending'),
   path('reseller-cancel/', views.admin_reseller_can, name='resellercancel'),
   path('reseller_update_status/', views.dashboard_reseller_update_status, name='reseller_update_status'),
   path('reselleredit/<int:id>/', views.reselleredit, name='reselleredit'),

################# Resellers Merchant URL ####################
   path('reseller_merchant/', views.resller_merchant_approve, name='resellermerchantapprove'),
   path('reseller_merchant_pending/', views.resller_merchant_pending, name='resellermerchantpending'),
   path('reseller_merchant_cancel/', views.resller_merchant_cancel, name='resellermerchantcancel'),
   path('add_reseller_merchant/', views.add_reseller_merchant, name='addresellermerchant'),
   path('reseller_merchant_status_update/', views.reseller_merchant_status, name='reseller_merchant_status'),
   path('resellermeredit/<int:id>/', views.resellermeredit, name='resellermeredit'),
   path('addmultiresellermerchant/', views.addmultiresellermerchant, name='addmultiresellermerchant'),
   

################# Parking User URL ####################
   path('parking_user/', views.parking, name='parkinguser'),
   path('parking_user-profile/', views.merchant_user_profile, name='parkinguserprofile'),
   path('all-merchant-park/', views.all_merchant_park, name='all_merchant_park'),
   path('merchant-parking-user-all/<int:pk>/', views.merchant_parking_user_all, name='merchant_parking_user_all'),

################# Label User URL ####################
   path('appcustomization/', views.appcustomization, name='appcustomization'),
   
################# Setting User URL ####################
   path('setting/', views.setting, name='setting'),
   
################# ParkUser Report URL ####################
   path('user_report/', views.user_report_xls, name='user_report'),
   path('user_report_download_range/', views.date_according_download, name='user_report_download_range'),
   


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

