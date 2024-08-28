from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Prefetch, Avg, Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from texnomart import permissions
from texnomart.models import Category, Product, Image, Attribute, AttributeKey, AttributeValue, Comments
from texnomart.serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, \
    AttributeKeySerializer, AttributeValueSerializer


# Create your views here.

class CategoryListApiView(generics.ListAPIView):
    queryset = Category.objects.annotate(products_count=(Count('products')))
    serializer_class = CategorySerializer

    # @method_decorator(cache_page(60, key_prefix="category_list"))  # 1 daqiqaga keshlab qo'yish
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)


class CategoryAllProducts(GenericAPIView):
    queryset = Product.objects.select_related('category').prefetch_related(
        Prefetch('images', queryset=Image.objects.filter(is_primary=True)))
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    # permission_classes = (permissions.IsSuperAdminOrReadOnly,)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        cache_key = f"category_products_{slug}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        products = self.queryset.filter(category__slug=slug)
        serializer = self.serializer_class(products, many=True, context={'request': self.request})
        cache.set(cache_key, serializer.data, timeout=0)  # 1 daqiqaga keshlab qo'yish
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCategoryView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (permissions.IsSuperAdminOrReadOnly,)


class UpdateCategoryView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        slug = self.kwargs['slug']
        cache.delete(f"category_products_{slug}")
        cache.delete("category_list")
        return response


class DeleteCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #
    def delete(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        cache_key = f'products_{self.request.user.id if self.request.user.is_authenticated else "anonymous"}'
        queryset = cache.get(cache_key)
        if not queryset:

            queryset = Product.objects.select_related('category').prefetch_related('images')

            if self.request.user.is_authenticated:
                user_like = Prefetch('user_like', queryset=User.objects.filter(id=self.request.user.id),
                                     to_attr='likes')
                queryset = queryset.prefetch_related(user_like)

            cache.set(cache_key, queryset, timeout=300)

        return queryset



class ProductDetailView(generics.GenericAPIView):
    queryset = Product.objects.prefetch_related(
        Prefetch('images', queryset=Image.objects.filter(is_primary=True)),
        Prefetch('comments', queryset=Comments.objects.select_related('user')),
        Prefetch('attributes', queryset=Attribute.objects.select_related('attribute_value').select_related('attribute_key')),
    ).annotate(rating=Avg('comments__rating'))
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        user = request.user

        product = self.get_queryset().filter(pk=product_id).prefetch_related(
            Prefetch(
                'user_like',
                queryset=User.objects.filter(id=user.id),
                to_attr='user_likes_prefetched'
            )
        ).first()

        if not product:
            return Response({'detail': 'Not found.'}, status=404)

        serializer = self.get_serializer(product)
        return Response(serializer.data)

class PruductEditView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class ProductDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class AttributeKeyView(GenericAPIView):
    queryset = Attribute.objects.all()
    serializer_class = AttributeKeySerializer

    def get(self, request, *args, **kwargs):
        cache_key = "attribute_keys"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = AttributeKey.objects.all()
        serializer = AttributeKeySerializer(data, many=True, context={'request': request})
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AttributeValueView(GenericAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', ]

    def get(self, request, *args, **kwargs):
        cache_key = "attribute_values"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        data = AttributeValue.objects.all()
        serializer = AttributeValueSerializer(data, many=True, context={'request': request})
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data, status=status.HTTP_200_OK)
