from django.shortcuts import render, HttpResponse
from rest_framework.generics import *
from rest_framework.views import APIView
from rest_framework.permissions import *
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .utils import Utlil
from .methodes import *
from .permissions import *

# End Points for SignUp User
class SignUpView(APIView):
    def post(self, request):
        user_information = request.data
        serializer = SignUpSerializer(data=user_information)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        cart = Cart.objects.create(user=user)
        user_data['id'] = user.pk
        code = generate_code()
        email_body = 'Hi '+user.username+' Use the code below to verify your email \n'+ str(code)
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify your email'}
        Utlil.send_email(data)
        code_verivecation = CodeVerification.objects.create(user=user, code=code)
        token = RefreshToken.for_user(user)
        tokens = {
            'refresh':str(token),
            'accsess':str(token.access_token)
        }
        return Response({'information_user':user_data,'tokens':tokens})

# End Points for Login User
class UserLoginApiView(APIView):
    # serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(email = request.data['username'])
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['image'] = request.build_absolute_uri(user.image.url)
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

# End Points for Logout User
class LogoutAPIView(APIView):
    serializer_class = UserLogoutSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

# End Points For Verified Account
class VerifyAccount(APIView):
    permission_classes = [HaveCodeVerifecation,]

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk') # Pass the pk to the request
        return super().get_permissions()
    
    def put(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(pk=pk)
        code_ver = CodeVerification.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)
                user.is_verified = True
                user.save()
                code_ver.delete()
                return Response({"message":'verification account hass been seccessfuly', 'user_id':user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})

# End Points For Get Code To Reset Password
class GetCodeResetPassword(APIView):

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk') # Pass the pk to the request
        return super().get_permissions()
    
    def post(self, request):
        email = request.data['email']
        try: 
            user = get_object_or_404(CustomUser, email=email)
            existing_code = CodeVerification.objects.filter(user=user).first()
            if existing_code:
                existing_code.delete()
            code_verivecation = generate_code()
            email_body = 'Hi '+user.username+' Use the code below to reassign your password \n'+ str(code_verivecation)
            data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify your email'}
            Utlil.send_email(data)
            code = CodeVerification.objects.create(user=user, code=code_verivecation)
            return Response({'message':'تم ارسال رمز التحقق',
                             'user_id' : user.id})
        except:
            raise serializers.ValidationError({'error':'pleace enter valid email'})
    
# End Points For Verified Account To Reset Password
class VerifyCodeToChangePassword(APIView):
    permission_classes = [HaveCodeVerifecation, ]

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk') # Pass the pk to the request
        return super().get_permissions()
    
    def post(self, request, pk):
        code = request.data['code']
        user = CustomUser.objects.get(id=pk)
        code_ver = CodeVerification.objects.filter(user=user.id).first()
        if code_ver:
            if str(code) == str(code_ver.code):
                if timezone.now() > code_ver.expires_at:
                    return Response({"message":"Verification code has expired"}, status=status.HTTP_400_BAD_REQUEST)
                code_ver.is_verified = True
                code_ver.save()
                return Response({"message":"تم التحقق من الرمز", 'user_id':code_ver.user.id},status=status.HTTP_200_OK)
            else:
                return Response({'message':'الرمز خاطئ, يرجى إعادة إدخال الرمز بشكل صحيح'})
        
# End Points For Reset Password
class ResetPasswordView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny, HaveCodeVerifecation, PermissionResetPassword]

    def get_permissions(self):
        self.request.pk = self.kwargs.get('pk')
        return super().get_permissions()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['pk']=self.kwargs.get('pk')
        return context

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     user = CustomUser.objects.get(id=pk)
    #     return self.get_serializer(user, many=False)
    
    # def put(self, request, pk):
    #     user = CustomUser.objects.get(pk=pk)
    #     try :
    #         code = CodeVerification.objects.filter(user=user).first()
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         code.delete()
    #         messages = {
    #             'message':'تم تغيير كلمة المرور بنجاح'
    #         }
    #         return Response(messages, status=status.HTTP_200_OK)
    #     except:
    #         return Response("ليس لديك الصلاحية بتغيير كلمة المرور")

# End Points For Update Image     
class UpdateImageUserView(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated,]

    def get_object(self):
        pk = self.kwargs.get('pk')
        return self.get_queryset().get(pk=pk)

# End Point For List Information User
class ListInformationUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = CustomUser.objects.all()
    serializer_class= CustomUserSerializer

class ListCreateBouquetsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Bouquet.objects.all()
    serializer_class = BouquetsSerializer

class ListCreateMedicalTestsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = MedicalTest.objects.all()
    serializer_class = MedicalTestSerializer


class GetBouquetsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    queryset = Bouquet.objects.all()
    serializer_class = BouquetsSerializer


class ListCreateItemCart(APIView):

    permission_classes = [IsAuthenticated,]
    def post(self, request):
        bouquet = Bouquet.objects.get(id=request.data['bouquet'])
        cart = Cart.objects.get(user=request.user)
        cart.bouquets.add(bouquet)

        return Response(status=status.HTTP_200_OK)
    
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        data = CartSerializer(cart, many=False)

        return Response(data.data, status=status.HTTP_302_FOUND)

class DeleteItemFromCart(APIView):

    permission_classes = [IsAuthenticated,]
    def post(self, request, item_id):
        cart = Cart.objects.get(user=request.user)
        bouquet = Bouquet.objects.get(id=item_id)
        cart.bouquets.remove(bouquet)

        return Response(status=status.HTTP_200_OK)

class ListCreateOrder(APIView):

    permission_classes = [IsAuthenticated,]
    def post(self, request):
        data = request.data
        cart = Cart.objects.get(user=request.user)
        serializer = OrderSerializer(data=data, many=False, context={'request':request, 'total_price':cart.total_price})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cart.bouquets.clear()
        # cart.save()
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = user.order_set.all()
        serializer = OrderSerializer2(orders, many=True)
        return Response(serializer.data ,status=status.HTTP_302_FOUND)
    
class ListResultsAnalysis(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        results_analysis = ResultsAnalysis.objects.get(user=user)
        results = ResultsAnalysisSerializer(results_analysis)
        medical_test = Analysis.objects.filter(resultsanalysis=results_analysis.id)
        data = AnalysisSerializer(medical_test, many=True)
        result_data = {
            'analysis': results.data,
            'medical_test' : data.data
        }
        return Response(result_data, status=status.HTTP_302_FOUND)