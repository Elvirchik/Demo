from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/create/', views.booking_create, name='booking_create'),
    path('booking/<int:pk>/review/', views.review_create, name='review_create'),
    path('reviews/', views.reviews_page, name='reviews'),

    path('panel/', views.admin_panel, name='admin_panel'),
    path('panel/request/<int:pk>/', views.admin_request_detail, name='admin_request_detail'),

    path('panel/rooms/', views.admin_room_list, name='admin_room_list'),
    path('panel/rooms/create/', views.admin_room_create, name='admin_room_create'),
    path('panel/rooms/<int:pk>/edit/', views.admin_room_edit, name='admin_room_edit'),
    path('panel/rooms/<int:pk>/delete/', views.admin_room_delete, name='admin_room_delete'),
]
