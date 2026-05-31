from django.urls import path
from .views import (
    RegisterView,
    LogoutView,
    CustomTokenObtainPairView,
    VerifyEmailView,
    ForgotPasswordView

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),

    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('logout/', LogoutView.as_view(), name='logout'),

    path(
        'verify-email/<int:user_id>/<str:token>/',
        VerifyEmailView.as_view(),
        name='verify_email'
    ),
    path(
        'forgot-password/',
        ForgotPasswordView.as_view(),
        name='forgot-password'
    ),

]