from django.contrib import admin
from .models import Book, Rental

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'number_of_pages')

class RentalAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'start_date',)  # Remove end_date and is_active
    list_filter = ('start_date',)  # Filter by start_date

admin.site.register(Book)
admin.site.register(Rental, RentalAdmin)