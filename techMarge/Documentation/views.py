from django.shortcuts import render

# Create your views here.


from django.contrib.auth.models import User
import threading
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import Response
from rest_framework.decorators import action, api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import ToolSerializer, UserSerializer
from .models import Tool


@api_view(["POST"])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.validated_data["is_active"] = False
        serializer.save()
        user = User.objects.filter(username=serializer.data["username"]).first()
        token = Token.objects.get(user=user)
        print(token)
        return Response(
            {"data": serializer.data, "token": token.key, "status": status.HTTP_200_OK}
        )
    else:
        return Response(
            {"error": "error", "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
        )


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
                    "status": status.HTTP_200_OK,
                }
            )
        else:
            print("error logging in")
            return Response(
                {
                    "passwordError": "invalid password",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )
    else:
        print("email is wrong")
        return Response(
            {
                "EmailError": "invalid email",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )


@api_view(["POST"])
def createTool(request):
    if request.data is not None:
        new_tool = Tool(
            type=request.data.get("type"),
            title=request.data.get("title").capitalize(),
            description=request.data.get("description"),
            location=request.data.get("location"),
            docLink=request.data.get("docLink"),
            language=request.data.get("language"),
        )
        if new_tool is not None:
            new_tool.save()
            return Response({"tool": new_tool.type, "status": status.HTTP_200_OK})

    else:
        return Response(
            {
                "error": "invalid or empty data",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )


@api_view(["GET"])
def fetchAllTools(request):
    tools = Tool.objects.all()
    if len(tools) > 0:
        tools_ser = ToolSerializer(tools, many=True)
        if tools_ser.data:
            return Response({"data": tools_ser.data, "status": status.HTTP_200_OK})
        else:
            return Response(
                {
                    "error": "error fetching data",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )
    else:
        return Response(
            {
                "error": "no data",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )


@api_view(["GET"])
def fetchOneTool(request):
    title = request.GET.get("title").capitalize()
    print(title)
    tool = Tool.objects.filter(title=title).first()
    if tool:
        tool_ser = ToolSerializer(tool, many=False)
        if tool_ser.data:
            return Response({"data": tool_ser.data, "status": status.HTTP_200_OK})
        else:
            return Response(
                {
                    "error": "error fetching data",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )

    else:
        return Response(
            {
                "error": "no data",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
        )
