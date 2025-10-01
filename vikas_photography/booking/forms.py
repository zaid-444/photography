from django import forms
from .models import PhotographerProfile,Booking

class PhotographerProfileForm(forms.ModelForm):
    class Meta:
        model = PhotographerProfile
        fields = ['full_name', 'phone_number', 'specialty', 'location', 'profile_pic']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event_type', 'venue', 'guest_count', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }