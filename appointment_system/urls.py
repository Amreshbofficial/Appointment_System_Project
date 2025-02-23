from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/signup/')),  # Redirect root URL to signup
    path('', include('bookings.urls')),
]