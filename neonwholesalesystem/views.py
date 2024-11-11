from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import datetime
from django.contrib import messages
from django.db.models import Sum
from django.core.paginator import Paginator
from .filters import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

def login_user(request):
    logout(request)
    try:
        if request.user.is_authenticated:
            return redirect('/')

        if request.method == "POST":
            username = request.POST['username']
            userpassword = request.POST['password']
            myuser = User.objects.filter(username = username)
            if not myuser.exists():
                messages.warning(request,"Invalid Credentials")
                return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            myuser = authenticate (username = username, password=userpassword)
            if myuser is not None:
                if myuser.is_staff or myuser.is_superuser:
                    login(request, myuser)
                    return redirect(request.POST.get('next', '/'))
                else:
                    messages.warning(request, 'User Unauthorized')
                    return redirect('/login/')
            else:
                messages.warning(request, 'Invalid Password')
                return redirect('/login/')

        return render(request,'login.html')
    except Exception as e:
        print(e)

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')

def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Account Created Successfully')
            return redirect('login_user')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# @login_required
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'documentation.html')
    products = Product.objects.filter(status = 1).all()
    tempproducts = Tempitem.objects.all()
    total_price = Tempitem.objects.aggregate(total_price=models.Sum('temptotal'))
    context={
                'products': products,
                'bill_items': tempproducts,
                'total_price': total_price,
            }
    return render(request, 'index.html', context)

@login_required
def add(request):
    if request.method == 'POST':
        selected_items = request.POST.get('pid')
        selected_size = request.POST.get('itemsize')
        selected_price = request.POST.get('itemprice')
        if selected_items is None:
            messages.warning(request, f'Select the item.')
            return redirect('/')
        # price = Product.objects.filter(name = selected_items, size=selected_size).values('price')
        price = float(selected_price)
        quntity = Product.objects.filter(name = selected_items, size=selected_size).values('totalquantity')
        quntity = quntity[0]['totalquantity']
        # price = price[0]['price']
        quantities = request.POST.get('quantity')
        cost = float(price) * int(quantities)
        products = Product.objects.filter(status = 1).all()

        if int(quantities) <= quntity :
            try:
                item = Tempitem.objects.filter(tempname=selected_items, tempsize = selected_size).get()
                item.tempprice = price
                item.tempquntity = quantities
                item.temptotal = cost
                item.save()
            except Tempitem.DoesNotExist:
                item = Tempitem.objects.create(tempname=selected_items,tempsize = selected_size, tempprice=price, tempquntity=quantities, temptotal=cost)

            tempproducts = Tempitem.objects.all()
            total_price = Tempitem.objects.aggregate(total_price=models.Sum('temptotal'))
            context={
                'products': products,
                'bill_items': tempproducts,
                'total_price': total_price,
            }
            return redirect('/', context)
        else:
            messages.warning(request, f'Maxmimum quntity of {selected_items} | {selected_size} item is {quntity}.')
            return redirect('/')

@login_required
def delete(request):
    Tempitem.objects.all().delete()
    CustomerBill.objects.all().delete()
    return redirect('/')

@login_required
def delete_item(request, id):
    if request.method == "POST":
        item = Tempitem.objects.get(id=id)
        item.delete()
        return redirect('/')

@login_required
def create_bill(request):
    items = Tempitem.objects.all()
    if not items:
        messages.warning(request, 'Enter items in  bill.')
        return redirect('/')
    totalitems = Tempitem.objects.aggregate(total=Sum('tempquntity'))
    totalprice = Tempitem.objects.aggregate(total=Sum('temptotal'))
    if request.method == "POST":
        custname = request.POST.get('custname')
        custnumb = request.POST.get('custmobile')
        custemail = request.POST.get('custemail')
        payment = request.POST.get('payment')
        discount = request.POST.get('discount')
        if discount != "":
            discount = float(discount)
        else:
            discount = 0
        percent_discount = request.POST.get('discount_percentage')
        if percent_discount != "":
            percent_discount = float(percent_discount)
        else:
            percent_discount = 0
        payprice = int(totalprice['total'] - discount)
        if custname == '' or custnumb == '':
            messages.warning(request, 'Enter the Customer Details.')
            return redirect('/')
        if len(custnumb) != 10:
            messages.warning(request, 'Enter the Customers Number Properly.')
            return redirect('/')

    pref = datetime.today().strftime('%Y%m%d')
    date = datetime.today()
    last_bill = CustomerBill.objects.order_by('-itemcode').first()
    last_transactional_code = last_bill.itemcode if last_bill else ''
    last_date = int(last_transactional_code[:8]) if last_transactional_code else 0
    last_sequence = int(last_transactional_code[-4:]) + 1 if last_transactional_code else 1
    if last_date == int(pref):
        transactionalcode = pref + str(last_sequence).zfill(4)
    else:
        transactionalcode = pref + "0001"

    for item in items:
        bill = invoiceitem()
        bill.itemname = item.tempname
        bill.itemsize = item.tempsize
        bill.itemprice = item.tempprice
        bill.itemquntity = item.tempquntity
        bill.itemtotal = item.temptotal
        bill.itemcode = transactionalcode
        bill.save()

    for item in items:
        bill = stockhistory()
        bill.itemname = item.tempname
        bill.itemsize = item.tempsize
        bill.itemquntity = item.tempquntity
        bill.status = 2
        bill.save()

    for item in items:
        update_product_quantity(item.tempname, item.tempsize , item.tempquntity)

    CustomerBill.objects.create(custname=custname, custnumb=custnumb, custemail = custemail, totalitem =totalitems['total'], totalprice=totalprice['total'], itemcode = transactionalcode, payment=payment, discount=discount, per_discount=percent_discount, payprice = payprice)
    Tempitem.objects.all().delete()
    data = invoiceitem.objects.filter(itemcode=transactionalcode)
    context = {'custname': custname, 'custnumb': custnumb, 'custemail': custemail, 'totalprice': totalprice, 'totalitem': totalitems, 'itemcode': transactionalcode, 'data': data, 'date': date, 'payment': payment, 'discount': discount, 'per_discount': percent_discount, 'payprice': payprice}
    if custemail:
        subject = 'Your Bill'
        message = 'Thank you! For Purchasing From Neon Wholesale Management System.'
        from_email = 'neonwholesalesystem@gmail.com'  
        recipient_list = [custemail]

        # Render the bill as a PDF (you might need to adjust this part based on your implementation)
        rendered_bill = render_to_string('pdf.html', context)

        # Send the email with the bill as an attachment (you might need to adjust this part based on your implementation)
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=rendered_bill)
    return render(request, 'pdf.html', context)

@login_required
def pdf(request):
    slr = CustomerBill.objects.last()
    return render(request,'pdf.html',{'seller':slr})

@login_required
def viewpdf(request, code):
    data = CustomerBill.objects.filter(itemcode=code)
    item = invoiceitem.objects.filter(itemcode=code)
    context = {'data':data, 'item':item}
    return render(request,'viewpdf.html',context)

def update_product_quantity(itemname,itemsize, itemquntity):
    product = get_object_or_404(Product, name=itemname, size=itemsize)
    product.totalquantity -= itemquntity
    product.save()

@login_required
def product(request):
    product = AddProduct()
    context = {'form':product}
    return render(request, 'product.html',context)

@login_required
def save_product(request):
    if request.method == "POST":
        form = AddProduct(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['name']
            product_size = form.cleaned_data['size']
            if not Product.objects.filter(name=product_name, size=product_size).exists():
                form.save()
                messages.success(request, 'Product saved successfully.')
            else:
                messages.warning(request, 'Product with the same name and size already exists.')
        return redirect('/product/')

@login_required
def view_product(request):
    product = Product.objects.order_by('id')
    myfilter = ProductFilter(request.GET, queryset=product)
    product = myfilter.qs
    paginator = Paginator(product, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {"product": products, 'form': EditProduct(), 'filter': myfilter}
    return render(request, 'view_product.html', context)

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product = Product.objects.get(name= product.name, size= product.size)
        form = EditProduct(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Updated Successfully.')
            return redirect('/viewproduct/')
    else:
        product = Product.objects.get(name= product.name, size= product.size)
        form = EditProduct(instance=product)
    return render(request, 'editproduct.html',{'form': form})

@login_required
def delete_product(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        messages.success(request, 'Product Deleted Successfully.')
    return redirect('/viewproduct/')

@login_required
def show_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    stock = stockhistory.objects.filter(itemname=product.name, itemsize = product.size)
    stock = stock.order_by('-id')
    paginator = Paginator(stock, 10)
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    if stock:
        context = {'product': product, 'stocks': stocks}
    else:
        context = {'product': product}
    return render(request, 'showproduct.html', context)

@login_required
def add_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    total = product.totalquantity

    if request.method == "POST":
        quantity = request.POST.get('quntity')
        if quantity is not None and quantity.isdigit():  # Check if quantity is not None and is a digit
            quantity = int(quantity)
            total += quantity
            product.totalquantity = total
            product.save()

            new_stock = stockhistory(itemname=product.name, itemsize=product.size, itemquntity=quantity, status=1)
            new_stock.save()

            messages.success(request, 'Stock added successfully.')
        else:
            messages.error(request, 'Invalid quantity value.')

    return redirect('/viewproduct/')

@login_required
def delete_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    total = product.totalquantity

    if request.method == "POST":
        quantity = request.POST.get('quntity')
        if quantity is not None and quantity.isdigit(): 
            quantity = int(quantity)
            if quantity <= total:
                total -= quantity
                product.totalquantity = total
                product.save()

                new_stock = stockhistory(itemname=product.name, itemsize=product.size, itemquntity=quantity, status=2)
                new_stock.save()

                messages.success(request, 'Stock removed successfully.')
            else:
                messages.error(request, 'Insufficient stock to remove.')
        else:
            messages.error(request, 'Invalid quantity value.')

    return redirect('/viewproduct/')

@login_required
def customer(request):
    customer = CustomerBill.objects.order_by('-id')
    myfilter = CustomerFilter(request.GET, queryset=customer)
    customer = myfilter.qs
    paginator = Paginator(customer, 10)
    page = request.GET.get('page')
    customer = paginator.get_page(page)
    context = {'customer':customer, 'form': EditCustomer(), 'filter':myfilter}
    return render(request, 'customer.html', context)

@login_required
def edit_customer(request, code):
    customer = CustomerBill.objects.get(itemcode = code)
    if request.method == "POST":
        customer = CustomerBill.objects.get(itemcode = code)
        form = EditCustomer(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer Updated Successfully.')
            return redirect('/customer/')
    else:
        customer = CustomerBill.objects.get(itemcode = code)
        form = EditCustomer(instance=customer)
    return render(request, 'editcustomer.html',{'form': form})
