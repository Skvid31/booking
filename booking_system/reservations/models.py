from django.db import models



ROOM_TYPES = [
    ('conference', 'Конференц-зал'),
    ('office', 'Офіс'),
    ('meeting', 'Зала для зустрічей'),
]

class Room(models.Model):
    name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES, default='meeting')  # Додаємо тип кімнати
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ({self.get_room_type_display()})'


# Модель для бронювання
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Booking by {self.user_name} for {self.room.name}'

# Опційна модель для користувачів
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, default='user')

    def __str__(self):
        return self.user.username
