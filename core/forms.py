from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

# from .fields import NigerianStateField
from phonenumber_field.formfields import PhoneNumberField


PAYMENT_CHOICES = (
    ('PS', 'paystack'),
    ('P', 'PayPal')
)





class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
     widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

     # Remove default help text for password fields
        self.fields['email'].help_text = ''
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        # Perform custom password validation
        if len(password1) < 8:
            raise forms.ValidationError("Your password must contain at least 8 characters.")
        if password1.isdigit():
            raise forms.ValidationError("Your password can’t be entirely numeric.")
        return password1

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')

        # Check if passwords match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2


    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Add custom username validation here if needed
        if not re.match(r'^\w+$', username):
            raise forms.ValidationError("Username can only contain letters, digits, and underscores.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Add custom email validation here if needed
        if not re.match(r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$', email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'input-field','placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field','placeholder': 'Password'}))






# class CheckoutForm(forms.Form):
#     shipping_address = forms.CharField(required=False)
#     shipping_address2 = forms.CharField(required=False)
#     shipping_country = CountryField(blank_label='(select country)').formfield(
#         required=False,
#         widget=CountrySelectWidget(attrs={
#             'class': 'custom-select d-block w-100',
#         }))
#     shipping_zip = forms.CharField(required=False)

#     billing_address = forms.CharField(required=False)
#     billing_address2 = forms.CharField(required=False)
#     billing_country = CountryField(blank_label='(select country)').formfield(
#         required=False,
#         widget=CountrySelectWidget(attrs={
#             'class': 'custom-select d-block w-100',
#         }))
#     billing_zip = forms.CharField(required=False)

#     same_billing_address = forms.BooleanField(required=False)
#     set_default_shipping = forms.BooleanField(required=False)
#     use_default_shipping = forms.BooleanField(required=False)
#     set_default_billing = forms.BooleanField(required=False)
#     use_default_billing = forms.BooleanField(required=False)

#     payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'No 23 Main Street'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'country-form'
    }))
    # state = NigerianStateField()

    phone_number = PhoneNumberField()

    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)









class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'coupon-input',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()


class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
    save = forms.BooleanField(required=False)
    use_default = forms.BooleanField(required=False)
