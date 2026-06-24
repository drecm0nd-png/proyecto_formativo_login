import uuid 
from django.db import models

# Tus modelos originales
class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=50, default='Unidad')
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estado = models.BooleanField(default=True)
    imagen = models.TextField(blank=True, null=True, default='default.png')
    ingredientes = models.ManyToManyField('Ingrediente', through='ProductoIngrediente', related_name='productos')

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f"PROD-{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Ingrediente(models.Model):
    codigo = models.CharField(max_length=30, unique=True, editable=False)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    cantidad = models.CharField(max_length=200, default='0') 

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = f"ING-{str(uuid.uuid4())[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class ProductoIngrediente(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad_requerida = models.CharField(max_length=100, verbose_name="Cantidad necesaria")

    def __str__(self):
        return f"{self.producto.nombre} usa {self.cantidad_requerida} de {self.ingrediente.nombre}"

class Rol(models.Model):
    tipo = models.CharField(max_length=30) # Ej: Cliente, Encargado, Admin
    rol_numero = models.CharField(max_length=2, unique=True) # Ej: 01, 02, 03

    def __str__(self):
        return f"{self.tipo} ({self.rol_numero})"

class Usuario(models.Model):
    numero = models.CharField(max_length=30, unique=True)
    correo = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=50)
    imagen = models.TextField(blank=True, null=True, default='default.png')
    contrasenia = models.CharField(max_length=255)
    # Relación: Si no se asigna, por defecto buscará el ID 1
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, default=1)