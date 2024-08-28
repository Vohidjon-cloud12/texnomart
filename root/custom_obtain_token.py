from rest_framework.templatetags.rest_framework import data
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        refresh = self.get_token(self.user)
        data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        data['user'] = {
            'username': self.user.username,
            'message': True
        }
        return data