from django.urls import path
from . import views

urlpatterns = [
    path('',views.log_in),
    path('sign_up',views.sign_up),
    path('log_in',views.relogin),
    path('signup',views.signup),
    path('home',views.home),
    path('login',views.login),
    path('log_out',views.log_out),
    path('inventory',views.show_inventory),
    path('go_to_add_products',views.go_to_add_products),
    path('add_product',views.add_product),
    path('delete/<int:id_porduct>',views.delete_product),
    path('edit/<int:id_porduct>',views.showedit_product),
    path('edit_product/<int:id_porduct>',views.edit_product),
    path('information/<int:id_product>',views.info_product),
    path('add_quntity/<int:all_products_id>',views.add_quntity),
    path('order/<int:user_id>',views.go_to_add_order),
    path('add_order/<int:userid>',views.add_order),
    path('show_list_order',views.show_list_order),
    path('catogery',views.catogrey),
    path('add_category',views.addcatogrey),
    path('delete_order/<int:id_ord>',views.delete_order),
    
]
