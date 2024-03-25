import random
import string

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View

from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm, SignUpForm, LoginForm
from .models import Item, OrderItem, Order, Payment, Coupon, Refund, UserProfile

from django.contrib.auth import login, authenticate

from django.http import JsonResponse
from paystackapi.paystack import Paystack





def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Cart(request):
    return render(request, 'cart.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the page the user originally intended to access
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/')  # Redirect to home page after successful login
            else:
                # Authentication failed
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})





def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
            }
        return render(self.request, "checkout.html", context)

    def post(self, request, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                print("Form is valid. Data:", form.cleaned_data)  # Print cleaned data for debugging
                
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionality to these fields
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                Payment_option = form.cleaned_data.get('Payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    country = country,
                    zip = zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                print("Form data received:") 
                print(self.request.POST)

                if Payment_option == 'PS':
                    return redirect('core:initiate_payment', Payment_option='paystack')
                elif Payment_option == 'P':
                    return redirect('core:payment', Payment_option='Paypal')
                else:
                    messages.warning(self.request, "invalid payment option selected")
                    return redirect('core:checkout')

        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")

      







def place_order(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            product = Item.objects.get(pk=1)
            var.product = product
            var.user = request.user
            var.total_cost = product.price * var.item_amount
            # var.total_cost = product.price * var.order_item.quantity
            var.save()
            payment = Payment.objects.create(amount=var.total_cost, email=request.user.email, user=request.user)
            payment.save()
            pk = settings.PAYSTACK_PUBLIC_KEY
            context = {
                'total_cost':var.total_cost,
                'item_amount':var.item_amount,
                'payment':payment,
                'paystack_pub_key':pk,
                'amount_value':payment.amount_value()
            }
            request.session['order_id'] = var.id
            return render(request, 'make_payment.html', context)
        else:
            messages.warning(request, 'Error, Something went wrong')
            return redirect('place-order')
    else:
        form = CheckoutForm()
        context = {'form':form}
        return render(request, 'place_order.html', context)





















def verify_payment(self, request, ref):
    payment = Payment.objects.get(ref=ref)
    verified = payment.verify_payment()

    if verified:
        pk = request.session['order_id']
        order = Order.objects.get(pk=pk)
        order.is_verified = True
        order.save()
        context = {'placed_order': pk, 'payment':payment}
        return render(request, 'success.html', context)
    else:
        messages.warning(request, 'sorry your order was not processed. please contact Nessa support.')
        return redirect('/')


















































class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"



def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')  # Assuming you have a form field for amount
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY
        paystackapi = Paystack.Transaction(paystack_secret_key)

        response = paystackapi.initialize(amount=amount, email=request.user.email)  # Assuming you have a user object

        return JsonResponse(response)

    return render(request, 'make_payment.html')




def payment_callback(request):
    if request.method == 'POST':
        paystack_secret_key = settings.PAYSTACK_SECRET_KEY
        paystackapi = Paystack.Transaction(paystack_secret_key)

        # Verify the payment
        response = paystackapi.verify(request.body.decode('utf-8'))

        # Process the payment status
        if response.get('status'):
            payment_status = response.get('data').get('status')

            if payment_status == 'success':
                # Payment successful, process the order or do something else
                return JsonResponse({'status': 'success'})

    # Payment failed or invalid callback, handle accordingly
    return JsonResponse({'status': 'error'})








class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")
        
        

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the current item
        current_item = context['object']
        # Get related items with the same category
        related_items = Item.objects.filter(category=current_item.category).exclude(id=current_item.id)[0:2]
        context['related_items'] = related_items
        return context




@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    
    # Get the user's active order or create a new one if none exists
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs.first()
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, 
            ordered_date=ordered_date
        )

    # Check if the item already exists in the order
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        item=item,
        ordered=False
    )

    # If the item already exists, update its quantity; otherwise, add it to the order
    if not created:
        order_item.quantity += 1
        order_item.save()
        messages.info(request, "This item quantity was updated.")
    else:
        messages.info(request, "This item was added to your cart.")

    return redirect("core:order-summary")




@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        order_item_qs = order.order_items.filter(item=item, ordered=False)
        
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            # Remove the order item from the order
            order_item.delete()
            messages.info(request, f"{item.title} was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart.")
    else:
        messages.info(request, "You do not have an active order.")
        
    return redirect("core:product", slug=slug)





@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        order_item_qs = order.order_items.filter(item=item, ordered=False)
        if order_item_qs.exists():
            order_item = order_item_qs[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()  # Remove the order item from the order
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("core:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request was received.")
                return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")




