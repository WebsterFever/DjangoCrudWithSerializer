from ipdb import set_trace
from django.forms import model_to_dict
from rest_framework.views import Request, Response, APIView , status
from users.serializers import UserSerializer
from .models import User
from addresses.models import Address
from rest_framework.pagination import PageNumberPagination


class UserView(APIView , PageNumberPagination):
    def post(self, req:Request) -> Response:
        serializer = UserSerializer(data=req.data)
       # if not serializer.is_valid():   
          # return Response(serializer.errors , status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        address_data = serializer.validated_data.pop("address")
        user = User.objects.create(**serializer.validated_data)
        Address.objects.create(**address_data, user=user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, req:Request) -> Response:
        by_email = req.query_params.get("email", None)
        if by_email:
            users = User.objects.filter(email__icontains=by_email)
        else:
             users = User.objects.all()
       
        result = self.paginate_queryset(users, req)
        serializer = UserSerializer(result , many=True)
        return self.get_paginated_response (serializer.data)

class UserDetailView(APIView):
    def get(self, req:Request, user_id: int) -> Response:
        try:
            found_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"msg": "This user is not in the database" },
            status.HTTP_404_NOT_FOUND,   
        )

        serializer = UserSerializer(found_user)
        return Response(serializer.data)
    
    def delete(self, req:Request, user_id: int) -> Response:
        try:
            found_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "User does not exist "},
                status.HTTP_404_NOT_FOUND,
            )
        found_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, req:Request, user_id: int) -> Response:
        try:
          found_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
          return Response(
                {"message": "User does not exist "},
                 status.HTTP_404_NOT_FOUND,
            )
        serializer = UserSerializer(data=req.data , partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        for key , value in serializer.validated_data.items():
            setattr(found_user , key , value )
        found_user.save()

        serializer = UserSerializer(found_user)
        return Response(serializer.data)


