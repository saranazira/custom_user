from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Account is successfully registered', status=201)

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
