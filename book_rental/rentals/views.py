# rentals/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Rental
import requests
# views.py
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib import messages


@login_required
def home(request):
    return render(request, 'rentals/home.html')

@login_required
def search_books(request):
    title = request.GET.get('title')
    books = []
    if title:
        response = requests.get(f"https://openlibrary.org/search.json?title={title}")
        data = response.json()
        books = [
            {
                'id': book.get('key').split('/')[-1],
                'title': book.get('title'),
                'author': ', '.join(book.get('author_name', [])),
                'number_of_pages': book.get('number_of_pages_median', 0)
            }
            for book in data.get('docs', [])
        ]
    return render(request, 'rentals/search_books.html', {'books': books})

@login_required
def rent_book(request, book_id):
    # Check if the book exists in the database
    try:
        book = Book.objects.filter(id=book_id).first()
    except Book.DoesNotExist:
        # If not found, handle the error, e.g., show an error message
        return render(request, 'rentals/404.html', status=404)
    
    Rental.objects.create(user=request.user, book=book)
    return redirect('rental_dashboard')


@login_required
def extend_rental(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    if rental.user != request.user:
        return render(request, 'rentals/404.html', {'message': 'Unauthorized access.'}, status=403)

    rental.save()
    return redirect('rental_dashboard')

# rentals/views.py

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return render(request, 'rentals/error.html', {'message': 'Access denied.'}, status=403)

    rentals = Rental.objects.all()
    return render(request, 'rentals/admin_dashboard.html', {'rentals': rentals})


@login_required

def rental_dashboard(request):
    rentals = Rental.objects.filter(user=request.user)
    return render(request, 'rentals/rental_dashboard.html', {'rentals': rentals})




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            # If form is not valid, re-render the login page with the form
            initial_data = {'usrname':'','password':''}
            return render(request, 'rentals/auth/login.html', {'form': form})
    else:
        # For GET requests, render the login page with an empty form
        form = AuthenticationForm()
        return render(request, 'rentals/auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'rentals/auth/register.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'rentals/auth/dashboard.html')



