from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import BookingRequest, Review, Room, UserProfile


BOOTSTRAP_TEXT_INPUTS = (
    forms.TextInput, forms.EmailInput, forms.PasswordInput, forms.NumberInput,
    forms.DateInput, forms.TimeInput, forms.Textarea,
)


def apply_bootstrap_classes(form):
    for field in form.fields.values():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs.setdefault('class', 'form-check-input')
        elif isinstance(widget, forms.Select):
            widget.attrs.setdefault('class', 'form-select')
        else:
            widget.attrs.setdefault('class', 'form-control')


#Форма регистрации
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    full_name = forms.CharField(label='ФИО', max_length=180)
    phone = forms.CharField(label='Телефон', max_length=20)
    email = forms.EmailField(label='Электронная почта')

    class Meta:
        model = User
        fields = ['username', 'full_name', 'phone', 'email', 'password1', 'password2']
        labels = {'username': 'Логин'}

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise ValidationError('Логин должен быть не короче 6 символов.')
        if not username.isalnum() or not username.isascii():
            raise ValidationError('Логин должен содержать только латинские буквы и цифры.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if password and len(password) < 8:
            raise ValidationError('Пароль должен быть не короче 8 символов.')
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                phone=self.cleaned_data['phone'],
            )
        return user

#Форма авторизации
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


#Форма составления заявки
class BookingRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    class Meta:
        model = BookingRequest
        fields = ['room', 'event_name', 'event_date', 'preferred_time', 'payment_method']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'type': 'time'}),
        }

#Форма изменения статуса заявки
class AdminBookingStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    class Meta:
        model = BookingRequest
        fields = ['status', 'admin_comment']

#Форма отзыва
class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'text': forms.Textarea(attrs={'rows': 4}),
        }


#Форма сотавление комнаты
class RoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_bootstrap_classes(self)

    class Meta:
        model = Room
        fields = ['name', 'capacity', 'location', 'description', 'price_per_hour', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
