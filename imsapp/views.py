from django.shortcuts import render,redirect
from imsapp.models import *
from django.contrib import messages

def log_in(request):
    return render(request,'login.html')
def relogin(request):
    return redirect('/')
def login(request):
    errors = User.objects.log_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])

    if user:
        if bcrypt.checkpw(request.POST['pwd'].encode(), user[0].password.encode()):
            request.session['user']=user[0].id

            return redirect('/home')
def sign_up(request):
    
    return render(request,'register.html')
def signup(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/sign_up')
    else:
        password = request.POST['pwd']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user=User.objects.create(first_name=request.POST['first_name'],
                            last_name=request.POST['last_name'],
                            email=request.POST['email'],
                            password=pw_hash)
        request.session['user']=user.id
        return redirect('/home')
def home(request):
        if 'user'not in request.session:
            return redirect('/')
        data={
        'user':User.objects.all(),
        'userid':User.objects.get(id=request.session['user']),
        }
        return render(request,'home.html',data)
def log_out(request):
    request.session.clear()
    return redirect('/')
def show_inventory(request):
    if 'user' not in request.session:
        return redirect('/log_out')
    data={
        'userid':User.objects.get(id=request.session['user']),
        'product':Product.objects.all(),
        
        
    }
    return render(request,'inventory.html',data)
def go_to_add_products(request):
    if 'user' not in request.session:
        return redirect('/log_out')
    data={
        'c':Catogrey.objects.all(),
        'user':User.objects.get(id=request.session['user'])
    }
    return render(request,'addproduct.html',data)
def add_product(request):
    if 'user' not in request.session:
        return redirect('/log_out')
    
    errors = Product.objects.product_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/go_to_add_products')
    else:
        pr_name=request.POST['p_name']
        price=float(request.POST['price'])
        quantity=float(request.POST['quantity'])
        desc=request.POST['desc']
        this_category=Catogrey.objects.get(type=request.POST['category'])
        this_product=Product.objects.create(name=pr_name,
                        price=price,
                        quantity=quantity,
                        description=desc
                        )
    this_product.categoies.add(this_category)
    return redirect('/inventory')
    
    
def delete_product(request,id_porduct):
    if 'user' not in request.session:
        return redirect('/log_out')
    this_product=Product.objects.get(id=id_porduct)
    this_product.delete()
    return redirect ('/inventory')   
def showedit_product(request,id_porduct):
    if 'user' not in request.session:
        return redirect('/log_out')
    
    data={
        'product':Product.objects.get(id=id_porduct),
        'c':Catogrey.objects.all()
    }
    return render(request,'edit.html',data)
def edit_product(request,id_porduct):
    if 'user' not in request.session:
        return redirect('/log_out')
    edit_name=request.POST['p_name']
    edit_price=request.POST['price']
    edit_quantity=request.POST['quantity']
    edit_desc=request.POST['desc']
    this_product=Product.objects.get(id=id_porduct)
    this_product.name=edit_name
    this_product.price=edit_price
    this_product.quantity=edit_quantity
    this_product.description=edit_desc
    this_product.save()
    return redirect('/inventory')
def info_product(request,id_product):
    if 'user' not in request.session:
        return redirect('/log_out')
    product_data={
        'all_products':Product.objects.get(id=id_product),
        'userid':User.objects.get(id=request.session['user']),
        
        
    }
    return render(request,'details.html',product_data)
def add_quntity(request,all_products_id):
    if 'user' not in request.session:
        return redirect('/log_out')
    sum =request.POST['quntity']
    num=Product.objects.get(id=all_products_id)
    
    num.quantity=float(sum)+num.quantity
    num.save()
    return redirect('/inventory')
def go_to_add_order(request,user_id):
    if 'user' not in request.session:
        return redirect('/log_out')
    data={
        'product':Product.objects.all(),
        'user':User.objects.get(id=user_id)
    }
    return render(request,'add_order.html',data)
def add_order(request,userid):
    
    if 'user' not in request.session:
        return redirect('/log_out')
    if 'user' not in request.session:
        return redirect('/log_out')
    
    errors = Order.objects.order_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/order/'+str(userid))
    else:
        id=User.objects.get(id=userid)
    # product_1=Product.objects.get(id=request.POST['product_id'])
        this_product=request.POST['product']
        this_quantity=request.POST['quantity']
        date=request.POST['order_date']
        loc=request.POST['loc']
        customer=request.POST['name_customer']
        new_order=Order.objects.create(user=id,order_date=date,
                                location=loc,
                                customer_name=customer,
                                quantity_order=this_quantity)
    new_order.product.add(this_product)
    # pro=product_1.quantity
    # pro=pro - int(this_quantity)
    # request.session['pro_qun']=pro
    
    data={
        
       'quantity': this_quantity,
    }
    
    return redirect('/show_list_order',data)
def show_list_order(request):
    if 'user' not in request.session:
        return redirect('/log_out')
    data={
        'order':Order.objects.all().order_by('-order_date'),
        'user':User.objects.get(id=request.session['user']),
        # 'product':Product.objects.all(),
    }
    return render(request,'show_list_order.html',data)
def catogrey(request):
    if 'user' not in request.session:
        return redirect('/log_out')
    return render(request,'category.html')


def addcatogrey(request):
    
    Catogrey.objects.create(
        type = request.POST['type']
    )
    return redirect('/go_to_add_products')  

def delete_order(request,id_ord):
    
    this_order=Order.objects.get(id=id_ord)
    this_order.delete()
    return redirect ('/show_list_order')   