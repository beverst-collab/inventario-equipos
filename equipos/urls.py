from django.urls import path
from . import views

urlpatterns = [
    #  parte de autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #  inicio sistema
    path('', views.lista, name='lista'),
    path('crear/', views.crear, name='crear'),
    path('editar/<int:id>/', views.actualizar, name='editar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
]