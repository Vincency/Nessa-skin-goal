from django.urls import path
from .views import (
    About,
    Contact,
    Cart,
    user_login,
    signup,
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    # PaymentView,
    AddCouponView,
    RequestRefundView,

    initiate_payment,
    payment_callback,

    verify_payment
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', About, name='about'),
    path('contact/', Contact, name='contact'),
    path('login/',user_login, name='login'),
    path('signup/', signup, name='signup'),
    
    path('cart/', Cart, name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),

    # path('product/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),

    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart, name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),

    path('initiate_payment/', initiate_payment, name='initiate_payment'),
    path('payment_callback/', payment_callback, name='payment_callback'),
    
    path('verify-payment/<str:ref>', verify_payment, name='verify-payment')
]
