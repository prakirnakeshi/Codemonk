from rest_framework import serializers
from .models import *

class BookSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__' # __all__ meaning all fields/parameters are included while calling the api, or data from db.
        # exclude = ['id'] #it will not send id parameter when the api is called.

# serializers.py
# from rest_framework import serializers

# class UserRegistrationSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     # username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
