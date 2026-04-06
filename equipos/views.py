from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from .models import Equipo


def es_admin(user):
    return user.groups.filter(name='admin').exists()


# LOGIN
def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('lista')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})

    return render(request, 'login.html')


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect('login')


# LISTAR-----filtros
@login_required
def lista(request):
    equipos = Equipo.objects.all()

    # 🔍 BUSCADOR----GENERAL
    q = request.GET.get('q')
    if q:
        equipos = equipos.filter(
            Q(nombre__icontains=q) |
            Q(marca__icontains=q) |
            Q(modelo__icontains=q) |
            Q(serial__icontains=q)
        )

    #  FILTRO  POR TIPO
    tipo = request.GET.get('tipo_equipo')
    if tipo and tipo != "Todos":
        equipos = equipos.filter(tipo_equipo__iexact=tipo)

    # FILTRO POR ESTADO
    estado = request.GET.get('estado')
    if estado and estado != "Todos":
        equipos = equipos.filter(estado__iexact=estado)

    return render(request, 'lista.html', {
        'equipos': equipos,
        'es_admin': es_admin(request.user)
    })


# CREAR----ACTIVO
@login_required
def crear(request):
    if request.method == 'POST':
        Equipo.objects.create(
            nombre=request.POST['nombre'],
            tipo_equipo=request.POST['tipo_equipo'],
            marca=request.POST['marca'],
            modelo=request.POST['modelo'],
            serial=request.POST['serial'],
            cantidad=request.POST['cantidad'],
            estado=request.POST['estado'],
            fecha_registro=request.POST['fecha_registro']
        )
        messages.success(request, "Equipo creado correctamente")
        return redirect('lista')

    return render(request, 'crear.html')


# EDITAR--ACTIVO
@login_required
def actualizar(request, id):
    equipo = get_object_or_404(Equipo, id=id)

    if not es_admin(request.user):
        return redirect('lista')

    if request.method == 'POST':
        equipo.nombre = request.POST['nombre']
        equipo.tipo_equipo = request.POST['tipo_equipo']
        equipo.marca = request.POST['marca']
        equipo.modelo = request.POST['modelo']
        equipo.serial = request.POST['serial']
        equipo.cantidad = request.POST['cantidad']
        equipo.estado = request.POST['estado']
        equipo.fecha_registro = request.POST['fecha_registro']
        equipo.save()

        messages.success(request, "Equipo actualizado")
        return redirect('lista')

    return render(request, 'editar.html', {'equipo': equipo})


# ELIMINAR---ACTIVO
@login_required
def eliminar(request, id):
    if not es_admin(request.user):
        return redirect('lista')

    equipo = get_object_or_404(Equipo, id=id)
    equipo.delete()

    messages.success(request, "Equipo eliminado")
    return redirect('lista')