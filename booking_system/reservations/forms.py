
from django import forms
from .models import Booking, Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user_name', 'email', 'room', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    # Перевірка доступності кімнати на обрані дати
    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if room and start_date and end_date:
            existing_bookings = Booking.objects.filter(
                room=room,
                start_date__lt=end_date,
                end_date__gt=start_date,
                status='confirmed'
            )
            if existing_bookings.exists():
                raise forms.ValidationError('Кімната вже заброньована на ці дати.')
        return cleaned_data
