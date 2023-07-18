from decimal import Decimal
from django.forms import *
from django import forms
from SalesPoint.core.erp.models import Category, Client, Product, Sale, Entity
from django.core.validators import MinValueValidator, MaxValueValidator


class EntityForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = "form-control"
            form.field.widget.attrs["autocomplete"] = "off"
            form.field.widget.attrs["placeholder"] = "Ingrese " + form.label.lower()
        self.fields["ruc"].widget.attrs["autofocus"] = True

    class Meta:
        model = Entity
        fields = "__all__"
        labels = {
            "ruc": "RUC",
            "social_reason": "Razón Social",
            "commercial_name": "Nombre Comercial",
            "main_address": "Dirección Matriz",
            "stablishment_address": "Dirección Establecimiento",
            "stablishment_code": "Código Establecimiento",
            "emition_point_code": "Código Punto de Emisión",
            "contability_obligation": "Obligado a llevar contabilidad",
            "logo": "Logo",
            "enviroment": "Entorno",
        }


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = "form-control"
            form.field.widget.attrs["autocomplete"] = "off"
            form.field.widget.attrs["placeholder"] = "Ingrese " + form.label.lower()
        self.fields["name"].widget.attrs["autofocus"] = True

    class Meta:
        model = Category
        fields = "__all__"
        labels = {
            "name": "Nombre",
        }


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = "form-control"
            form.field.widget.attrs["autocomplete"] = "off"
            form.field.widget.attrs["placeholder"] = "Ingrese " + form.label.lower()
        self.fields["names"].widget.attrs["autofocus"] = True
        self.fields["birth"].widget = forms.DateInput(attrs={"type": "date"})

    class Meta:
        model = Client
        fields = "__all__"
        labels = {
            "names": "Nombre",
            "surnames": "Apellido",
            "dni": "Cédula",
            "birth": "Fecha de Nacimiento",
            "address": "Dirección",
            "phone": "Número de Télefono",
            "mail": "Email",
            "gender": "Sexo",
        }


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = "form-control"
            form.field.widget.attrs["autocomplete"] = "off"
            form.field.widget.attrs["placeholder"] = "Ingrese " + form.label.lower()
        self.fields["name"].widget.attrs["autofocus"] = True

    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "names": "Nombre",
            "category": "Categoria",
            "image": "Imagen",
            "pvp": "Precio",
        }


class CategoryIVAForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Categoría",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    new_iva = forms.ChoiceField(
        choices=[("custom", "Ingresar por teclado")],
        label="Nuevo IVA",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    new_iva_value = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("20.00"))],
        label="Nuevo IVA (Ingresar por teclado)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs["class"] = "form-control"
            form.field.widget.attrs["autocomplete"] = "off"
            form.field.widget.attrs["placeholder"] = "Ingrese " + form.label.lower()
        self.fields["client"].widget.attrs["autofocus"] = True
        self.fields["subtotal"].widget.attrs["readonly"] = True
        self.fields["total"].widget.attrs["readonly"] = True
        # self.fields['date_sale'].widget = forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = Sale
        fields = "__all__"
        labels = {
            "client": "Cliente",
            "date_sale": "Fecha de Venta",
            "subtotal": "Subtotal",
            "iva": "IVA",
            "total": "Total",
        }


class TestForm(Form):
    categories = ModelChoiceField(
        queryset=Category.objects.all(),
        widget=Select(attrs={"class": "form-control select2", "style": "width: 100%"}),
    )

    products = ModelChoiceField(
        queryset=Product.objects.none(),
        widget=Select(attrs={"class": "form-control select2", "style": "width: 100%"}),
    )

    search = CharField(
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese una descripción"}
        )
    )
