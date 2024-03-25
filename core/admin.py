from django.contrib import admin

from .models import Item, Category, OrderItem, Order, Payment, Coupon, Refund, Address, UserProfile

from .forms import CheckoutForm



# def make_refund_accepted(modeladmin, request, queryset):
#     queryset.update(refund_requested=False, refund_granted=True)


# make_refund_accepted.short_description = 'Update orders to refund granted'


# class OrderAdmin(admin.ModelAdmin):
#     list_display = [
#         'user',
#         'ordered',
#         'being_delivered',
#         'received',
#         'refund_requested',
#         'refund_granted',
#         'shipping_address',
#         'billing_address',
#         'payment',
#         'coupon'
#     ]
    
#     list_display_links = [
#         'user',
#         'shipping_address',
#         'billing_address',
#         'payment',
#         'coupon'
#     ]

#     list_filter = [
#         'ordered',
#         'being_delivered',
#         'received',
#         'refund_requested',
#         'refund_granted'
#     ]
   
    # search_fields = [
    #     'user__username',
    #     'ref_code'
    # ]
    # actions = [make_refund_accepted]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        # 'state',
        'delivery_address',
        'country',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'delivery_address']


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
                    # , OrderAdmin)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Address, AddressAdmin)
admin.site.register(UserProfile)
admin.site.register(Category)
