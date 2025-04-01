from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User
import threading
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import Response
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import UserSerializer


@api_view(["POST"])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data["is_active"] = False
        serializer.save()
        user = User.objects.filter(username=serializer.data["username"]).first()
        token = Token.objects.get(user=user)
        print(token)
        return Response({"data": serializer.data, "token": token.key})
    else:
        return Response({"error": "errro"})


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user_obj = User.objects.filter(email__iexact=email).first()
    ser = UserSerializer(user_obj, many=False)
    if user_obj:
        validate_password = check_password(password, ser.data["password"])
        print(validate_password, password)
        if validate_password:
            token = Token.objects.get(user=user_obj)
            return Response(
                {
                    "username": ser.data["username"],
                    "id": ser.data["id"],
                    "token": token.key,
                }
            )
        else:
            print("error logging in")
            return Response({"passwordError": "invalid password"})
    else:
        print("email is wrong")
        return Response({"EmailError": "invalid email"})
