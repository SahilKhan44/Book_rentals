# rentals/urls.py

from django.urls import path
from . import views
# from .views import login_view ,logout_view   # Import the login view


urlpatterns = [ 

    path('register/', views.register_view,name= 'register'),
    path('', views.login_view,name= 'login'),
    path('logout/', views.logout_view,name= 'logout'),
    path('dashboard/', views.dashboard_view,name= 'dashboard'),

    path('home/', views.home, name='home'),
    path('search_books/', views.search_books, name='search_books'),
    path('rent_book/<str:book_id>/', views.rent_book, name='rent_book'),
    path('rental_dashboard/', views.rental_dashboard, name='rental_dashboard'),
    path('extend_rental/<int:rental_id>/', views.extend_rental, name='extend_rental'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
