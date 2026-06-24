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

        # 2. Crear Usuarios
        if not Usuario.objects.exists():
            admin_rol = Rol.objects.get(rol_numero='03')
            encargado_rol = Rol.objects.get(rol_numero='02')
            cliente_rol = Rol.objects.get(rol_numero='01')

            Usuario.objects.create(numero='30020205051', correo='admin@jcasas.com', nombre='Andres Rodriguez', contrasenia='1234', rol=admin_rol, imagen= "https://i.pinimg.com/236x/d2/9e/bd/d29ebd9d5dcb19cd26980a4338e842a0.jpg")
            Usuario.objects.create(numero='30020205052', correo='encargado@jcasas.com', nombre='Julio Cesar', contrasenia='1234', rol=encargado_rol, imagen= "https://i.pinimg.com/736x/ec/4b/98/ec4b9865156249d0a46911ef9fdf2b5d.jpg")
            Usuario.objects.create(numero='30020205053', correo='cliente@jcasas.com', nombre='Juan Fernandez', contrasenia='1234', rol=cliente_rol, imagen= "https://i.redd.it/what-do-u-think-of-pomni-v0-z61d1348celf1.jpg?width=736&format=pjpg&auto=webp&s=e5a4476f502c7a55314a7bc46369854948d35c8a")

        # 3. Crear 10 Ingredientes
        if not Ingrediente.objects.exists():
            ingredientes_nombres = ['Carne Res', 'Queso Cheddar', 'Lechuga', 'Tomate', 'Pan', 'Pizza Masa', 'Salsa Tomate', 'Mozzarella', 'Albahaca', 'Pollo']
            for nombre in ingredientes_nombres:
                Ingrediente.objects.create(nombre=nombre, cantidad='100')

        # 4. Crear 5 Productos
        if not Producto.objects.exists():
            productos_data = [
                ('Hamburguesa Casera', 'Carne de res, queso cheddar, lechuga y tomate', 15.00, 'https://www.recetasnestle.com.ec/sites/default/files/styles/recipe_detail_mobile/public/srh_recipes/4e4293857c03d819e4ae51de1e86d66a.jpg?itok=GtJnAEZ6'),
                ('Pizza Margarita', 'Base de tomate, mozzarella fresca y albahaca', 12.00, 'https://cdn.blog.paulinacocina.net/wp-content/uploads/2023/09/pizza-margherita-paulina-cocina-recetas.jpg'),
                ('Ensalada Cesar', 'Lechuga romana, crutones, queso parmesano', 9.00, 'https://www.goodnes.com/sites/g/files/jgfbjl321/files/srh_recipes/755f697272cbcdc6e5df2adb44b1b705.jpg'),
                ('Tacos al Pastor', 'Carne de cerdo marinada con piña', 8.00, 'https://images.getrecipekit.com/20240719202231-srf-20pork-20collar-20tacos-20al-20pastor-2-35836-20-1.jpg?aspect_ratio=1:1&quality=90&'),
                ('Pollo Crispy', 'Pollo empanizado crujiente', 11.00, 'https://imag.bonviveur.com/pollo-frito-crujiente.jpg'),
            ]
    
            for nombre, desc, precio, url in productos_data:
                Producto.objects.create(
                    nombre=nombre, 
                    descripcion=desc, 
                    precio=precio, 
                    imagen=url 
                )