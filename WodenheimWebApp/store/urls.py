from django.urls import path, include
from . import views
"""
urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkoout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('welcome/', views.welcome, name='welcome'),
]
"""


urlpatterns = [
    path('', views.welcome, name="welcome"),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkoout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.singout, name="logout"),
    path('signin/', views.signin, name="signin"),
    path('create-paypal-order', views.create_paypal_order_view, name='create_paypal_order'),
    path('capture-paypal-order', views.capture_paypal_order_view, name='capture_paypal_order'),
]

