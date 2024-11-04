from django.db import models
from django.contrib.auth.models import User


#create your models
STATE_CHOICES =(
('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
('Andhra Pradesh','Andhra Pradesh'),
('Arunachal Pradesh','Arunachal Pradesh'),
('Assam','Assam'),
('Bihar','Bihar'),
('Chhattisgarh','Chhattisgarh'),
('Goa','Goa'),
('Gujarat','Gujarat'),
('Haryana','Haryana'),
('Himachal Pradesh','Himachal Pradesh'),
('Jharkhand','Jharkhand'),
('Karnataka','Karnataka'),
('Kerala','Kerala'),
('Madhya Pradesh','Madhya Pradesh'),
('Maharashtra','Maharashtra'),
('Manipur','Manipur'),
('Meghalaya','Meghalaya'),
('Mizoram','Mizoram'),
('Nagaland','Nagaland'),
('Odisha','Odisha'),
('Punjab','Punjab'),
('Rajasthan','Rajasthan'),
('Sikkim','Sikkim'),
('Tamil Nadu','Tamil Nadu'),
('Telangana','Telangana'),
('Tripura','Tripura'),
('Uttar Pradesh','Uttar Pradesh'),
('Uttarakhand','Uttarakhand'),
('West Bengal','West Bengal'),

)

# Define category choices
CATEGORY_CHOICES = (
    ('AR', 'Pencil'),
    ('OG', 'Pencil Box'),
    ('DB', 'Pen'),
    ('PS', 'Ruler'),
    ('SS', 'Ruled Note'),
    ('DF', 'Unruled Note'),
    ('CN', 'Eraser'),
    ('BE', 'Sharpener'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()  
    discounted_price = models.FloatField()  
    description = models.TextField(default='')
    composition =models.TextField(default='')
    uses = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    Product_image = models.ImageField(upload_to='products/')
    def __str__(self):
        return self.title
    

class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1 to 5 rating
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} review by {self.user.username}"

    


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcod = models.IntegerField()  
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

class Order(models.Model):
 STATUS_CHOICES= (
     ('Accepted','Accepted'),
     ('Packed','Packed'),
     ('On The Way','On The Way'),
     ('Delivered','Delivered'),
     ('Cancel','Cancel'),
     ('Pending','Pending'),
 
 )   


class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)




class Orderplaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveBigIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATE_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)  

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price  
    

# class Wishlist(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Change 'Product' to 'product'

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"