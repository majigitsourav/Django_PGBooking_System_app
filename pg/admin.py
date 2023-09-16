from django.contrib import admin
from . models import *
# Register your models here.
@admin.register(PG)
class PGModelAdmin(admin.ModelAdmin):
    list_display=[ 'pname' ,'email' ,'phone_no','pg_rg_no','pro_address','description','rent','property_image1','property_image2','property_image3','state','city','location','no_of_beds','amenities']


@admin.register(PGLister)
class PGOwnerModelAdmin(admin.ModelAdmin):
    list_display = ['unique_id','full_name', 'emg_phone', 'email', 'id_proof', 'gender', 'password', 'phone', 'security_answer']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['name','father_name','email','phone_no','dob','emg_no','proof_ID','password','gender']

@admin.register(BookDetails)
class BookDetailsModelAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','from_date','to_date','total_amount','pgid','pgname','paid']

