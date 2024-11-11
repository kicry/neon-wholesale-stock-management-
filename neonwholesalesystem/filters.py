import django_filters
from django_filters import DateFilter, CharFilter
from django import forms
from .models import *

class CustomerFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr="gte", label="Start Date", widget=forms.DateInput(attrs={'class': 'form-control mt-1 col-lg-3','placeholder': 'Select Start Date','type': 'date'}, format='%d-%m-%Y'))
    end_date = DateFilter(field_name="date_created", lookup_expr="lte", label="End Date", widget=forms.DateInput(attrs={'class': 'form-control mt-1 col-lg-3','placeholder': 'Select End Date','type': 'date'}, format='%d-%m-%Y'))
    itemcode = CharFilter(field_name="itemcode", label="Bill Code", lookup_expr="icontains", widget=forms.TextInput(attrs={'class': 'form-control mt-1 col-lg-3','placeholder': 'Enter Bill Code'}))

    class Meta:
        model = CustomerBill
        fields = ('itemcode','payment')
        labels = {
            'payment': 'Payment',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.form.fields:
            self.form.fields[field_name].widget.attrs.update({'class': 'form-control mt-1 col-lg-3'})


class ProductFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr="gte", label="Start Date", widget=forms.DateInput(attrs={'class': 'form-control mt-1 col-lg-3','placeholder': 'Select Start Date','type': 'date'}, format='%d-%m-%Y'))
    end_date = DateFilter(field_name="date_created", lookup_expr="lte", label="End Date", widget=forms.DateInput(attrs={'class': 'form-control mt-1 col-lg-3','placeholder': 'Select End Date','type': 'date'}, format='%d-%m-%Y'))
    name = CharFilter(field_name="name", label="Name", lookup_expr="icontains", widget=forms.TextInput(attrs={'class': 'form-control mt-1 col-lg-3', 'placeholder': 'Enter Product Name'}))

    class Meta:
        model = Product
        fields = ('name', 'status')
        labels = {
            'name' : 'Name',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.form.fields:
            self.form.fields[field_name].widget.attrs.update({'class': 'form-control mt-1 col-lg-3'})
            