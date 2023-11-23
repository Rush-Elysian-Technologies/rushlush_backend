from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
# Vendor models
class Vendor(models.Model):
    # If we delete the user, the user data will also be deleted as we used CASCADE
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # It means address can be empty
    address=models.TextField(null=True)

    # whenever we call this fuction it returns,this magic methog __str__, user name
    def __str__(self):
        return self.user.username



# Product Category Model 
# This can be created only by admin, vendor any only add product according to that category

class ProductCategory(models.Model):
    # whenevr you use charfiled the max length is compulsary
    title=models.CharField(max_length=200)
    # This details field can be null
    detail=models.TextField(null=True)

    # whenever we call this fuction it returns,this magic methog __str__, self.title
    def __str__(self):
        return self.title


# product Model 
class Product(models.Model):
    # Product is product category dependant, if we delete vendor data, it will not delete data when we "set_null"  
    category=models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True,related_name='category_product')
    # Who is adding the product
    vendor=models.ForeignKey(Vendor,on_delete=models.SET_NULL,null=True)
    # whenevr you use charfiled the max length is compulsary
    title=models.CharField(max_length=200)
    # Add a new 'slug' field
    # slug = models.SlugField(unique=True, null=True, blank=True)
    slug = models.CharField(max_length=300,unique=True,null=True)
    # This details field can be null
    detail=models.TextField(null=True)
    # This price filed is required
    price=models.DecimalField(max_digits=10,decimal_places=2)
    # Add tags
    # tags = models.ManyToManyField('Tag')
    tags=models.TextField(null=True)
    # Image add
    image=models.ImageField(upload_to='product_imgs',null=True)
    demo_url=models.URLField(null=True,blank=True)

    # def save(self, *args, **kwargs):
    #     # Automatically generate a slug when saving the product
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
    # whenever we call this fuction it returns,this magic methog __str__, self.title
    def __str__(self):
        return self.title
    # deine tag links
    def tag_list(self):
        if self.tags:
            tagList = self.tags.split(',')
        else:
            tagList = []
        return tagList

    
# class Tag(models.Model):
#     name = models.CharField(max_length=255)


# Customer models
class Customer(models.Model):
    # If we delete the user, the user data will also be deleted as we used CASCADE
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # It is a required filed so keet it empty
    mobile=models.PositiveBigIntegerField(unique=True)

    # whenever we call this fuction it returns,this magic methog __str__, user name
    def __str__(self):
        return self.user.username
    

# Order Model
class Order(models.Model):
    # who made this order, using cascade if we delete the customer, order data will  be deleted
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer_orders')
    # order time
    order_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.order_time)


# Order Items Model 
# can be one or many, cascade delete order item if order is deleted
# Order item belons to specific order number
class OrderItems(models.Model):
    # Specific order num which have multiple items
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    # which product the customer ordered
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    
    # we will return product title
    def __str__(self):
        return self.product.title


# Customer Address Model
class CustomerAddress(models.Model):
    # 
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer_address')
    # 
    address=models.TextField()
    # customer can set any address default
    # that default address weill show in their billing information
    default_address=models.BooleanField(default=False)

    # we will return address
    def __str__(self):
        return self.address


# Product rating and review
class ProductRating(models.Model):
    # who is the customer
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='rating_customers')
    #
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_ratings')
    # Rating will be varied from 1 to 5
    rating=models.IntegerField()
    #
    reviews=models.TextField()
    # whenever customer adds rating, it automatically add data and time
    add_time=models.DateTimeField(auto_now_add=True)

    # by default we will retun the reviews
    def __str__(self):
        return f'{self.rating} - {self.reviews}'


# pip install pillow - for images or file fields
# Product Images Model
class ProductImage(models.Model):
    # 
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_imgs')
    # we define null because we have already existing rows
    image=models.ImageField(upload_to='product_imgs/',null=True)


    # we will return address
    def __str__(self):
        return self.image.url

