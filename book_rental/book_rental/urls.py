from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rentals.urls')),
    # path('auth/', include('rentals.urls')),  # This includes password reset URLs

]
