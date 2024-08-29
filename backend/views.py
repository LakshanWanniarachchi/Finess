import decimal
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # Add this line
from .serializers import UserSerializer , LoginSerializer , HelthSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate  # Add this line
from .models import Health
# Create your views here.


class Create_User(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
           
        
            user = serializer.save()


            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
            "message": "User created successfully!",
            "refresh": refresh_token,
            "access": access_token,
            }, status=status.HTTP_201_CREATED)
           
           
           
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class CustomLoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        
           
            user = authenticate(username= request.data.get("username"), password= request.data.get("password"))
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                tokens = {
                    "message": "User logged in successfully!",
                    "refresh": refresh_token,
                    "access": access_token,
                }
                return Response(tokens, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


class CalculateBMI(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = HelthSerializer

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data)
        
    
        if serializer.is_valid():
            
           
           
           user = request.user
           weight = decimal.Decimal(serializer.data.get('weight'))
           height = decimal.Decimal(serializer.data.get('height'))
           bmi = weight / (height ** 2)
           
           save_data = Health.objects.create(user=user, weight=weight, height=height, bmi=bmi)
           save_data.save()
           
           return Response({
            "message": "BMI calculated successfully!",
            "bmi": bmi,
            "weight": weight,
            "height": height,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    
    