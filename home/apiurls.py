from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from .api import *
from rest_framework import routers
from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('login/', LoginApiView.as_view(), name="login"),
    path('send_otp/', send_otp_email, name='send_otp'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('reset_password/', reset_password, name='reset_password'),

    # path('reset_password/', reset_password, name='reset_password'),
    path('create-admin/', AdminAPIView.as_view()),
    path('create-merchant/', MerchantAPIView.as_view()),
    path('merchant-app-label/', LabelAPIView.as_view()),
    path('create-reseller/', ResellerAPIView.as_view()),
    path('parkinguser/', ParkinguserAPIView.as_view()),
    path('permission-field/', PermissionField.as_view()),

    path('api-token-auth/', rest_views.obtain_auth_token, name='api-token-auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

