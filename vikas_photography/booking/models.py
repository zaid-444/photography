from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    ROLE_CHOICES=(
        ('client','Client'),
        ('photographer','Photographer'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_approved=models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username} - {self.role}'
    

class PhotographerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True) 
    phone_number = models.CharField(max_length=20, blank=True)
    specialty = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='photographers/', blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.username
    

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    photographer = models.ForeignKey(PhotographerProfile, on_delete=models.CASCADE, related_name="bookings")
    event_type = models.CharField(max_length=100, choices=[
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate Event'),
        ('other', 'Other'),
    ], default='other')
    venue = models.CharField(max_length=255, blank=True)
    guest_count = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ), default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer.username} → {self.photographer.user.username} ({self.status})"
    

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:20]}"
