# reservations/urls.py
from django.urls import path
from .views import booking_view, calendar_view, bookings_json, room_list_view, home_view

urlpatterns = [
    path('home/', home_view, name='home_view'),  # Головна сторінка
    path('booking/', booking_view, name='booking_view'),
    path('calendar/', calendar_view, name='calendar_view'),
    path('bookings-json/', bookings_json, name='bookings_json'),
    path('rooms/', room_list_view, name='room_list_view'),
]
