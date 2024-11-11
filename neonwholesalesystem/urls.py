from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_user, name="login_user"),
    path('signup/', signup_user, name="signup_user"),
    path('logout/', logout_user, name="logout"),
    path('', index, name="Index"),
    path('product/', product, name="product"),
    path('viewproduct/', view_product, name="viewproduct"),
    path('addstock/<str:product_id>/', add_stock, name="addstock"),
    path('deletestock/<str:product_id>/', delete_stock, name="deletestock"),
    path('editproduct/<str:product_id>/', edit_product, name="editproduct"),
    path('showproduct/<str:product_id>/', show_product, name="showproduct"),
    path('deleteproduct/<str:product_id>/', delete_product, name="deleteproduct"),
    path('saveproduct/', save_product, name="saveproduct"),
    path('add/', add, name="Additem"),
    path('delete/', delete, name="Deleteitem"),
    path('delete/<str:id>/', delete_item, name="Deletetempitem"),
    path('createbill/', create_bill, name="Createbill"),
    path('pdf/', pdf, name="pdf"),
    path('viewpdf/<str:code>/', viewpdf, name="viewpdf"),
    path('customer/', customer, name="customer"),
    path('editcustomer/<str:code>/', edit_customer, name="editcustomer"),
]
