from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from django.contrib.auth import  authenticate
from django.contrib.auth.password_validation import validate_password
from .methodes import *

# Handel Seriailzer For SignUp
class SignUpSerializer(serializers.ModelSerializer):
    confpassword = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confpassword']
        extra_kwargs = {
            'password':{'write_only':True,}
        }
    def validate(self, validated_data):
        validate_password(validated_data['password'])
        validate_password(validated_data['confpassword'])
        if validated_data['password'] != validated_data['confpassword'] :
            raise serializers.ValidationError("password and confpassword didn't match")
        return validated_data

    def create(self, validated_data):
        validated_data.pop('confpassword', None)
        return CustomUser.objects.create_user(**validated_data)
    

# Handel Seriailzer For Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError("Incorrect Credentials")
            if not user.is_active:
                raise serializers.ValidationError({'message_error':'this account is not active'})
            if not user.is_verified:
                raise serializers.ValidationError({'message_error':'this account is not verified'})
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

        data['user'] = user
        return data
    
# Handel Seriailzer For Logout
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# Handel Seriailzer For Reset Password
class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confpassword = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['confpassword'] != attrs['password']:
            raise serializers.ValidationError({'message_error':'Passwords do not match.'})
        validate_password(attrs['password'])
        return attrs

    def update(self, instance, validated_data):
        pk = self.context.get('pk')
        instance = CustomUser.objects.get(pk=pk)
        instance.set_password(validated_data['password'])
        instance.save()
        code = CodeVerification.objects.filter(user=instance).first()
        code.delete()
        return instance
    
# Handel Seriailzer For Update Image
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['image']
    
# Handel Seriailzer For List Information User
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'image']

# Handel Seriailzer For List Information Medical Tests
class MedicalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalTest
        fields = ['test_name']

# Handel Seriailzer For List Information Bouquets
class BouquetsSerializer(serializers.ModelSerializer):
    medical_test = MedicalTestSerializer(read_only=True, many=True)
    class Meta:
        model = Bouquet
        fields = ['bouquet_name', 'price', 'descreption', 'image', 'medical_test']

class CartBouquetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bouquet
        fields = ['id', 'bouquet_name', 'price', 'image']

class CartSerializer(serializers.ModelSerializer):
    bouquets = CartBouquetSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ['id', 'bouquets', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True,}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        total_price = self.context.get('total_price')
        bouquets = validated_data.pop('bouquets')
        validated_data['user'] = request.user
        validated_data['total_price'] = total_price
        order = Order.objects.create(**validated_data)
        for bouquet in bouquets:
            order.bouquets.add(bouquet)
        return order
    

class BouquetsSerializer2(serializers.ModelSerializer):
    # medical_test = MedicalTestSerializer(read_only=True, many=True)
    class Meta:
        model = Bouquet
        fields = ['bouquet_name', 'price', 'image']

class OrderSerializer2(serializers.ModelSerializer):
    bouquets = BouquetsSerializer2(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'user':{'read_only':True,}
        }

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ['medical_test', 'result', 'natural_value', 'evaluation', 'date']

class ResultsAnalysisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResultsAnalysis
        fields = ['user']