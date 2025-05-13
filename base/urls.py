from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path('auth/sign-up/',SignUpView.as_view()),
    path('auth/log-in/', UserLoginApiView.as_view()),
    path('auth/log-out/', LogoutAPIView.as_view()),
    path('auth/get-code-reset-password/', GetCodeResetPassword.as_view()),
    path('auth/veryfiy-account/<str:pk>/', VerifyAccount.as_view()),
    path('auth/verify-code-to-reset-password/<str:pk>/', VerifyCodeToChangePassword.as_view()),
    path('auth/reset-password/<str:pk>/', ResetPasswordView.as_view()),
    path('setting/list-info-user/<str:pk>/', ListInformationUserView.as_view()),
    path('setting/update-image/<str:pk>/',UpdateImageUserView.as_view()),

    path('list-create-bouquets/',ListCreateBouquetsView.as_view()),
    path('list-create-medical-tests/',ListCreateMedicalTestsView.as_view()),
    path('get-bouquet/<str:pk>/',GetBouquetsView.as_view()),
    
    path('list-create-item-cart/', ListCreateItemCart.as_view(), name='list_create_item_cart'),
    path('delete-item-from-cart/<str:item_id>/', DeleteItemFromCart.as_view(), name='delete_item_from_cart'),
    path('list-create-order/', ListCreateOrder.as_view(), name='list_create_order'),
    path('list-results-analysis/', ListResultsAnalysis.as_view(), name='list_results_analysis'),

]    
