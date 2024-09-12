
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Booking
from .models import ROOM_TYPES
from django.shortcuts import render
from .models import Room


def home_view(request):
    return render(request, 'reservations/home.html')

def room_list_view(request):
    # Отримання всіх активних кімнат
    rooms = Room.objects.filter(is_active=True)
    return render(request, 'reservations/room_list.html', {'rooms': rooms})


def calendar_view(request):
    # Отримуємо всі доступні типи кімнат для фільтрації
    room_types = ROOM_TYPES
    selected_type = request.GET.get('room_type')  # Отримання вибраного типу кімнати з параметрів запиту

    # Фільтрація кімнат на основі обраного типу
    rooms = Room.objects.filter(is_active=True)
    if selected_type:
        rooms = rooms.filter(room_type=selected_type)

    return render(request, 'reservations/calendar.html', {'room_types': room_types, 'selected_type': selected_type})


def home_view(request):
    # Відображення головної сторінки
    return render(request, 'reservations/home.html')
def bookings_json(request):
    room_type = request.GET.get('room_type')
    bookings = Booking.objects.filter(status='confirmed')

    if room_type:
        bookings = bookings.filter(room__room_type=room_type)  # Фільтруємо бронювання по типу кімнати

    events = []
    for booking in bookings:
        events.append({
            'title': f'Бронювання: {booking.room.name}',
            'start': booking.start_date.isoformat(),
            'end': booking.end_date.isoformat(),
        })

    return JsonResponse(events, safe=False)


def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            # Відправка підтвердження на електронну пошту
            send_mail(
                'Підтвердження бронювання',
                f'Ваше бронювання для кімнати {booking.room.name} з {booking.start_date} до {booking.end_date} успішно створено.',
                settings.EMAIL_HOST_USER,
                [booking.email],
                fail_silently=False,
            )
            messages.success(request, 'Бронювання успішно створено. Перевірте вашу електронну пошту для підтвердження.')
            return redirect('booking_view')
    else:
        form = BookingForm()

    return render(request, 'reservations/booking.html', {'form': form})
