from django.db.models import Avg
from rest_framework import serializers
from rest_framework.authtoken.admin import User

from texnomart.models import Category, Product, Attribute, AttributeKey, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    def get_product_count(self, obj):
        return obj.products_count

    class Meta:
        model = Category
        fields = '__all__'


# class ProductSerializer(serializers.ModelSerializer):
#     user_like = serializers.SerializerMethodField()
#     category = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#
#     def get_user_like(self, obj):
#         return hasattr(obj, 'user_liked ') and bool(obj.user_liked)
#
#     def get_category(self, obj):
#         return obj.category.title
#
#     def get_image(self, obj):
#         request = self.context.get('request')
#         image = next((img for img in obj.images.all() if img.is_primary), None)
#         if image:
#             return request.build_absolute_uri(image.image.url)
#         return None
#
#     class Meta:
#         model = Product
#         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    user_like = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_user_like(self, obj):
        return bool(obj.user_like)

    def get_category(self, obj):
        return obj.category.title

    def get_image(self, obj):
        request = self.context.get('request')
        image = next((img for img in obj.images.all() if img.is_primary), None)
        if image:
            return request.build_absolute_uri(image.image.url)
        return None

    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    user_like = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_user_like(self, obj):
        return getattr(obj, 'user_likes_prefetched', None)

    def get_image(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        if images:
            return [request.build_absolute_uri(img.image.url) for img in images]
        return None

    def get_comments(self, obj):
        comments = obj.comments.all()
        if comments:
            return [{comment.user.username: {'comment': comment.comment}} for comment in comments]
        return []

    def get_rating(self, obj):
        return obj.rating

    def get_attributes(self, obj):
        return {
            attr.attribute_key.key_name: attr.attribute_value.value
            for attr in obj.attributes.all()
        }

    class Meta:
        model = Product
        fields = '__all__'


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = ['id', 'key_name', ]


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ['id', 'value', ]
