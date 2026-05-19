from django.contrib.auth.models import User
from  django.core.validators import  RegexValidator
from django.db import models

class Room(models.Model):
    name=models.CharField('Название комнаты', max_length=120)
    capacity = models.PositiveIntegerField('Вместимость')
    location = models.TextField('Расроложение', max_length=120)
    description = models.TextField('Краткое описание', blank=True)
    price_per_hour = models.DecimalField('Цена за час аренды', max_digits=10, decimal_places=2)
    is_active = models.BooleanField('Доступность комнаты', default=True)

    class Meta:
        verbouse_name = 'Помещение'
        verbouse_name_plural = 'Помещения'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.capacity} мест)'

class BookingRequest(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'Новая'
        APPOINTED = 'appointed', 'Мероприятие назначено'
        COMPLETED = 'completed', 'Мероприятие завершено'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличниые'
        CARD = 'card', 'Банковская карта'
        INVOICE = 'invoice', 'Безнал'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, verbose_name='Помещение')
    event_name = models.CharField('Название мероприятия', max_length=160)
    event_date = models.DateField('Дата мероприятия')
    preferred_time = models.TimeField('Предпочтительное время')
    payment_method = models.CharField('Способ оплаты', max_length=20, choices=PaymentMethod.choices)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.NEW)
    admin_comment = models.TextField('Комментарий администратора', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbouse_name = 'Заявка'
        verbouse_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.event_name} - {self.user.username}'

class Review(models.Model):
    booking = models.OneToOneField(BookingRequest, on_delete=models.CASCADE, verbose_name='Заявка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField('Отзыв')
    rating = models.PositiveSmallIntegerField('Оценка', default=5)
    created_at = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        verbouse_name = 'Отзыв'
        verbouse_name_plural = 'Отзывы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв {self.user.username} - {self.rating}/5'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField('ФИО', max_length=180)
    phone = models.CharField('Телефон', max_length=20, validators=[RegexValidator(r'^\+?[0--9\-\s\(\)]{10,20}$', 'Введите корректный номер телефона')])

    class Meta:
        verbouse_name = 'Профиль'
        verbouse_name_plural = 'Профили'

    def __str__(self):
        return self.full_name
