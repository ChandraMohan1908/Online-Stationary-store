from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from django.db.models import Count, Q
from django.template.loader import render_to_string, get_template
from io import BytesIO
from xhtml2pdf import pisa
import os

from django.core.mail import send_mail
from .models import (
    Cart, Customer, Payment, Orderplaced, Product, Wishlist, Review, ContactMessage, CATEGORY_CHOICES
)
from .forms import (
    CustomerRegistrationForm, CustomerProfileForm, PasswordChangeForm,
    ProductForm, CustomerForm, CartForm, PaymentForm, OrderplacedForm, ReviewForm, ContactForm
)
from django.views import View
from django.contrib.admin.sites import site



# Create your views here.

def home(request):
    totalitem=0
    wishlist=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request, "app/home.html",locals())

def payment_success(request):
    # Render the payment success page
    return render(request, 'app/payment_success.html')


class CategoryView(View):  
    def get(self, request, val):
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
              totalitem=len(Cart.objects.filter(user=request.user))
              wishlist=len(Wishlist.objects.filter(user=request.user))
        # Filter products based on the category slug
        products = Product.objects.filter(category=val)
        # Pass products to the template as context
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/Category.html",locals()) 

def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    reviews = product.reviews.all()  # Assuming reviews are a related field
    review_form = ReviewForm()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
        return redirect('product-detail', product_id=pk)

    return render(request, 'app/productdetail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
    })

class CategoryTitle(View):
    def get(self,request,val):
        products = Product.objects.filter(title=val)
        title = Product.objects.filter(category=products[0].category).values('title')
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user)) 
          wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/Category.html",locals()) 

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
           wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
           wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcod']

            # Always create a new Customer instance
            Customer.objects.create(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcod=zipcode,
            )
            messages.success(request, "New address saved successfully.")
            return redirect('address')  
            
        else:
            messages.warning(request, "Invalid input data.")
        
        return render(request, 'app/profile.html',locals()) 

# to view the address filter user name 
def address(request):
    add =Customer.objects.filter(user=request.user)
    
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        wishlist=len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html',locals()) 

#update address
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem=0
        wishlist=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
           wishlist=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', locals()) 

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            # Corrected 'Cleaned_data' to 'cleaned_data'
            add.name = form.cleaned_data['name']  
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcod = form.cleaned_data['zipcod']
            add.save()
            messages.success(request, 'Congratulations! Profile Updated Successfully')
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('address')


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id) 
    Cart(user=user, product=product).save()
    return redirect("/cart")


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0

    # Calculate the total amount for the items in the cart
    for p in cart:
        value= p.quantity * p.product.discounted_price
        amount = amount+value
        totalamount=amount+40
        totalitem=0
        if request.user.is_authenticated:
           totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals()) 

class checkout(View):
    def get(self, request):
        user = request.user
        print(user)
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        totalitem=0
        if request.user.is_authenticated:
          totalitem=len(Cart.objects.filter(user=request.user))
        famount = 0
        id = 0
        
        for p in cart_items:
            value = p.quantity * p.product.discounted_price  # Accessing discounted_price from the product
            famount += value
            id = p.id
        
            
        totalamount = famount + 40

        pay = Payment(amount = totalamount, razorpay_order_id = "nothing", razorpay_payment_status = "Accepted", razorpay_payment_id = "nothing", paid = 1, user_id = 1)
        pay.save()

        ors = Orderplaced(quantity = totalitem, status = "Accepted", product_id = id, customer_id = 1, user_id = 1, payment_id = Payment.objects.latest('id').id)

        ors.save()

        

        return render(request, 'app/payment_success.html', locals())

from .models import Orderplaced  # Ensure this is imported correctly

def orders(request):
    totalitem = 0
    wishlist = 0
    order_placed = []

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishlist = Wishlist.objects.filter(user=request.user).count()
        # Retrieve orders for the current user
        order_placed = Orderplaced.objects.filter(user=request.user).order_by('-ordered_date')
        
    return render(request, 'app/orders.html', {
        'order_placed': order_placed,
        'totalitem': totalitem,
        'wishlist': wishlist
    })


def download_invoice(request, order_id):
    try:
        order = Orderplaced.objects.get(id=order_id, user=request.user, status="Delivered")
    except Orderplaced.DoesNotExist:
        return HttpResponse('Order not found or not delivered.')

    # Define the template and context for generating the invoice
    template_path = 'app/invoice_template.html'
    context = {'order': order}

    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    template = get_template(template_path)
    html = template.render(context)

    # Generate the PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)  # Move to the beginning of the buffer

    if pisa_status.err:
        return HttpResponse('We had some errors while generating the PDF.')

    # Return the PDF response to the user
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'  # To download the file
    return response




#ADMIN

class CustomAdminView(View):
    def get(self, request, *args, **kwargs):
        # Only show this page to staff users
        if not request.user.is_staff:
            return render(request, 'error.html', {'message': 'Unauthorized access'})

        # Aggregate data for pie charts
        order_counts = Orderplaced.objects.values('status').annotate(count=Count('status'))
        user_count = Customer.objects.count()
        product_count = Product.objects.count()

        context = {
            'admin_site': site,
            'products': Product.objects.all(),
            'customers': Customer.objects.all(),
            'cart_items': Cart.objects.all(),
            'payments': Payment.objects.all(),
            'orders': Orderplaced.objects.all(),
            'wishlists': Wishlist.objects.all(),
            'order_counts': list(order_counts) if order_counts else [{'status': 'No Orders', 'count': 0}],
            'user_count': user_count,
            'product_count': product_count,
        }
        return render(request, 'app/custom_admin.html', context)
    
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.quantity += 1
            c.save()  

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  

            # Debugging logs
            print(f"Amount: {amount}, Total Amount: {totalamount}")

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.quantity -= 1
            c.save()  

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  

            # Debugging logs
            print(f"Amount: {amount}, Total Amount: {totalamount}")

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse(data)



def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        try:
            c = Cart.objects.get(Q(product_id=prod_id) & Q(user=request.user))
            c.delete()  

            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(item.quantity * item.product.discounted_price for item in cart)
            totalamount = amount + 40  # Add shipping cost

            # Debugging logs
            print(f"Amount: {amount}, Total Amount: {totalamount}")

            data = {
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)
        except Cart.DoesNotExist:
            return JsonResponse(data)
        
    

# Include this function if not already present
def home(request):
    wishitem = Wishlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
    return render(request, 'app/home.html', {'wishitem': wishitem})

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product_instance = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.get_or_create(user=user, product=product_instance)
        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product_instance = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product_instance).delete()
        data = {
            'message': 'Wishlist Removed Successfully',
        }
        return JsonResponse(data)

@login_required      
def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'app/wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return render(request, 'app/wishlist.html', {'wishlist_items': []})
        

def search(request):
    query = request.GET.get('search', '')  # Get search term from request
    totalitem = 0
    wishitem = 0

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()

    # Filter products based on the search query
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'app/search.html', {
        'products': products,
        'totalitem': totalitem,
        'wishitem': wishitem,
    })

# Product views
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')

# Customer views
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin/customer_list.html', {'customers': customers})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'admin/customer_form.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'admin/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    return redirect('customer_list')

# Cart Views
def cart_list(request):
    carts = Cart.objects.all()
    return render(request, 'admin/cart_list.html', {'carts': carts})

def cart_add(request):
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cart_list')
    else:
        form = CartForm()
    return render(request, 'admin/cart_management.html', {'form': form})

def cart_edit(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST, instance=cart)
        if form.is_valid():
            form.save()
            return redirect('cart_list')
    else:
        form = CartForm(instance=cart)
    return render(request, 'admin/cart_management.html', {'form': form})

def cart_delete(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    cart.delete()
    return redirect('cart_list')  # Redirect back to the cart list

# Order Placed Views
def order_list(request):
    orders = Orderplaced.objects.all()
    return render(request, 'admin/order_list.html', {'orders': orders})

def order_add(request):
    if request.method == 'POST':
        form = OrderplacedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderplacedForm()
    return render(request, 'admin/order_management.html', {'form': form})

def order_edit(request, pk):
    order = get_object_or_404(Orderplaced, pk=pk)
    if request.method == 'POST':
        form = OrderplacedForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderplacedForm(instance=order)
    return render(request, 'admin/order_management.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(order, pk=pk)
    order.delete()
    return redirect('order_list')  # Redirect back to the order list

# Payment Views
def payment_list(request):
    payments = Payment.objects.all()
    return render(request, 'admin/payment_list.html', {'payments': payments})

def payment_add(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'admin/payment_management.html', {'form': form})

def payment_edit(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'admin/payment_management.html', {'form': form})

def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    return redirect('payment_list')  # Redirect back to the payment list



def dashboard_view(request):
    # Map abbreviations to full names for categories
    category_dict = dict(CATEGORY_CHOICES)
    
    # Products data by category with full names
    products_data = Product.objects.values('category').annotate(total=Count('id'))
    products_chart_data = {
        'labels': [category_dict[entry['category']] for entry in products_data],  # Use full names
        'values': [entry['total'] for entry in products_data]
    }

    # Orders data by status
    orders_data = Orderplaced.objects.values('status').annotate(total=Count('id'))
    orders_chart_data = {
        'labels': [entry['status'] for entry in orders_data],
        'values': [entry['total'] for entry in orders_data]
    }

    # Customers data by state
    customers_data = Customer.objects.values('state').annotate(total=Count('id'))
    customers_chart_data = {
        'labels': [entry['state'] for entry in customers_data],
        'values': [entry['total'] for entry in customers_data]
    }

    # Payments data by status
    payments_data = Payment.objects.values('status').annotate(total=Count('id'))
    payments_chart_data = {
        'labels': [entry['status'] for entry in payments_data],
        'values': [entry['total'] for entry in payments_data]
    }

    context = {
        'products_data': products_chart_data,
        'orders_data': orders_chart_data,
        'customers_data': customers_chart_data,
        'payments_data': payments_chart_data,
    }
    
    return render(request, 'admin/dashboard.html', context)




@login_required
def place_order(request):
    # Get the current user
    user = request.user

    # Retrieve the cart items for the current user
    cart_items = Cart.objects.filter(user=user)
    
    # Check if the cart is empty
    if not cart_items.exists():
        return redirect('show_cart')  # Redirect if the cart is empty

    # Retrieve the associated customer instance
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        return redirect('profile')  # Redirect to profile if customer details are missing

    # Calculate the total amount for the payment
    total_amount = sum(item.quantity * item.product.discounted_price for item in cart_items)

    # Create a new payment record for the order
    payment = Payment.objects.create(
        user=user,
        amount=total_amount,
        status='Completed',  # Update status as needed
        date=timezone.now()
    )

    # Collect order details to include in the email
    product_details = ""
    for item in cart_items:
        # Create each order entry
        Orderplaced.objects.create(
            user=user,
            customer=customer,
            product=item.product,
            quantity=item.quantity,
            payment=payment,
            ordered_date=timezone.now(),
            status='Accepted'
        )
        # Append product details to the email content
        product_details += f"{item.product.title} (Quantity: {item.quantity})\n"
    
    # Clear the user's cart after placing the order
    cart_items.delete()

    # Construct and send the email
    subject = 'Order Confirmation'  # Email subject
    message = (
        f"Dear {user.username},\n\n"
        f"Your order has been placed successfully with the following details:\n\n"
        f"Products:\n{product_details}\n"
        f"Total Amount: Rs. {total_amount}\n\n"
        f"Thank you for shopping with us!\n\nBest regards,\nYour Eshop Team"
    )
    email_from = 'chandruganesan19@gmail.com'  # Replace with your sender email address
    recipient_list = [user.email]  # User’s email from their profile

    # Send the email
    send_mail(subject, message, email_from, recipient_list)

    # Redirect to the orders page after processing and email sending
    return redirect('orders')


def orders(request):
    totalitem = 0
    wishlist = 0
    order_placed = []

    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishlist = Wishlist.objects.filter(user=request.user).count()
        order_placed = Orderplaced.objects.filter(user=request.user).order_by('-ordered_date')

    return render(request, 'app/orders.html', {
        'order_placed': order_placed,
        'totalitem': totalitem,
        'wishlist': wishlist
    })


def send_contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            user_email = request.user.email  # logged-in user's email
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = user_email  # Sender email
            recipient_list = ['chandruganesan19@gmail.com']  # Admin email

            # Send email
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False
            )
            return redirect('send_contact_email')  # Redirect to a success page

    else:
        form = ContactForm()

    return render(request, 'app/contact_form.html', {'form': form})