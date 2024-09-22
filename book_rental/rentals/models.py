# rentals/models.py

from django.db import models
from django.contrib.auth.models import User
# from datetime import datetime

class Book(models.Model):
    id = models.CharField(max_length=100, primary_key=True)  # Using the OpenLibrary ID as primary key
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    number_of_pages = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    # end_date = models.DateField()


    @property
    def calculate_fee(self):
        # Assuming a fee of $0.01 per page for each additional month
        # First month is free, so only charge for months after the first
        from datetime import datetime
        today = datetime.today().date()
        months_rented = (today.year - self.start_date.year) * 12 + today.month - self.start_date.month
        if months_rented > 1:
            return (self.book.number_of_pages / 100) * (months_rented - 1)
        return 0.0

    def __str__(self):
        return f'{self.book.title} rented by {self.user.username}'

