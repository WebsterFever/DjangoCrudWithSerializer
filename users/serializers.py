from rest_framework import serializers

from addresses.serializers import AddressSerializer
from recipes.serializers import RecipeSerializer

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=20)
    last_name =  serializers.CharField(max_length=20)
    email = serializers.EmailField()
    created_at = serializers.DateTimeField(read_only=True)
    update_at = serializers.DateTimeField(read_only=True)
    address = AddressSerializer()
    recipes = RecipeSerializer(many=True, read_only=True)