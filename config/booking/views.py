from django.contrib import messages
from  django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Q
from  django.shortcuts import get_object_or_404, redirect, render
from .forms import AdminBookingStatusForm, BookingRequestForm, LoginForm, RegisterForm, ReviewForm, RoomForm
from .models import BookingRequest, Review, Room

def is_exam_admin(user):
    return user.is_authenticated and user.is_staff

def home(request):
    rooms = Room.objects.filter(is_active=True)[:6]
    reviews = Review.objects.select_related('user', 'booking')[:3]
    return render(request, 'booking/home.html', {'rooms': rooms, 'reviews': reviews})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Регистрация прошла успешно.')
        return redirect('dashboard')
    return render(request, 'booking/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'booking/login.html'
    authentication_form = LoginForm

    def form_invalid(self, form):
        messages.error(self.request, 'Неверный логин или пароль.')
        return super().form_invalid(form)

    def get_success_url(self):
        if self.request.user.is_staff:
            return '/panel/'
        return '/dashboard/'


login_view = CustomLoginView.as_view()


@login_required
def dashboard(request):
    requests = BookingRequest.objects.filter(user=request.user).select_related('room')
    return render(request, 'booking/dashboard.html', {'requests': requests})


@login_required
def booking_create(request):
    form = BookingRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()
        messages.success(request, 'Заявка успешно отправлена.')
        return redirect('dashboard')
    return render(request, 'booking/booking_form.html', {'form': form})


@login_required
def review_create(request, pk):
    booking = get_object_or_404(BookingRequest, pk=pk, user=request.user)
    if booking.status == BookingRequest.Status.NEW:
        messages.error(request, 'Отзыв можно оставить только после изменения статуса заявки администратором.')
        return redirect('dashboard')
    if hasattr(booking, 'review'):
        messages.info(request, 'Вы уже оставили отзыв по этой заявке.')
        return redirect('dashboard')

    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.booking = booking
        review.user = request.user
        review.save()
        messages.success(request, 'Спасибо за отзыв.')
        return redirect('dashboard')
    return render(request, 'booking/review_form.html', {'form': form, 'booking': booking})


def reviews_page(request):
    reviews = Review.objects.select_related('user', 'booking', 'booking__room')
    return render(request, 'booking/reviews.html', {'reviews': reviews})


@user_passes_test(is_exam_admin)
def admin_panel(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    requests = BookingRequest.objects.select_related('user', 'room')

    if query:
        requests = requests.filter(
            Q(event_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(room__name__icontains=query)
        )
    if status:
        requests = requests.filter(status=status)

    paginator = Paginator(requests, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'booking/admin_panel.html', {
        'page_obj': page_obj,
        'query': query,
        'status': status,
        'status_choices': BookingRequest.Status.choices,
    })


@user_passes_test(is_exam_admin)
def admin_request_detail(request, pk):
    booking = get_object_or_404(BookingRequest.objects.select_related('user', 'room'), pk=pk)
    form = AdminBookingStatusForm(request.POST or None, instance=booking)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Статус заявки обновлен.')
        return redirect('admin_panel')
    return render(request, 'booking/admin_request_detail.html', {'form': form, 'booking': booking})



@user_passes_test(is_exam_admin)
def admin_room_list(request):
    query = request.GET.get('q', '')
    rooms = Room.objects.all()

    if query:
        rooms = rooms.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(rooms, 8)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'booking/admin_room_list.html', {
        'page_obj': page_obj,
        'query': query,
    })


@user_passes_test(is_exam_admin)
def admin_room_create(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Помещение успешно добавлено.')
        return redirect('admin_room_list')
    return render(request, 'booking/admin_room_form.html', {
        'form': form,
        'title': 'Добавление помещения',
        'button_text': 'Создать помещение',
    })

@user_passes_test(is_exam_admin)
def admin_room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instansce=room)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Помещение обновлено')
        return redirect('admin_room_list')
    return render(request, 'booking/admin_room_form.html', {
        'form': form,
        'room': room,
        'title': 'Редактирование помещения',
        'button_text': 'Сохранить изменения'
    })

@user_passes_test(is_exam_admin)
def admin_room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        try:
            room.delete()
            messages.success(request, 'Помещение удалено')
        except Exception:
            room.is_active = False
            room.save(update_fields=['is_active'])
            messages.warning(request, 'Помещение используется, оно будет скрыто, а не удалено')
        return redirect('admin_room_list')
    return render(request, 'booking/admin_room_confirm_delete.html', {'room': room})