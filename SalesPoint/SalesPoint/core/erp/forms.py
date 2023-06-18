from django.forms import ModelForm

from SalesPoint.core.erp.models import Category


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = Category
        fields = '__all__'
        labels = {
            'name': 'Nombre',
        }
        