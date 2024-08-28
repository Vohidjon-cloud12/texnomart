from django.contrib.auth.models import User
from rest_framework import serializers


# class LoginSerializerSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()
#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')
#         if username and password:
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)



class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=100, required=True)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=100, required=True, write_only=True)
    password2 = serializers.CharField(max_length=100, required=True, write_only=True)
    email = serializers.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


