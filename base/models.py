from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from .methodes import *

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    # phonenumber = PhoneNumberField(region='SY',unique=True)
    username = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/users', null=True,default='images/account.jpg')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',) 


    def __str__(self):
        return self.username
    
class CodeVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return f'{self.user.username} code:{self.code}'
class MedicalTest(models.Model):
    test_name = models.CharField(max_length=50)

    def __str__(self):
        return self.test_name


class Bouquet(models.Model):
    bouquet_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    descreption = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/Bouquets', null=True, blank=True)
    medical_test = models.ManyToManyField(MedicalTest)

    def __str__(self):
        return self.bouquet_name

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bouquets = models.ManyToManyField(Bouquet)

    @property
    def total_price(self):
        total = 0
        for bouquet in self.bouquets.all():
            total += bouquet.price
        return total

    def __str__(self):
        return f'cart for user {self.user.username}'

Gender = (
    ('ذكر', 'ذكر'),
    ('أنثى', 'أنثى')
)
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    gender = models.CharField(choices=Gender, max_length=20)
    birthdate = models.DateField()
    phonenumber = PhoneNumberField(region='SY')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount = models.BooleanField(default=False, max_length=25, null=True, blank=True)
    type_discount = models.CharField(max_length=100, default='no discount', null=True, blank=True)
    is_accepted = models.BooleanField(default=False, max_length=25, null=True, blank=True)
    file_discount = models.FileField(upload_to='images/Discount', null=True, blank=True)
    bouquets = models.ManyToManyField(Bouquet)

    def __str__(self):
        return f'{self.id}'
    
    def save(self, *args, **kwargs):
        # super().save(*args, **kwargs)
        if self.discount == True and self.is_accepted == True:
            if self.type_discount == 'ذوي الإعاقة':
                discount_amount = (self.total_price * 40)/100
                self.total_price = self.total_price - discount_amount

            elif self.type_discount == 'أيتام':
                discount_amount = (self.total_price * 20)/100
                self.total_price = self.total_price - discount_amount
        
        super().save(*args, **kwargs)


class ResultsAnalysis(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    medical_test = models.ManyToManyField(MedicalTest, through='analysis')

    def __str__(self):
        return f'result analysis for patient {self.user.username}'
    
class Analysis(models.Model):
    resultsanalysis = models.ForeignKey(ResultsAnalysis, on_delete=models.CASCADE)
    medical_test = models.ForeignKey(MedicalTest, on_delete=models.CASCADE)
    result = models.DecimalField(max_digits=10, decimal_places=2)
    natural_value = models.CharField(max_length=100)
    evaluation = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.medical_test.test_name} for patient {self.resultsanalysis.user.username}'