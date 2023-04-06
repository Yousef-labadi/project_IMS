from django.db import models
import re
import bcrypt
from datetime import datetime, date


class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) <= 0:
            errors["first_name"] = "Must enter a first name!"
        elif len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters!"
        if len(postData['last_name']) <= 0:
            errors["last_name"] = "Must enter a last name!"
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters!"
        if len(postData['pwd']) <= 0:
            errors["pwd"] = "Password is required!"
        if len(postData['pwd']) < 8:
            errors['pwd'] = "Password must be at least 8 characters!"
        EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="invalid email address!"
        if len(postData['email']) <= 0:
            errors["email"] = "Email is required!"
        if User.objects.filter(email = postData['email']).exists():
            errors['email'] = "Email already exists."
    
        if postData['cpwd'] != postData['pwd']:
            errors['cpwd'] = "Confirmation password does not match password!"
        return errors
    
    def log_validation(self, postData):
        errors = {}
        try:
            user = User.objects.get(email = postData['email'])
        except:
            errors['email'] = "Invalid Inputs"
            return errors
        if not bcrypt.checkpw(postData['pwd'].encode(), user.password.encode()):
            errors['pwd'] = "Invalid Inputs"
        return errors
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if   postData.get('p_name')== None or postData.get('p_name') == '' :
            errors["p_name"] = "product name cant be empty"
        elif len(postData.get('p_name')) < 2:
            errors["p_name"] = "priduct name shoud be at least 2 char"
        if 'p_name' not in postData or postData['p_name'] == '':
            errors['price'] = 'price name is required.'
        if 'price' not in postData or postData['price'] == '':
            errors['price'] = 'price is required.'
        elif int(postData['price']) < 0:
            errors['price'] = 'price must be more than zero'
        if 'quantity' not in postData or postData['quantity'] == '':
            errors['quantity'] = 'quantity is required.'
        elif int(postData['quantity']) < 0:
            errors['quantity'] = 'quantity must be more than zero.'
        if 'desc' in postData and len(postData['desc']) <= 0:
            errors['desc']='desc is required'

        if 'desc' in postData and len(postData['desc']) <= 0:
            errors['desc']='desc is required'
        return errors
class ordertManager(models.Manager):
    def order_validator(self, postData):
        errors = {}
        if   postData.get('name_customer')== None or postData.get('name_customer') == '' :
            errors["name_customer"] = "customer name cant be empty"
        elif len(postData.get('name_customer')) < 2:
            errors["name_customer"] = "customer name shoud be at least 2 char"
        if   postData.get('loc')== None or postData.get('loc') == '' :
            errors["loc"] = "location name cant be empty"
        elif len(postData.get('name_customer')) < 2:
            errors["loc"] = "location name shoud be at least 2 char"
        
        if 'quantity' not in postData or postData['quantity'] == '':
            errors['quantity'] = 'quantity is required.'
        elif int(postData['quantity']) < 0:
            errors['quantity'] = 'quantity must be more than zero.'
        if 'product' in postData and len(postData['product']) <= 0:
            errors['product']='product is required'
        order_date_str = postData['order_date']
        if order_date_str:
            order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
            if order_date < date.today():
                errors['order_date'] = "Order date cannot be in the past."
        else:
            errors['order_date'] = "Order date is required."
        
        
        if 'loc' in postData and len(postData['loc']) <= 0:
            errors['loc']='location is required'
        return errors
            
        
class Catogrey(models.Model):
    type=models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    
class Product(models.Model):
    name=models.TextField()
    price=models.FloatField()
    quantity=models.FloatField()
    description=models.TextField()
    categoies=models.ManyToManyField(Catogrey,related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=ProductManager()
    
class Order(models.Model):
    user = models.ForeignKey(User,related_name="orders_made",on_delete=models.CASCADE)
    product = models.ManyToManyField(Product,related_name='ordered_products')
    order_date = models.DateField()
    customer_name = models.CharField(max_length=255)
    location = models.CharField(max_length=45)
    quantity_order=models.FloatField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=ordertManager()
    