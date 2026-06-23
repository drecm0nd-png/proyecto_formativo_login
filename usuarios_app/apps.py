from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UsuariosAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios_app'

    def ready(self):
        post_migrate.connect(self.poblar_datos_iniciales, sender=self)

    def poblar_datos_iniciales(self, sender, **kwargs):
        Rol = self.get_model('Rol')
        Usuario = self.get_model('Usuario')
        Ingrediente = self.get_model('Ingrediente')
        Producto = self.get_model('Producto')

        # 1. Crear Roles
        roles = [
            {'tipo': 'Cliente', 'rol_numero': '01'},
            {'tipo': 'Encargado', 'rol_numero': '02'},
            {'tipo': 'Administrador', 'rol_numero': '03'},
        ]
        for r in roles:
            Rol.objects.get_or_create(rol_numero=r['rol_numero'], defaults={'tipo': r['tipo']})

        # 2. Crear Usuarios (uno de cada rol)
        if not Usuario.objects.exists():
            admin_rol = Rol.objects.get(rol_numero='03')
            encargado_rol = Rol.objects.get(rol_numero='02')
            cliente_rol = Rol.objects.get(rol_numero='01')

            Usuario.objects.create(numero='30020205051', correo='admin@jcasas.com', nombre='Andres Rodriguez', contrasenia='1234', rol=admin_rol)
            Usuario.objects.create(numero='30020205052', correo='encargado@jcasas.com', nombre='Julio Cesar', contrasenia='1234', rol=encargado_rol)
            Usuario.objects.create(numero='30020205053', correo='cliente@jcasas.com', nombre='Juan Fernandez', contrasenia='1234', rol=cliente_rol)

        # 3. Crear 10 Ingredientes
        if not Ingrediente.objects.exists():
            ingredientes_nombres = ['Carne Res', 'Queso Cheddar', 'Lechuga', 'Tomate', 'Pan', 'Pizza Masa', 'Salsa Tomate', 'Mozzarella', 'Albahaca', 'Pollo']
            for nombre in ingredientes_nombres:
                Ingrediente.objects.create(nombre=nombre, cantidad='100')

        # 4. Crear 5 Productos
        if not Producto.objects.exists():
    # Lista de productos con: (nombre, descripción, precio, imagen_url)
            productos_data = [
                ('Hamburguesa Casera', 'Carne de res, queso cheddar, lechuga y tomate', 15.00, 'https://resuelveconbimbo-com-v2-assets.s3.amazonaws.com/...'),
                ('Pizza Margarita', 'Base de tomate, mozzarella fresca y albahaca', 12.00, 'https://encrypted-tbn0.gstatic.com/images?q=tbn:AN...'),
                ('Ensalada Cesar', 'Lechuga romana, crutones, queso parmesano', 9.00, 'https://www.goodnes.com/sites/g/files/jgfbjl321/fi...'),
                ('Tacos al Pastor', 'Carne de cerdo marinada con piña', 8.00, 'https://comedera.com/wp-content/uploads/sites/9/20...'),
                ('Pollo Crispy', 'Pollo empanizado crujiente', 11.00, 'https://imag.bonviveur.com/pollo-frito-crujiente.j...'),
            ]
    
        for nombre, desc, precio, url in productos_data:
            Producto.objects.create(
                nombre=nombre, 
                descripcion=desc, 
                precio=precio, 
                imagen=url  # Aquí guardamos la URL real en lugar de un '1'
            )