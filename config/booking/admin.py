from django.contrib import admin
from .models import BookingRequest, Review, Room, UserProfile

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'location', 'price_per_hour', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')


@admin.register(BookingRequest)
class BookingRequestAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'user', 'room', 'event_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'event_date')
    search_fields = ('event_name', 'user__username', 'room__name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'rating', 'created_at')
    search_fields = ('user__username', 'text')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'user')
