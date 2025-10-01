from django.urls import path
from .views import *

urlpatterns=[
    path('',home,name='home'),
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('contact/',contact_view,name='contact'),
    path('photographer/profile/',create_photographer_profile, name='create_photographer_profile'),
    path('dashboard/',dashboard,name='dashboard'),
    path('photographer/<int:photographer_id>/book/', book_photographer, name='book_photographer'),
    path('update-booking/<int:booking_id>/<str:status>/',update_booking_status,name='update_booking_status')
]
urlpatterns += [
    path('photographers/', photographer_list, name='photographer_list'),
]