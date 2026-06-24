
##################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from .models import Producto, Ingrediente, ProductoIngrediente, Usuario, Rol
from .forms import ProductoForm, IngredienteForm


#MOSTRAR MENSAJE
def mostrar_mensaje(request):
    return HttpResponse("Retornando un saludo al cliente de la aplicación")




def mostrar_pagina_inicio(request):
    productos = Producto.objects.all()
    usuario = None
    
    # Intentamos obtener al usuario de la BD si hay sesión iniciada
    if 'usuario_id' in request.session:
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
        except Usuario.DoesNotExist:
            pass # Si el usuario fue borrado pero la sesión persiste
            
    # Obtenemos el rol de forma segura
    rol_numero = str(usuario.rol.rol_numero) if usuario and usuario.rol else ''
    
    context = {
        'productos': productos,
        # Si el usuario existe, pasamos su nombre; si no, None
        'nombre_usuario': usuario.nombre if usuario else None,
        # Banderas para el template (más limpio que usar la sesión directo)
        'es_admin_o_encargado': rol_numero in ['02', '03'],
        'es_admin': rol_numero == '02',
        'es_encargado': rol_numero == '03',
    }
    return render(request, 'inicio.html', context)



#MOSTRAR MENSAJE
def mostrar_pagina_cliente(request):
    return render(request, 'usuarios_app/cliente.html')





#MOSTRAR MENSAJE
def registrar_producto(request):
    if request.session.get('rol_numero') != '02': 
        messages.error(request, "No tienes permiso para acceder aquí.")
        return redirect('inicio')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto_guardado = form.save() 
            return redirect('constituir_ingredients', producto_id=producto_guardado.id)
    else:
        form = ProductoForm() 
        
    return render(request, 'usuarios_app/registrar_producto.html', {'form': form})



#MOSTRAR MENSAJE

def ver_productos(request):
    productos = Producto.objects.all()
    return render(request, 'usuarios_app/ver_productos.html', {'productos': productos})





#MOSTRAR MENSAJE

def alterar_producto(request, producto_id):
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'guardar_todo':
            lista_ids = request.POST.getlist('producto_ids')
            for p_id in lista_ids:
                producto = get_object_or_404(Producto, id=p_id)
                producto.nombre = request.POST.get(f'nombre_{p_id}')
                producto.descripcion = request.POST.get(f'descripcion_{p_id}')
                producto.unidad_medida = request.POST.get(f'unidad_medida_{p_id}')
                producto.precio = request.POST.get(f'precio_{p_id}')
                producto.save() 
        else:
            producto = get_object_or_404(Producto, id=producto_id)
            if accion == 'cambiar_estado':
                producto.estado = not producto.estado  
                producto.save()
            elif accion == 'eliminar_producto':
                producto.delete() 
                
    return redirect('ver_productos')



#MOSTRAR MENSAJE

def registrar_ingrediente(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            ingrediente_guardado = form.save()
            return render(request, 'usuarios_app/constituir_ingredientes.html', {'ingrediente': ingrediente_guardado})
    else:
        form = IngredienteForm()
        
    return render(request, 'usuarios_app/registrar_ingrediente.html', {'form': form})




#MOSTRAR MENSAJE

def ver_ingredientes(request):
    ingredientes = Ingrediente.objects.all()
    return render(request, 'usuarios_app/ver_ingredientes.html', {'ingredientes': ingredientes})




#MOSTRAR MENSAJE

def alterar_ingrediente(request, ingrediente_id):
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'guardar_todo':
            lista_ids = request.POST.getlist('ingrediente_ids')
            for ing_id in lista_ids:
                ingrediente = get_object_or_404(Ingrediente, id=ing_id)
                ingrediente.nombre = request.POST.get(f'nombre_{ing_id}')
                ingrediente.cantidad = request.POST.get(f'cantidad_{ing_id}')
                ingrediente.save()
                
        elif accion == 'eliminar_ingrediente':
            ingrediente = get_object_or_404(Ingrediente, id=ingrediente_id)
            ingrediente.delete()
            
    return redirect('ver_ingredientes')




#MOSTRAR MENSAJE

def constituir_ingredients(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        
        if accion == 'asociar_ingrediente':
            ProductoIngrediente.objects.filter(producto=producto).delete()
            ingrediente_ids = request.POST.getlist('ingrediente_ids')
            for ing_id in ingrediente_ids:
                cantidad_req = request.POST.get(f'cantidad_{ing_id}')
                if cantidad_req and cantidad_req.strip():
                    ingrediente = get_object_or_404(Ingrediente, id=ing_id)
                    ProductoIngrediente.objects.create(
                        producto=producto,
                        ingrediente=ingrediente,
                        cantidad_requerida=cantidad_req
                    )
            return redirect('ver_productos')
        
        elif accion == 'crear_rapido':
            form_ing = IngredienteForm(request.POST)
            if form_ing.is_valid():
                nuevo_ing = form_ing.save()
                cantidad_req = request.POST.get('cantidad_requerida_nuevo')
                if cantidad_req and cantidad_req.strip():
                    ProductoIngrediente.objects.create(
                        producto=producto,
                        ingrediente=nuevo_ing,
                        cantidad_requerida=cantidad_req
                    )
            return redirect('constituir_ingredients', producto_id=producto.id)

    context = {
        'producto': producto,
        'receta_actual': ProductoIngrediente.objects.filter(producto=producto),
        'todos_los_ingredientes': Ingrediente.objects.all(),
        'form_ingrediente': IngredienteForm()
    }
    return render(request, 'usuarios_app/constituir_ingredientes.html', context)




#MOSTRAR MENSAJE

# Asegura que la vista acepte el token CSRF
def cambiar_imagen_producto(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        nueva_url = request.POST.get('nueva_imagen')
        if nueva_url:
            producto.imagen = nueva_url
            producto.save()
        return redirect('inicio') # O la vista donde quieras volver
    return redirect('inicio')


from django.contrib.auth.hashers import check_password 
from django.shortcuts import render, redirect
from django.contrib import messages





#MOSTRAR MENSAJE

from django.contrib.auth.hashers import check_password # Importa esto

def inicio_sesion(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        usuario_obj = Usuario.objects.filter(correo=email).first()
        
        if usuario_obj:
            # 1. Comprobamos si el campo parece un hash (empieza por 'pbkdf2_')
            es_hash = str(usuario_obj.contrasenia).startswith('pbkdf2_')
            
            # 2. Verificamos según el tipo de dato
            if es_hash:
                # Usa el método seguro de Django
                es_valido = check_password(password, usuario_obj.contrasenia)
            else:
                # Usa comparación directa para texto plano
                es_valido = (str(usuario_obj.contrasenia).strip() == password.strip())
            
            if es_valido:
                # Login exitoso
                request.session['usuario_id'] = usuario_obj.id
                request.session['nombre_usuario'] = usuario_obj.nombre
                # ... resto de la lógica de sesión
                return redirect('inicio')
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
            
    return render(request, 'usuarios_app/inicio_sesion.html')




#MOSTRAR MENSAJE

def cerrar_sesion(request):
    request.session.flush()
    return redirect('inicio')




#MOSTRAR MENSAJE

def restablecer_contrasena(request):
    return render(request, 'usuarios_app/restablecer_contrasena.html')




#MOSTRAR MENSAJE

def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("first_name", "").strip()
        correo = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        telefono = request.POST.get("numero", "").strip()

        if not nombre or not correo or not password or not telefono:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, "usuarios_app/registro.html")

        if password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "usuarios_app/registro.html")
        
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Este correo ya está registrado.")
            return render(request, "usuarios_app/registro.html")
            
        if Usuario.objects.filter(numero=telefono).exists():
            messages.error(request, "Este número de teléfono ya está registrado.")
            return render(request, "usuarios_app/registro.html")

        rol_cliente = Rol.objects.filter(rol_numero='01').first()
        nuevo_usuario = Usuario.objects.create(
            nombre=nombre,
            correo=correo,
            contrasenia=make_password(password),
            numero=telefono,
            rol=rol_cliente
        )

        request.session['usuario_id'] = nuevo_usuario.id
        request.session['nombre'] = nuevo_usuario.nombre
        request.session['rol_numero'] = rol_cliente.rol_numero
        request.session.save()
        
        return redirect("inicio")
    
    return render(request, "usuarios_app/registro.html")




#MOSTRAR MENSAJE

def perfil(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('inicio_sesion')
    
    # IMPORTANTE: Busca siempre al usuario en la BD, no en la sesión
    usuario = Usuario.objects.get(id=usuario_id)
    
    contexto = {
        'nombre': usuario.nombre,
        'correo': usuario.correo,
        'numero': usuario.numero,
        'tipo': usuario.rol.tipo if usuario.rol else 'Sin rol',
        'imagen_url': usuario.imagen, # Asegúrate que aquí usas el campo de la BD
    }
    return render(request, 'usuarios_app/perfil.html', contexto)




#MOSTRAR MENSAJE


def actualizar_perfil(request):
    if request.method == 'POST':
        # 1. Recuperar el usuario usando la sesión
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            return redirect('login') 
        
        usuario = get_object_or_404(Usuario, id=usuario_id)
        
        # 2. Asignar los valores del formulario
        usuario.nombre = request.POST.get('nombre', usuario.nombre)
        usuario.correo = request.POST.get('correo', usuario.correo)
        usuario.numero = request.POST.get('numero', usuario.numero)
        
        # 3. Lógica para la imagen
        nueva_url = request.POST.get('imagen_url')
        
        # Guardamos 'default.png' si está vacío para que tu lógica de frontend funcione
        if not nueva_url or nueva_url.strip() == "" or nueva_url == '1':
            usuario.imagen = 'default.png'
        else:
            usuario.imagen = nueva_url
            
        # 4. Guardar cambios
        usuario.save()
        
        # 5. IMPORTANTE: Redireccionar de vuelta al perfil tras el POST
        # Esto evita el error de "reenviar formulario" si el usuario presiona F5
        return redirect('perfil') 
    
    # Si alguien intenta entrar a esta URL mediante GET, lo mandamos al perfil
    return redirect('perfil')