from django.urls import path
from . import views

urlpatterns = [
    path('status/', views.connection_status),
    path('send-otp/', views.SendOtpView.as_view(), name='send_otp'),
    path('verify-otp/', views.VerifyOTPView.as_view()),
    path('me/', views.UserInfoView.as_view())
]
