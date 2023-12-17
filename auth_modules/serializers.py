from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class SignUpSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username","email","password","Phone_no")

class LoginSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email","password",)
