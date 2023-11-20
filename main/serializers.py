from rest_framework import serializers
#import all models we created
from . import models


#create VendorSerializer and extend the model Serializer
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Vendor
        # which fields we want to show
        fields=['id','user','address']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1


#create VendorDetailSerializer and extend the model Serializer
class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Vendor
        # which fields we want to show
        fields=['id','user','address']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(VendorDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1


# Product image serializer
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['id','product','image']



#create ProductListSerializer and extend the model Serializer
class ProductListSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True, read_only=True)
    # product_imgs=ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model=models.Product
        # which fields we want to show, coming from product model
        fields=['id','category','vendor', 'title','tag_list','detail', 'price','product_ratings','image']
        # fields=['id','category','vendor', 'title','tag_list','detail', 'price','product_ratings','product_imgs']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(ProductListSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1





#create ProductDetailSerializer and fileds will be same as product list
class ProductDetailSerializer(serializers.ModelSerializer):
    product_ratings=serializers.StringRelatedField(many=True, read_only=True)
    product_imgs=ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model=models.Product
        # which fields we want to show, coming from product model
        fields=['id','category','vendor', 'title','slug','tag_list','detail', 'price','product_ratings','product_imgs','demo_url','image']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(ProductDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1


#create CustomerSerializer and extend the model Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        # which fields we want to show
        fields=['id','user','mobile']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(CustomerSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


#create CustomerDetailSerializer and extend the model Serializer
class CustomerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Customer
        # which fields we want to show
        fields=['id','user','mobile']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(CustomerDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


#create OrderSerializer and extend the model Serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Order
        # which fields we want to show
        fields=['id','customer']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


#create OrderDetailSerializer and extend the model Serializer
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.OrderItems
        # which fields we want to show
        fields=['id','order','product']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(OrderDetailSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


#create CustomerAddressSerializer and extend the model Serializer
class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.CustomerAddress
        # which fields we want to show
        fields=['id','customer','address','default_address']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(CustomerAddressSerializer, self).__init__(*args, **kwargs)
        self.Meta.depth = 1


# ProductRatingSerializer by the customer
class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductRating
        # which fields we want to show
        fields=['id','customer','product','rating','reviews','add_time']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(ProductRatingSerializer, self).__init__(*args, **kwargs)
        # If we define the depth it will fech data from customer and product
        self.Meta.depth = 1



#create CategorySerializer and extend the model Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductCategory
        # which fields we want to show
        fields=['id','title','detail']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1


#create CategoryDetailSerializer and extend the model Serializer
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.ProductCategory
        # which fields we want to show
        fields=['id','title','detail']

        # use depth to fetch user data
    def __init__(self, *args, **kwargs):
        super(CategoryDetailSerializer, self).__init__(*args, **kwargs)
        # self.Meta.depth = 1

