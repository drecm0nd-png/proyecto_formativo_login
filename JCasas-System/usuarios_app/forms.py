from django import forms
# Descomenta esta línea eliminando el '#' del principio:
from .models import Producto, Ingrediente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto  # Ahora Python sabe qué es 'Producto'
        fields = ['nombre', 'descripcion', 'unidad_medida', 'precio', 'estado']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descripción'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Unidad, Kilo, Litro'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente # Ahora Python sabe qué es 'Ingrediente'
        fields = ['nombre', 'cantidad']
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del ingrediente (ej: Queso Mozzarella)'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 500 gramos, 2 Kilos, 10 Unidades'}),
        }