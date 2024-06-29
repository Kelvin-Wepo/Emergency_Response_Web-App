from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
import africastalking

YOUR_DOMAIN = 'http://localhost:8000'
stripe.api_key = 'sk_test_51OyFFj05WR71AuXapnRyNOu6pPi2WZpP1JmoDG6xDpHjkQ0HljzRdq0Zd5F176eLunS88O49oUMsekVynw10UyLx00WGP4ZRTr'
# APPLICATION VIEWS.
# home function
africastalking.api_key = settings.AFRICASTALKING_API_KEY
def home(request):
    comments= Feedback.objects.all()
    return render(request, 'public/index.html', {'comments':comments})

# def owners_home(request):
#     comments= Feedback.objects.all()
#     return render(request, 'owners/owner_home.html', {'comments':comments})


def services(request):
    ambulances= Ambulance.objects.all()
    return render(request, 'public/services.html', {'ambulances': ambulances})


# Register function

def public_register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            profile, created = Profile.objects.get_or_create(user=user)

            phone_number = form.cleaned_data.get('contact_number')
               
            if phone_number is not None:  # Check if phone_number is not None
                profile.contact_number = phone_number
                profile.save()
        # Send SMS only if phone_number is not None
                africastalking_username = 'kwepo'
                africastalking_api_key = africastalking.api_key
        
                africastalking.initialize(africastalking_username, africastalking_api_key)
                sms = africastalking.SMS
                message = "Welcome to ERS Services your Emergency Services Partner."
                response = sms.send(message, [profile.contact_number])
                print("SMS response:", response)
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'logins/register.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request, 'logins/admin.html')


#user login
def user_login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_hospital:
                login(request, user)
                return redirect('owner')
            elif user is not None and user.is_public:
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('admin')
            else:
                msg= 'invalid credentials'
        else:
            messages.info = 'error validating form'
    return render(request, 'logins/login.html', {'form': form, 'msg': msg})

#admin
def admin(request):
    return render(request,'admin.html')


# logout function


def user_logout(request):
    logout(request)
    return render(request, 'public/index.html')


def profile(request):
    users = User.objects.all()
    current_user = request.user
    # profile = get_object_or_404(Profile,user=request.user)

    return render(request, 'profile/profile.html', {"users": users})

def hospital_profile(request):
    users = User.objects.all()
    current_user = request.user
    # profile = get_object_or_404(Profile,user=request.user)

    return render(request, 'profile/owner_profile.html', {"users": users})


def update_profile(request):
    # profiles= Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userprofileform = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if userprofileform.is_valid():
            userprofileform.save()
            return redirect(to='profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile/update_profile.html', {'form': form})

def hospital_update_profile(request):
    # profiles= Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userprofileform = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if userprofileform.is_valid():
            userprofileform.save()
            return redirect(to='hospital_profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile/hospital_update_profile.html', {'form': form})

# owners html
def hospital(request):
    ambulance = Ambulance.objects.all()
    return render(request, 'hospitals/hospital_home.html', {'ambulance': ambulance})


def add_ambulance(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        ambulance_name = request.POST.get('ambulance_name')
        current_location = request.POST.get('current_location')
        availability = request.POST.get('availability') == 'True'  # Converts 'True'/'False' string to boolean
        response_rate = request.POST.get('response_rate')
        driver_name = request.POST.get('driver_name')
        hospital_name = request.POST.get('hospital_name')

        ambulance = Ambulance(
            image=image,
            ambulance_name=ambulance_name,
            current_location=current_location,
            availability=availability,
            response_rate=response_rate,
            driver_name=driver_name,
            hospital_name=hospital_name
        )

        ambulance.save_ambulance()

        return redirect('hospital')  # Replace 'owner' with the actual name of the redirect URL

    return render(request, 'hospitals/add.html')


def single_ambulance(request, ambulance_id):
    single_ambulance = get_object_or_404(Ambulance, id=ambulance_id)
    current_user = request.user
    user = get_object_or_404(User, username=current_user.username)
    bookings = Booking.get_bookings(ambulance_id)

    return render(request, 'owners/single_ambulance.html', {'single_ambulance': single_ambulance, 'bookings': bookings})

def delete_ambulance(request, ambulance_id):
    ambulance = Ambulance.objects.get(id=ambulance_id)
    ambulance.delete()
    return redirect('hospital')


def update_ambulance(request, ambulance_id):
    update = Ambulance.objects.get(id=ambulance_id)
    if request.method == 'POST':
        ambulanceform = AmbulanceUpdateForm(
            request.POST, request.FILES, instance=update)
        if ambulanceform.is_valid():
            ambulanceform.save()
            return redirect('single', ambulance_id)
    else:
        form2 = AmbulanceUpdateForm(instance=update)
    return render(request, 'hospitals/update_ambulance.html', {'form2': form2})


def user_single_ambulance(request, ambulance_id):
    single_ambulance = Ambulance.objects.get(id=ambulance_id)
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    ambulance = Ambulance.objects.get(id=ambulance_id)
    form2 = CommentForm()
    
    if request.method == 'POST':
        form2 = CommentForm(request.POST)
        if form2.is_valid():

            comment = form2.save(commit=False)

            comment.user_id = user
            comment.ambulance_id = ambulance

            comment.save()

            return redirect('single_ambulance',ambulance_id)
        else:
            form2 = CommentForm()

    return render(request, 'public/single_ambulance.html', {'single_ambulance': single_ambulance, 'form2': form2, 'ambulance': ambulance})

def hospital_single_ambulance(request, ambulance_id):
    single_ambulance = Ambulance.objects.get(id=ambulance_id)
    current_user = request.user
    user = User.objects.get(username=current_user.username)

    return render(request, 'public/single_ambulance.html', {'owner_single_ambulance': single_ambulance,})


def comment(request, ambulance_id):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    ambulance = Ambulance.objects.get(id=ambulance_id)
    form2 = CommentForm()
    
    if request.method == 'POST':
        form2 = CommentForm(request.POST)
        if form2.is_valid():

            comment = form2.save(commit=False)

            comment.user_id = user
            comment.ambulance_id = ambulance

            comment.save()

            return redirect('single_ambulance',ambulance_id)
        else:
            form2 = CommentForm()
    return render(request, 'public/single_ambulance.html', {'form2': form2, 'ambulance': ambulance})


#booking form
def booking(request, ambulance_id):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    ambulance = Ambulance.objects.get(id=ambulance_id)
    form3 = BookingForm()
    
    if request.method == 'POST':
        form3 = BookingForm(request.POST)
        if form3.is_valid():

            booking = form3.save(commit=False)

            booking.user_id = user
            booking.ambulance_id = ambulance

            booking.save()

            return redirect('single_booking',booking_id)
        else:
            form3 = BookingForm()

    return render(request, 'public/order.html', {'form3': form3, 'ambulance': ambulance})



def create_checkout_session(request):
    machinery_queryset = Machinery.objects.all()

    for machinery in machinery_queryset:

        if request.method == 'POST':
                try:
                    checkout_session = stripe.checkout.Session.create(
                        line_items=[
                            {
                                    
                                'price_data': {
                                    'currency': 'kes',  
                                    'unit_amount' : machinery.hire_price,
                                    'product_data': {
                                        'name':machinery.machinery_name,
                                        # 'images':machinery.image,
                                        
                                    }

                                },
                                'quantity': 1,
                            },
                        ],
                        mode='payment',
                        success_url=YOUR_DOMAIN + '/success/',
                        cancel_url=YOUR_DOMAIN + '/cancel/',
                    )
                    print('--------------')
                    return redirect(checkout_session.url)

                except Exception as e:
                    print('error occured')
                    print(str(e))

                context = {
                    'machinery': machinery
                }

    return render(request, 'public/checkout.html')

def success(request):
    return render (request, 'public/success.html')

def cancel(request):
    return render (request, 'public/cancel.html')

