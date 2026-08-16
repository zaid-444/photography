from django import forms
from .models import PhotographerProfile,Booking

class PhotographerProfileForm(forms.ModelForm):
    class Meta:
        model = PhotographerProfile
        fields = ['full_name', 'phone_number', 'specialty', 'location', 'profile_pic']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client_name', 'client_phone', 'client_email', 'event_type', 'venue', 'guest_count', 'date', 'time', 'message']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        event_date = cleaned_data.get('date')
        if event_date:
            from datetime import date
            if event_date < date.today():
                raise forms.ValidationError('You cannot select a past date.')
        return cleaned_data