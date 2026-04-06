from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # conectar app
    path('', include('equipos.urls')),
]