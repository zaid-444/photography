from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from .models import UserProfile,PhotographerProfile,Booking
from .forms import PhotographerProfileForm,BookingForm
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.db.models import Q
import json

# Create your views here.

def home(request):
    featured_photographers = PhotographerProfile.objects.filter(user__userprofile__is_approved=True)[:6]
    return render(request, 'booking/home.html', {
        'featured_photographers': featured_photographers
    })

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        messages.success(request, f"Thank you {name}! Your message has been sent successfully. We will get back to you soon.")
        return redirect('contact')
    return render(request, 'booking/contact.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')

        if not username or not password or not confirm_password or not role:
            messages.error(request, 'Please fill in all required fields, including selecting a role.')
            return redirect('signup')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')       
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, role=role)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')
    return render(request, 'booking/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
            return redirect('login')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid User or Password')
            return redirect('login')
    return render(request, 'booking/login.html')


@login_required
def create_photographer_profile(request):
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile or user_profile.role != 'photographer' or not user_profile.is_approved:
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


@login_required
def edit_photographer_profile(request):
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile or user_profile.role != 'photographer' or not user_profile.is_approved:
        messages.warning(request, "You are not allowed to access this page.")
        return redirect('dashboard')

    try:
        profile = request.user.photographerprofile
    except PhotographerProfile.DoesNotExist:
        messages.error(request, "Photographer profile does not exist. Please create one first.")
        return redirect('create_photographer_profile')

    if request.method == 'POST':
        form = PhotographerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your photographer profile has been updated successfully!")
            return redirect('dashboard')
    else:
        form = PhotographerProfileForm(instance=profile)

    return render(request, 'booking/edit_photographer_profile.html', {'form': form, 'profile': profile})



def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def dashboard(request):
    user_profile = getattr(request.user, 'userprofile', None)
    if not user_profile:
        if request.user.is_superuser:
            return redirect('/admin/')
        messages.error(request, "User profile not found.")
        return redirect('home')

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
    existing_booking = Booking.objects.filter(
        photographer = photographer,
        status__in = ['pending', 'accepted', 'confirmed']
    ).values_list('date',flat=True)
    booked_dates = [d.strftime('%Y-%m-%d') for d in existing_booking]
    booked_dates_json = json.dumps(booked_dates)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        selected_date = request.POST.get('date')

        if selected_date in booked_dates:
            messages.error(request, f"This photographer is already booked on {selected_date}. Please pick another date.")
            return render(request, 'booking/book_photographer.html',{
                'form':form,
                'photographer': photographer,
                'booked_dates': booked_dates,
                'booked_dates_json': booked_dates_json,
            })
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.photographer = photographer
            booking.save()
            messages.success(request, "Your booking request has been sent successfully")
            return redirect('dashboard')
    else:
        form = BookingForm()
        context = {
            'form': form,
            'photographer': photographer,
            'booked_dates': booked_dates,
            'booked_dates_json': booked_dates_json,
        }
        return render(request, 'booking/book_photographer.html',context)

@login_required
def update_booking_status(request, booking_id, status):
    photographer_profile = get_object_or_404(PhotographerProfile, user=request.user)
    booking = get_object_or_404(Booking, id=booking_id, photographer=photographer_profile)
    photographer_name = photographer_profile.full_name or photographer_profile.user.username

    booking.status = status
    booking.save()

    Notification.objects.create(
        user=booking.customer,
        message=f"Your booking with {photographer_name} was {status}."
    )
    if status == "rejected":
        messages.info(request, "Booking request rejected.")
    else:
        messages.success(request, f"Booking {status} successfully!")
    return redirect('dashboard')


def photographer_list(request):
    photographers = PhotographerProfile.objects.filter(user__userprofile__is_approved=True)
    search_query = request.GET.get('search', '').strip()
    selected_location = request.GET.get('location', '').strip()
    selected_specialty = request.GET.get('specialty', '').strip()

    if search_query:
        photographers = photographers.filter(
            Q(full_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(specialty__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if selected_location:
        photographers = photographers.filter(location__iexact=selected_location)

    if selected_specialty:
        photographers = photographers.filter(specialty__iexact=selected_specialty)

    all_approved = PhotographerProfile.objects.filter(user__userprofile__is_approved=True)

    locations = sorted(list(set(all_approved.values_list('location', flat=True).exclude(location=''))))

    specialties = sorted(list(set(all_approved.values_list('specialty', flat=True).exclude(specialty=''))))

    context = {
        'photographers': photographers,
        'search_query': search_query,
        'selected_location': selected_location,
        'selected_specialty': selected_specialty,
        'locations': locations,
        'specialties': specialties,
    }

    return render(request, 'booking/photographer_list.html', context)