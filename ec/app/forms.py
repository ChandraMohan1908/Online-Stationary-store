from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Product, Customer, Cart, Payment, Orderplaced, Review

from . models  import Customer 

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#change password

class MypasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password',widget=forms.PasswordInput(attrs={'autofocus': 'True','autocomplete': 'current-password','class': 'form-control'}))
    new_password1 = forms.CharField(label='New password',widget=forms.PasswordInput(attrs={'autofocus': 'True','autocomplete': 'current-password','class': 'form-control'}))
    new_password2 = forms.CharField(label='Confirm new password',widget=forms.PasswordInput(attrs={'autofocus': 'True','autocomplete': 'current-password','class': 'form-control'}))

# Custom Password Reset Form
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

# Custom Set Password Form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'})
    )


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'zipcod', 'state'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.NumberInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'zipcod': forms.NumberInput(attrs={'class': 'form-control'}),

        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'composition', 'uses', 'category', 'Product_image']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'zipcod', 'state']

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'product', 'quantity']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']

class OrderplacedForm(forms.ModelForm):
    class Meta:
        model = Orderplaced
        fields = ['user', 'customer', 'product', 'quantity', 'status', 'payment']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }