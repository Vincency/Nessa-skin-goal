# class CheckoutView(View):
#   def get(self, request, *args, **kwargs):
#     try:
#       order = Order.objects.get(user=self.request.user, ordered=False)
#       form = CheckoutForm()
#       shipping_address_qs = Address.objects.filter(
#           user=self.request.user,
#           address_type='S',
#           default=True
#       )
#       billing_address_qs = Address.objects.filter(
#           user=self.request.user,
#           address_type='B',
#           default=True
#       )
#       context = {
#           'form': form,
#           'order': order,
#           'has_shipping_address': shipping_address_qs.exists(),
#           'has_billing_address': billing_address_qs.exists()
#       }
#       return render(self.request, "checkout.html", context)
#     except ObjectDoesNotExist:
#       messages.info(self.request, "You do not have an active order")
#       return redirect("core:order-summary")  # Redirect to order summary page

#   def post(self, request, *args, **kwargs):
#     form = CheckoutForm(self.request.POST or None)
#     try:
#       order = Order.objects.get(user=self.request.user, ordered=False)
#       if form.is_valid():
#         # Shipping address handling
#         use_default_shipping = form.cleaned_data.get('use_default_shipping')
#         if use_default_shipping:
#           shipping_address_qs = Address.objects.filter(
#               user=self.request.user,
#               address_type='S',
#               default=True
#           )
#           if not shipping_address_qs.exists():
#             messages.error(self.request, "No default shipping address available. Please enter a shipping address.")
#             return redirect('core:checkout')  # Redirect back to checkout
#           if shipping_address_qs.exists():
#             shipping_address = shipping_address_qs[0]
#             order.shipping_address = shipping_address
#             order.save()
#           else:
#             messages.info(self.request, "No default shipping address available")
#             return redirect('core:checkout')  # Redirect back to checkout
#         else:
#           shipping_address = form.cleaned_data.get('shipping_address')
#           # New validation check for shipping_address
#           if shipping_address:
#             # Proceed with creating the Address object
#             new_address = Address.objects.create(
#                 user=self.request.user,
#                 street_address=shipping_address,
#                 apartment_address=form.cleaned_data.get('apartment_address'),
#                 country=form.cleaned_data.get('country'),
#                 zip=form.cleaned_data.get('zip'),
#                 address_type='S'
#             )
#             set_default_shipping = form.cleaned_data.get('set_default_shipping')
#             if set_default_shipping:
#               new_address.default = True
#               new_address.save()
#             order.shipping_address = new_address
#             order.save()
#           else:
#             messages.error(self.request, "Please enter a shipping address.")
#             return redirect('core:checkout')  # Redirect back to checkout
#         # ... (rest of your code for billing address and payment processing)
#     except ObjectDoesNotExist:
#       messages.warning(self.request, "You do not have an active order")
#       return redirect("core:order-summary")

        

