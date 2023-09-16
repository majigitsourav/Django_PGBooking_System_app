from django.shortcuts import render,redirect,get_object_or_404
import razorpay
from django.http import HttpResponse
# Create your views here.
from .models import *
from django.db.models import Q
from django.conf import settings
from django.contrib import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *



# from.forms import*


def test(request):
    return render(request,'mainindex.html')

def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def service(request):
    return render(request,'service.html')

def user_login(request):
    return render(request,'login_user.html')

def pgowner_login(request):
    return render(request,'login_pgowner.html')

def user_reg(request):
    return render(request,'user_reg.html')

def pgowner_reg(request):
    return render(request,'pgowner_reg.html')


def change_password(request):
    return render(request,'change_password.html')
    
def passwordchange(request,user_type):
    context = {}
    
    # Get the user type (PGOwner or User)
    user_type = None
    unique_id = None
    
    if 'user_unique_id' in request.session:
        user_type = 'User'
        unique_id = request.session['user_unique_id']
    elif 'owner_unique_id' in request.session:
        user_type = 'PGOwner'
        unique_id = request.session['owner_unique_id']

    if user_type and unique_id:
        if request.method == "POST":
            current = request.POST["cpwd"]
            new_pass = request.POST["npwd"]
            
            try:
                if user_type == 'User':
                    user = Customer.objects.get(unique_id=unique_id)
                elif user_type == 'PGOwner':
                    user = PGLister.objects.get(unique_id=unique_id)
                    
                if user.password == current:
                    user.password = new_pass
                    
                    user.save()
                    
                    context["maz"] = "Password Changed Successfully!!!"
                    context["col"] = "alert-success"
                else:
                    context["maz"] = "Incorrect Current Password"
                    context["col"] = "alert-danger"
            except (PGLister.DoesNotExist, Customer.DoesNotExist):
                context["maz"] = "User not found"
                context["col"] = "alert-danger"
    else:
        context["maz"] = "Session data not found."
        context["col"] = "alert-danger"

    return render(request, 'change_password.html', context)

    

    
       

def popertylist(request):
    return render(request,'propertylist.html')


def listing(request):
    # Fetch PG listings from the database
    pg_listings = PG.objects.all()
    booking = BookDetails.objects.all()

    # Get a list of PG IDs that have been booked
    booked_pg_ids = [booking_item.pgid for booking_item in booking]

    # Filter the pg_listings queryset to include only PGs where id is not in booked_pg_ids
    available_pg_listings = pg_listings.exclude(id__in=booked_pg_ids)
    print("booked_pg_ids:", booked_pg_ids)
    print("available_pg_listings:", available_pg_listings)


    context = {
        'pg_listings': available_pg_listings,
    }

    return render(request, 'listing.html', context)


def create_pg(request):
    if request.method == 'POST':
        # If the request method is POST, it means the form was submitted
        # Create a new instance of the addpg model and populate it with form data
        new_pg = PG(
            pgname=request.POST['property_name'],
            gender=request.POST['gender'],
            pname=request.POST['contact_name'],
            email=request.POST['email'],
            phone_no=request.POST['mobile'],
            pg_rg_no=request.POST['pgregno'],
            pro_address=request.POST['propertyaddress'],
            description=request.POST['description'],
            rent=request.POST['rent'],
            property_image1=request.FILES['property_image1'],
            property_image2=request.FILES['property_image2'],
            property_image3=request.FILES['property_image3'],
            state=request.POST['state'],
            city=request.POST['city'],
            location=request.POST['locality'],
            no_of_beds=request.POST['noofbeds'],
            amenities=request.POST['amenities_text']
        )
        if 'property_image1' in request.FILES:
            new_pg.property_image1 = request.FILES['property_image1']
        if 'property_image2' in request.FILES:
            new_pg.property_image2 = request.FILES['property_image2']
        if 'property_image3' in request.FILES:
            new_pg.property_image3 = request.FILES['property_image3']


        # Save the new PG instance to the database
        new_pg.save()
        pname_to_match = new_pg.pname.lower()
        
        # Fetch PGs with the same pname (case-insensitive) as the one just added
        c = PG.objects.filter(pname__iexact=pname_to_match)
        # messages.success(request, 'Property details added successfully.')
        return render(request, 'showpropertylist.html',{'a':c})

    return render(request, 'propertylist.html')



    
def pg_search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')

        # Split the user's input into keywords
        keywords = search_query.split()

        # Initialize an empty Q object to build the query
        q = Q()

        for keyword in keywords:
            # Add OR conditions for each keyword and field
            q |= Q(city__icontains=keyword) | Q(state__icontains=keyword) | Q(location__icontains=keyword)

        # Use the combined Q object to filter PG accommodations
        pg_results = PG.objects.filter(q)
        booked_pgid_list = BookDetails.objects.values_list('pgid', flat=True)
    
        # Exclude the booked PGIDs from the first queryset (pg_listings)
        available_pg_listings =  pg_results.exclude(id__in=booked_pgid_list)

        return render(request, 'listing.html', {'pg_listings': available_pg_listings, 'search_query': search_query})

def show_pg(request, pg_id):
    # Retrieve the PgModel instance using the pg_id parameter
 if 'user_unique_id' in request.session:
      pg = get_object_or_404(PG, id=pg_id)
    # Pass the pg object to the template for rendering
      return render(request, 'showpg.html', {'pg': pg})
 return redirect('ulogin')
def pg_owner_registration(request):
    if request.method == 'POST':
        # Extract form data
        full_name = request.POST.get('full_name')
        emg_phone = request.POST.get('emg_phone')
        id_proof = request.POST.get('id_proof')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('txtEmpPhone')
        security_answer = request.POST.get('security_answer')
        
        # Check if any required field is empty
        if not (full_name and emg_phone and id_proof and password and gender and email and phone and security_answer):
            messages.warning(request, "Please fill out all required fields.")
        else:
            try:
                pg_owner = PGLister(
                    full_name=full_name,
                    emg_phone=emg_phone,
                    id_proof=id_proof,
                    password=password,
                    gender=gender,
                    email=email,
                    phone=phone,
                    security_answer=security_answer,
                )
                pg_owner.save()
                messages.success(request, f"Congratulations {full_name}! You have successfully registered. Your unique_id is: {pg_owner.unique_id}" )
            except Exception as e:
                messages.warning(request, f"Failed to register: {e}")
    
    return render(request, 'pgowner_reg.html')

# def pg_owner_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         users = PGLister.objects.filter(email=email)
        
#         if users.exists():
#             for user in users:
#                 if user.password == password:
#                     # Authentication successful
#                     messages.success(request, 'Login successful!')
#                     return render(request, 'propertylist.html')
#             # Password didn't match for any user
#             messages.error(request, 'Invalid email or password.')
#         else:
#             # No user with the provided email
#             messages.error(request, 'Invalid credentials. Please try again.')

#     return render(request, 'login_pgowner.html')

def pg_owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            owner =  PGLister.objects.get(email=email,password=password)
            request.session['owner_unique_id'] = owner.unique_id
            messages.success(request, 'Login successful!')
            return render(request, 'propertylist.html')
        except PGLister.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
        
            # No user with the provided email
    return render(request,'login_pgowner.html')

def plogout(request):
    logout(request)
    return render(request,'index.html')


# for user

def userreg(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('a1')
        father_name = request.POST.get('a2')
        email = request.POST.get('a3')
        phone_no = request.POST.get('a4')
        dob = request.POST.get('a5')
        emg_no = request.POST.get('a6')
        proof_ID = request.POST.get('a7')
        password = request.POST.get('a8')
        gender = request.POST.get('a9')
        security_answer = request.POST.get('a10')
        if not (name and father_name and email and phone_no and dob and emg_no and proof_ID and password and gender and security_answer):
            messages.warning(request, "Please fill out all required fields.")
        else:
            try:
                u = Customer(
                name = name,
                father_name = father_name,
                email = email,
                phone_no = phone_no,
                dob = dob,
                emg_no = emg_no,
                proof_ID = proof_ID,
                password = password,
                gender = gender,
                security_answer = security_answer,
            )
                u.save()
                messages.success(request, f"Congratulations {name}! You have successfully registered. Your unique_id is: {u.unique_id}" )
            except Exception as e:
                messages.warning(request, f"Failed to register: {e}")
    return render(request,"userregistration.html")


def ulogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            users = Customer.objects.get(email=email,password=password,)
            request.session['user_unique_id'] = users.unique_id
            messages.success(request, 'Login successful!')
            return redirect('home')
        except Customer.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
        
            # No user with the provided email
    return render(request,'user_login.html')
def ulogout(request):
    logout(request)
    return render(request,'index.html')




def book_details(request):
    # Get the parameters from the URL
    total_pay = request.GET.get('totalPay')
    num_months = request.GET.get('numMonths')
    pg_id = request.GET.get('pgId')

    pg = get_object_or_404(PG, id=pg_id)
    #name=get_object_or_404(PG, pname=)
    if request.method =="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        from_date=request.POST.get("check-in")
        to_date=request.POST.get("check-out")
        total_amount=int(request.POST.get("price")) *100

        print(total_amount)
        # price_in_rupees = float(request.POST.get("price"))  # Assuming price is in rupees
        # total_amount = max(int(price_in_rupees * 100), 100)  # Ensure minimum amount is Rs. 1 (100 paise)
        pgid=request.POST.get("pgid")
        pgname=request.POST.get("pgname")
        unic_name=request.POST.get("unic_name")
        owner_uniq_id=request.POST.get("owner_unic_id")

        client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
        payment_response = client.order.create({'amount':total_amount,'currency':'INR','payment_capture':1})
       
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status =='created':
              booking = BookDetails(
                name=name,
                email=email,
                phone=phone,
                from_date=from_date,
                to_date=to_date,
                total_amount=total_amount/100,
                pgid=pgid,
                pgname=pgname, 
                unic_name=unic_name,
                order_id=order_id,
                payment_status = order_status,
                owner_uniq_id =owner_uniq_id
            )
        booking.save()

        return render(request, "book_details.html",{'payment': payment_response})
   


    # You can perform any additional processing here
    
    return render(request, 'book_details.html', {
        'total_pay': total_pay,
        'num_months': num_months,
        'pg': pg,
    })
# for user
def get_username(unique_id):
    try:
        username = Customer.objects.get(unique_id=unique_id)
        return username
    except Customer.DoesNotExist:
        return "Unknown"
    
#for pgowner
def get_pgowner(unique_id):
    try:
        ownername = PGLister.objects.get(unique_id=unique_id)
        return ownername
    except PGLister.DoesNotExist:
        return "Unknown"




# def payment(request):
#     if request.method =="POST":
#         name=request.POST.get("name")
#         email=request.POST.get("email")
#         phone=request.POST.get("phone")
#         from_date=request.POST.get("check-in")
#         to_date=request.POST.get("check-out")
#         total_amount=int(request.POST.get("price")) *100
#         print(total_amount)
#         # price_in_rupees = float(request.POST.get("price"))  # Assuming price is in rupees
#         # total_amount = max(int(price_in_rupees * 100), 100)  # Ensure minimum amount is Rs. 1 (100 paise)
#         pgid=request.POST.get("pgid")
#         pgname=request.POST.get("pgname")
#         unic_name=request.POST.get("unic_name")
#         client = razorpay.Client(auth=(settings.KEY,settings.SECRET))
#         payment = client.order.create({'amount':total_amount,'currency':'INR','payment_capture':1})
       
#         print(payment)

#         booking = BookDetails(name=name,email=email,phone=phone,from_date=from_date,to_date=to_date,total_amount=total_amount,pgid=pgid,pgname=pgname, unic_name=unic_name,order_id=payment['id'])
#         booking.save()

#         return render(request, "book_details.html",{'payment': payment})
#     return render(request,"book_details.html")

def payment_status(request):
    if request.method == 'POST':
        a = request.POST
       
    return render(request,"book_success.html")



def bookinglist(request):
    context = {}
    unique_id=None
    if 'user_unique_id' in request.session:
        unique_id = request.session['user_unique_id']
    book = BookDetails.objects.filter(unic_name=unique_id)
    return render(request,'bookinglist.html',{'book':book})


#forgot Password
def forgot_password_customer(request):
    user = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        security_answer = request.POST.get('security_answer')
        
        try:
            user = Customer.objects.get(email=email, security_answer=security_answer)
        except Customer.DoesNotExist:
            pass
        
        if user:
            request.session['reset_user_id'] = user.unique_id
            return redirect('reset_password_customer')
        else:
            messages.error(request, 'Invalid email or security answer.')

    return render(request, 'forgot_password_customer.html', {'user': user})


def forgot_password_pg_lister(request):
    user = None
    
    if request.method == 'POST':
        email = request.POST.get('email')
        security_answer = request.POST.get('security_answer')
        
        try:
            user = PGLister.objects.get(email=email, security_answer=security_answer)
        except PGLister.DoesNotExist:
            pass
        
        if user:
            request.session['reset_user_id'] = user.unique_id
            return redirect('reset_password_pg_lister')
        else:
            messages.error(request, 'Invalid email or security answer.')

    return render(request, 'forgot_password_pg_lister.html', {'user': user})


def reset_password_customer(request):
    unique_id = request.session.get('reset_user_id')
    
    if not unique_id:
        return redirect('forgot_password_customer')
    
    user = None
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        
        try:
            user = Customer.objects.get(unique_id=unique_id)
        except Customer.DoesNotExist:
            pass

        if user:
            user.password = new_password
            user.save()
            return redirect('password_reset_confirmation')  # Change this to your login URL
        else:
            messages.error(request, 'Invalid user for password reset.')

    return render(request, 'reset_password_customer.html', {'user': user})


def reset_password_pg_lister(request):
    unique_id = request.session.get('reset_user_id')
    
    if not unique_id:
        return redirect('forgot_password_pg_lister')
    
    user = None
    
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        
        try:
            user = PGLister.objects.get(unique_id=unique_id)
        except PGLister.DoesNotExist:
            pass

        if user:
            user.password = new_password
            user.save()
            return redirect('password_reset_confirmation')  # Change this to your login URL
        else:
            messages.error(request, 'Invalid user for password reset.')

    return render(request, 'reset_password_pg_lister.html', {'user': user})



def password_reset_confirmation(request):
    return render(request, 'password_reset_confirmation.html')



def profile(request):
    return render(request, 'profile.html')

def pgowner_profile(request):
    return render(request, 'pgowner_profile.html')


def pgowner_booking(request):
    unique_id = request.session['owner_unique_id']
    new_pg=get_object_or_404(PGLister, unique_id=unique_id)

    pname_to_match = new_pg.full_name.lower()
        
        # Fetch PGs with the same pname (case-insensitive) as the one just added
    #c = PG.objects.filter(pname__iexact=pname_to_match)
        
    # Fetch PGs with the same pname (case-insensitive) as the one just added
    c = BookDetails.objects.filter(owner_uniq_id__iexact=pname_to_match)
    
    return  render(request, 'pg_booked.html',{'a':c})


