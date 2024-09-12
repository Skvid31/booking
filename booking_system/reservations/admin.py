
from django.contrib import admin
from .models import Room, Booking

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'price', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'room', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'room')
    search_fields = ('user_name', 'email')
    actions = ['confirm_bookings', 'cancel_bookings']

    # Дії для підтвердження та скасування бронювань
    @admin.action(description='Підтвердити вибрані бронювання')
    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Скасувати вибрані бронювання')
    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')

admin.site.register(Room, RoomAdmin)
admin.site.register(Booking, BookingAdmin)
