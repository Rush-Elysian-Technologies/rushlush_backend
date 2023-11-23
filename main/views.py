# what kind of view we want to show
from rest_framework import generics,permissions,pagination,viewsets
#import the serializers in our views
from . import serializers
# import model
from . import models

# If any kind of duplication, this error activates, and we will catch the error
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login

# Create your views here.
# VendorList returns all the sellers
# from generices we want list API view, it will return data as alist
# change the “ListAPIView” to "ListCreateAPIView", it is responsible for creating the data and adding the data 

class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    # we can add as many permission we want
    # permission_classes=[permissions.IsAuthenticated]


# VendorDetail returns all the details of the vendors
# from generices we want RetrieveAPIView, it will return data 
# change “RetrieveAPIView” to RetrieveUpdateDestroy”, which is responsible, for fetching, updating and destroying the single data 


class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorDetailSerializer
    # we can add as many permission we want
    # permission_classes=[permissions.IsAuthenticated]


# ProductList returns all the list of the products
class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    pagination_class = pagination.PageNumberPagination

    # # override the defualt query set, this give all products is specific category
    def get_queryset(self):
        qs=super().get_queryset()
        category_id = self.request.GET.get('category')  # Use get() method to handle missing parameter
        if category_id is not None:
            category = models.ProductCategory.objects.get(id=category_id)
            qs = qs.filter(category=category)
        return qs
    # def get_queryset(self):
    #     qs=super().get_queryset()
    #     category=self.request.GET['category']
    #     category=models.ProductCategory.objects.get(id=category)
    #     qs=qs.filter(category=category)
    #     return qs



# TagProductList returns all the list of the products with specif tag
class TagProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    pagination_class = pagination.PageNumberPagination

    # # override the defualt query set, this give all products is specific category
    def get_queryset(self):
        qs=super().get_queryset()
        #kwars which we are passing in URL
        tag=self.kwargs['tag']
        # i means insensitive
        qs = qs.filter(tags__icontains=tag)
        return qs


# RelatedProductList returns all the list of the products with specif tag
class RelatedProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductListSerializer
    # pagination_class = pagination.PageNumberPagination

    # # override the defualt query set, this give all products is specific category
    def get_queryset(self):
        qs=super().get_queryset()
        #kwars which we are passing in URL, we get ID
        product_id=self.kwargs['pk']
        product=models.Product.objects.get(id=product_id)
        # i means insensitive, exclude the current product from the list
        qs = qs.filter(category=product.category).exclude(id=product_id)
        return qs


# ProductDetails returns all the Details of the products
class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer



# CustomerList returns all the CCustomer
class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer


# CustomerDetail returns all the details of the Customers
class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerDetailSerializer

# we will use csrf decorator and return response---this is old one
@csrf_exempt
def customer_login(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    if user:
        customer=models.Customer.objects.get(user=user)
        msg={
            'bool':True,
            'user':user.username, 
            'id': customer.id,
        }
    else:
        msg={
            'bool':False,
            'msg':'Invalid Username/ Password!'
        }

    return JsonResponse(msg)

# @csrf_exempt
# def customer_login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)
    
#     if user:
#         login(request, user)  # Log the user in
#         customer = models.Customer.objects.get(user=user)
#         request.session['customer_id'] = customer.id  # Set customer_id in session
#         msg = {
#             'bool': True,
#             'user': user.username,
#             'id': customer.id,
#         }
#     else:
#         msg = {
#             'bool': False,
#             'msg': 'Invalid Username/Password!'
#         }

#     return JsonResponse(msg)


# we will use csrf decorator and return response
# we are not posting any tokens , so CSRF is applied 
@csrf_exempt
def customer_register(request):
    first_name=request.POST.get('first_name')
    last_name=request.POST.get('last_name')
    email=request.POST.get('email')
    mobile=request.POST.get('mobile')
    username=request.POST.get('username')
    password=request.POST.get('password')
    try:
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            # mobile=mobile,
            username=username,
            password=password,
        )
        if user:
            try:
                # create customer
                customer=models.Customer.objects.create(
                    user=user,
                    mobile=mobile
                )
                msg={
                    'bool':True,
                    'user':user.id,
                    'customer':customer.id,
                    'msg':'Thank you for Registration. You can Login now!'
                }
            except IntegrityError:
                msg={
                        'bool':False,
                        'msg':'Mobile Number already Exists!!'
                    }
        else:
            msg={
                'bool':False,
                'msg':'Oops ... Something went wrong!!'
            }
    except IntegrityError:
        msg={
                'bool':False,
                'msg':'Username already Exists!!'
            }

    return JsonResponse(msg)

# OrderList returns all the orders
class OrderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    # pagination_class=pagination.LimitOffsetPagination

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     return super().post(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     try:
    #         # Existing code for order creation and processing

    #         return Response({"message": "Order created successfully"}, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         # Log the exception for backend debugging purposes
    #         logger.error(f"Error processing order: {str(e)}")
    #         # Return a clearer error message in JSON format
    #         return Response({"error": "Internal Server Error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Order items returns all the order items
class OrderItemList(generics.ListCreateAPIView):
    queryset = models.OrderItems.objects.all()
    serializer_class = serializers.OrderItemSerializer
    # pagination_class=pagination.LimitOffsetPagination



# OrderDetail returns all the details of the Customers
class OrderDetail(generics.ListAPIView):
    # queryset = models.OrderItems.objects.all()
    serializer_class = serializers.OrderDetailSerializer

    def get_queryset(self):
        order_id=self.kwargs['pk']
        order=models.Order.objects.get(id=order_id)
        order_items=models.OrderItems.objects.filter(order=order)

        return order_items



# CustomerAddress retusn customer address
class CustomerAddressViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.CustomerAddressSerializer
    queryset=models.CustomerAddress.objects.all()


# ProductRatingViewSet returns customer product reviews and ratings
class ProductRatingViewSet(viewsets.ModelViewSet):
    serializer_class=serializers.ProductRatingSerializer
    queryset=models.ProductRating.objects.all()


# category list API view
class CategoryList(generics.ListCreateAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer


# category detail API view
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategoryDetailSerializer






