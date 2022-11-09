from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.http import HttpResponse
from django.shortcuts import redirect
from .decorators import unauthenticated_user, allowed_users, admin_only



	


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:

        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)
                return redirect('login')
            

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
        if request.user.is_authenticated:
         return redirect('dashboard')
        else:

            if request.method == 'POST':
                username = request.POST.get('username')
                password =request.POST.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    messages.info(request, 'Username OR password is incorrect')

            context = {}
            return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url="login")
@admin_only
def dashboard(request):
    orders=Order.objects.all()
    o_count=orders.count()
    customer=Customer.objects.all()
    orders_delivered=orders.filter(status="Delivered").count()
    orders_pending=orders.filter(status="Pending").count()
    myfilter=OrderFilter(request.GET,queryset=orders)
    orders=myfilter.qs
    context={
        'o_count':o_count,
        'myfilter':myfilter,
       'orders':orders,
       'customer':customer,
       'orders_delivered':orders_delivered,
       'orders_pending':orders_pending
    }
    return render(request,'dashboard.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def customer_pages(request,pk):
    customer=Customer.objects.get(id=pk)
    order=customer.order_set.all()
    myfilter=OrderFilter(request.GET,queryset=order)
    order=myfilter.qs
    orders_count=order.count()
    context={
        'customer':customer,
        'myfilter':myfilter,
        'orders':order,
        'orders_count':orders_count
    }
    return render(request,'customer.html',context)    

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def create_order(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('dashboard')

	context = {'form':formset}
	return render(request, 'order_form.html', context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form':form}
    return render(request,'order_form.html',context)
    
@login_required(login_url="login")
@allowed_users(allowed_roles=['admin'])
def delete_item(request,pk):
    order=Order.objects.get(id=pk)
    context={'item':order}
    if request.method=="POST":
        order.delete()
        return redirect('dashboard')
    return render(request,'delete.html',context)  

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def customer_page(request):
    cus_order=request.user.customer.order_set.all()
    context={
        'ord':cus_order
    }
    return render(request,'user.html',context)

@login_required(login_url="login")
@allowed_users(allowed_roles=['customer'])
def cus_settings(request):
    user=request.user.customer
    form=CustomerForm(instance=user)
    if request.method=="POST":
        form=CustomerForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('settings')         
    context={
        'form':form
    }
    return render(request,'setings.html',context)