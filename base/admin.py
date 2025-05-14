from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
class AdminCustomUser(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id', 'email','username', 'is_verified']    
    ordering = ['-id']

    fieldsets = (
        (None, 
                {'fields':('email', 'password',)}
            ),
            ('User Information',
                {'fields':('username', 'first_name', 'last_name','image')}
            ),
            ('Permissions', 
                {'fields':('is_verified', 'is_staff', 'is_superuser', 'is_active', 'groups','user_permissions')}
            ),
            ('Registration', 
                {'fields':('date_joined', 'last_login',)}
        )
    )

    add_fieldsets = (
        (None, {'classes':('wide',),
            'fields':(
                'email' , 'username', 'password1', 'confpassword',
            ),}
            ),
    )
admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(CodeVerification)



class AdminMedicalTest(admin.ModelAdmin):
    list_display = ['test_name']
    search_fields = ['test_name']
    list_per_page = 25

admin.site.register(MedicalTest, AdminMedicalTest)

class AdminBouquet(admin.ModelAdmin):
    list_display = ['bouquet_name', 'price', 'descreption']
    search_fields = ['bouquet_name']
    list_per_page = 25

admin.site.register(Bouquet, AdminBouquet)

class AdminCart(admin.ModelAdmin):
    list_display = ['user']
    list_per_page = 25

admin.site.register(Cart, AdminCart)

class AdminOrder(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'gender', 'phonenumber', 'total_price']
    search_fields = ['phonenumber', 'full_name']
    list_per_page = 25

admin.site.register(Order, AdminOrder)

class AdminAnalysis(admin.ModelAdmin):
    list_display = ['user', 'medical_test', 'result', 'natural_value', 'evaluation', 'date']
    search_fields = ['medical_test']
    list_per_page = 25

    fieldsets = (
        ('Choice Result Analysis', 
            {'fields':('resultsanalysis',)}
        ),
        ('Please Add detailes Analysis',
            {'fields':('medical_test', 'result', 'natural_value', 'evaluation')}
        ),
    )

    def user(self, obj):
        return obj.resultsanalysis.user.username
    
admin.site.register(Analysis, AdminAnalysis)

class AdminResultsAnalysis(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['search_keyword']
    list_per_page = 25
    def search_keyword(self, obj):
        return obj.user.username
admin.site.register(ResultsAnalysis, AdminResultsAnalysis)