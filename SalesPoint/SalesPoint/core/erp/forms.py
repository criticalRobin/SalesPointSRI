from django.forms import ModelForm, DateInput
from django import forms
from SalesPoint.core.erp.models import Category, Client, Product, Sale


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['placeholder'] = 'Ingrese ' + form.label.lower()
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Nombre',
        }
        
        
class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['placeholder'] = 'Ingrese ' + form.label.lower()
        self.fields['names'].widget.attrs['autofocus'] = True
        self.fields['birth'].widget = forms.DateInput(attrs={'type': 'date'})
    
    class Meta:
        model = Client
        fields = '__all__'
        labels = {
            'names': 'Nombre',
            'surnames': 'Apellido',
            'dni': 'Cédula',
            'birth': 'Fecha de Nacimiento',
            'address': 'Dirección',
            'phone': 'Número de Télefono',
            'mail': 'Email',
            'gender': 'Sexo',
        }
        
        
class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['placeholder'] = 'Ingrese ' + form.label.lower()
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'names': 'Nombre',
                'category': 'Categoria',
            'image': 'Imagen',
            'pvp': 'Precio',
        }
        
        
class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['placeholder'] = 'Ingrese ' + form.label.lower()
        self.fields['client'].widget.attrs['autofocus'] = True
        self.fields['subtotal'].widget.attrs['readonly'] = True
        self.fields['total'].widget.attrs['readonly'] = True
        # self.fields['date_sale'].widget = forms.DateInput(attrs={'type': 'date'})
    
    class Meta:
        model = Sale
        fields = '__all__'
        labels = {
            'client': 'Cliente',
            'date_sale': 'Fecha de Venta',
            'subtotal': 'Subtotal',
            'iva': 'IVA',
            'total': 'Total',
        }