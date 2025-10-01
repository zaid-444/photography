from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import UserProfile,PhotographerProfile,Booking
from .forms import PhotographerProfileForm,BookingForm
from django.contrib.auth.decorators import login_required
from .models import Notification


# Create your views here.

def home(request):
    return render(request,'booking/home.html')

def contact_view(request):
    return render(request,'booking/contact.html')

def signup_view(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        role=request.POST['role']
        if password != confirm_password:
            messages.error(request,'Passwords not match')
            return redirect('signup')       
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already taken')
            return redirect('signup')        
        user=User.objects.create_user(username=username,email=email,password=password)
        UserProfile.objects.create(user=user,role=role)
        messages.success(request,"Account created successfully")
        return redirect('login')
    return render(request,'booking/signup.html')


def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid User or Password')
            return redirect('login')
    return render(request,'booking/login.html')


@login_required
def create_photographer_profile(request):
    user_profile = request.user.userprofile
    if user_profile.role != 'photographer' or not user_profile.is_approved:
        messages.warning(request, "You are not allowed to access this page.")
        return redirect('dashboard')
    try:
        profile = request.user.photographerprofile
        messages.info(request, "Profile already exists.")
        return redirect('dashboard')
    except PhotographerProfile.DoesNotExist:
        pass
    if request.method == 'POST':
        form = PhotographerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Photographer profile created successfully!")
            return redirect('dashboard')
    else:
        form = PhotographerProfileForm()
    return render(request, 'booking/create_photographer_profile.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def photographer_list(request):
    user_profile=getattr(request.user,'userprofile',None)
    if not user_profile or user_profile.role != 'client':
        messages.error(request,'Only clients can view photographers')
        return redirect('home')
    photographers = PhotographerProfile.objects.filter(user__userprofile__is_approved=True)
    return render(request, 'booking/photographer_list.html', {'photographers': photographers})


@login_required
def dashboard(request):
    user_profile = request.user.userprofile
    context = {
        'role': user_profile.role,
        'is_approved': user_profile.is_approved,
    }
    if user_profile.role == 'photographer' and user_profile.is_approved:
        try:
            photographer_profile = PhotographerProfile.objects.get(user=request.user)
            bookings = Booking.objects.filter(photographer=photographer_profile)
            context['profile'] = photographer_profile
            context['bookings'] = bookings
        except PhotographerProfile.DoesNotExist:
            context['profile'] = None
            context['bookings'] = None
    elif user_profile.role == 'client':
        my_bookings = Booking.objects.filter(customer=request.user)
        context['my_bookings'] = my_bookings
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        context['notifications'] = notifications
    return render(request, 'booking/dashboard.html', context)


@login_required
def book_photographer(request, photographer_id):
    photographer = get_object_or_404(PhotographerProfile, id=photographer_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.photographer = photographer
            booking.save()
            messages.success(request, "Your booking request has been sent!")
            return redirect('dashboard')
    else:
        form = BookingForm()
    return render(request, 'booking/book_photographer.html', {'form': form, 'photographer': photographer})


@login_required
def update_booking_status(request, booking_id, status):
    photographer_profile = get_object_or_404(PhotographerProfile, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, photographer=photographer_profile)
    if status == "rejected":
        Notification.objects.create(
            user=booking.customer,
            message=f"Your booking with {photographer_profile.full_name} was rejected."
        )
        booking.delete()
        messages.info(request, "Booking request rejected and deleted.")
    else:
        booking.status = status
        booking.save()
        Notification.objects.create(
            user=booking.customer,
            message=f"Your booking with {photographer_profile.full_name} was {status}."
        )
        messages.success(request, f"Booking {status} successfully!")
    return redirect('dashboard')