from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if not email:
            self.add_error('email', forms.ValidationError("Email is required."))

        if email and User.objects.filter(email=email).exists():
            self.add_error('email', forms.ValidationError("Email is already in use."))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True

        if commit:
            user.save()

        return user


class AddProduct(forms.ModelForm):
    name=models.CharField(max_length=350,blank=True, null=True)
    size = models.CharField(max_length=50)
    description = models.TextField()
    totalquantity = models.IntegerField(default=0)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

    class Meta:
        model = Product
        fields = ('name','size','description','totalquantity','price','status')
        labels = {
            'name': 'Product Name',
            'size': 'Product Size',
            'description': 'Description',
            'totalquantity': 'Quantity',
            'price': 'Price',
            'status': 'Status'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'null': 'True', 'rows': 4}),
            'totalquantity': forms.NumberInput(attrs={'class':'form-control', 'min': '0', 'max': '1000'}),
            'price': forms.NumberInput(attrs={'class':'form-control' , 'min':'0'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }



class EditProduct(forms.ModelForm):
    name=models.CharField(max_length=350,blank=True, null=True)
    size = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField(default=0)
    status = models.CharField(max_length=2, choices=(('1','Active'),('2','Inactive')), default=1)

    class Meta:
        model = Product
        fields = ('name','size','description','price','status')
        labels = {
            'name': 'Product Name',
            'size': 'Product Size',
            'description': 'Description',
            'price': 'Price',
            'status': 'Status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'null': 'True'}),
            'price': forms.NumberInput(attrs={'class':'form-control' , 'min':'0'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }

class EditCustomer(forms.ModelForm):
    custname = models.CharField(max_length=350)
    custnumb = models.IntegerField(default = 0 ,null=True, blank=True)
    payment = models.CharField(max_length=2, choices=(('1','Cash'),('2','Online'),('3','Pending')), default=1)

    class Meta:
        model = CustomerBill
        fields = ('custname', 'custnumb','payment')
        labels = {
            'custname': 'Customer Name',
            'custnumb': 'Customer No.',
            'payment': 'Payment',
        }
        widgets = {
            'custname': forms.TextInput(attrs={'class':'form-control'}),
            'custnumb': forms.NumberInput(attrs={'class':'form-control'}),
            'payment': forms.Select(attrs={'class':'form-control'}),
        }
        