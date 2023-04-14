from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_category', 'description', 'price', 'image', 'quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
# class ProductForm(forms.Form):
#     product_name = forms.CharField(max_length=100)
#     product_category = forms.CharField(max_length=100)
#     description = forms.CharField(widget=forms.Textarea)
#     price = forms.DecimalField(decimal_places=2)
#     image = forms.ImageField()
#     quantity = forms.IntegerField()