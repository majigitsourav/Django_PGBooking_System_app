from django.db import models
from django.utils.crypto import*



# Create your models here.
from django.db import models

class PG(models.Model):
    pgname = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    pname = models.CharField(max_length=100)# pg name
    email = models.EmailField()
    phone_no = models.CharField(max_length=10)
    pg_rg_no = models.CharField(max_length=10,unique=True)  #p owner uniq id
    pro_address = models.CharField(max_length=1000) #land mark
    description = models.TextField()
    rent = models.CharField(max_length=50)
    property_image1 = models.ImageField(upload_to='property_images/',blank=True, null=True)
    property_image2 = models.ImageField(upload_to='property_images/',blank=True, null=True)
    property_image3 = models.ImageField(upload_to='property_images/',blank=True, null=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    no_of_beds = models.CharField(max_length=1)
    amenities = models.CharField(max_length=2000)

    def __str__(self):
        return self.pgname
    class Meta:
        db_table="PG"

class PGLister(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    unique_id = models.CharField(primary_key = True,max_length = 50)
    full_name = models.CharField(max_length=100)
    emg_phone = models.CharField(max_length=20)
    id_proof = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    security_answer = models.CharField(max_length=200)
    def save(self, *args, **kwargs):
        if not self.unique_id:
            # Generate a random string for uniqueness
            random_string = get_random_string(length=6)
            # Combine full_name and random_string to create unique_id
            self.unique_id = f"{self.full_name}_{random_string}"
        super().save(*args, **kwargs)
    
    
    
    class Meta:
        db_table = 'PGLister'



class Customer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    unique_id = models.CharField(primary_key = True,max_length = 50)
    name=models.CharField(max_length=100)
    father_name= models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone_no = models.IntegerField(max_length=10)
    dob = models.DateField()
    emg_no = models.IntegerField(max_length=10)
    proof_ID = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    gender = models.CharField(max_length=30,choices=GENDER_CHOICES, default='male')
    security_answer = models.CharField(max_length=200)
    
    def save(self, *args, **kwargs):
        if not self.unique_id:
            # Generate a random string for uniqueness
            random_string = get_random_string(length=6)
            # Combine full_name and random_string to create unique_id
            self.unique_id = f"{self.name}_{random_string}"
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'Customer'

class BookDetails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
    total_amount = models.IntegerField(max_length=10)
    pgid = models.IntegerField()
    pgname = models.CharField(max_length=100)
    unic_name=models.CharField(max_length=100)
    order_id=models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    payment_status=models.CharField(max_length=100,blank=True,null=True)
    owner_uniq_id=models.CharField(max_length=100)
    class Meta:
        db_table = 'BookDetails'