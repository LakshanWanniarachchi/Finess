import decimal
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .FitnessCalculations import cal_Calories_Burned_During_Exercise  # Add this line
from .serializers import UserSerializer, LoginSerializer, HelthSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate  # Add this line
from .models import Health, Calories_Burned , Profile
from rest_framework.generics import CreateAPIView

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, Calories_Burned_data_Serializer, Bmi_data_Serializer ,UserProfileSerializer
from .GeminiAi import GeminiAi  # Add this line
# Create your views here.
import json
from datetime import datetime


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class Create_User(CreateAPIView):
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

        user = authenticate(username=request.data.get(
            "username"), password=request.data.get("password"))
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
            activity = serializer.validated_data.get('activity')
            duration = decimal.Decimal(
                serializer.validated_data.get('duration_hours'))
            bmi = weight / (height ** 2)

            calories_burned = cal_Calories_Burned_During_Exercise(
                activity, weight, duration)

            if isinstance(calories_burned, str):  # Check if there's an error message
                return Response({
                    "message": calories_burned
                }, status=status.HTTP_400_BAD_REQUEST)

            save_data = Health.objects.create(user=user, weight=weight, height=height, bmi=bmi,  calories_burned=calories_burned,
                                              duration_hours=duration,
                                              activity=activity)

            save_data.save()

            return Response({
                "message": "BMI calculated successfully!",
                "bmi": bmi,
                "weight": weight,
                "height": height,
                "calories_burned": calories_burned,
                "duration_hours": duration,
                "activity": activity
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CalculateBMI(APIView):
#     # authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class = HelthSerializer

#     def post(self, request):

#         serializer = self.serializer_class(data=request.data)


#         if serializer.is_valid():


#            user = request.user
#            weight = decimal.Decimal(serializer.data.get('weight'))
#            height = decimal.Decimal(serializer.data.get('height'))
#            bmi = weight / (height ** 2)

#            save_data = Health.objects.create(user=user, weight=weight, height=height, bmi=bmi)
#            save_data.save()

#            return Response({
#             "message": "BMI calculated successfully!",
#             "bmi": bmi,
#             "weight": weight,
#             "height": height,
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class Cal_Calories_Burned(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = Calories_Burned_Serializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             user = request.user
#             activity = serializer.validated_data.get('activity')
#             weight = decimal.Decimal(serializer.validated_data.get('weight'))
#             duration = decimal.Decimal(serializer.validated_data.get('duration_hours'))

#             calories_burned = cal_Calories_Burned_During_Exercise(activity, weight, duration)

#             if isinstance(calories_burned, str):  # Check if there's an error message
#                 return Response({
#                     "message": calories_burned
#                 }, status=status.HTTP_400_BAD_REQUEST)

#             save_data = Calories_Burned.objects.create(
#                 user=user,
#                 calories_burned=calories_burned,
#                 duration_hours=duration,
#                 activity=activity,
#                 weight=weight
#             )

#             return Response({
#                 "message": "Calories burned calculated successfully!",
#                 "calories_burned": calories_burned,
#                 "duration": duration,
#                 "activity": activity,
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class get_calories(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        calories = Health.objects.filter(user=user).order_by('-date')[:30]
        serializer = Calories_Burned_data_Serializer(calories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class get_BMI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        bmi = Health.objects.filter(user=user).order_by('-date')[:1]
        serializer = Bmi_data_Serializer(bmi, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class get_diet_plan(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        calories = Health.objects.filter(user=user).order_by('-date')[:30]
        serializer_Calories = Calories_Burned_data_Serializer(
            calories, many=True)

        bmi = Health.objects.filter(user=user).order_by('-date')[:1]
        serializer_bmi = Bmi_data_Serializer(bmi, many=True)
        
        
        user_data = Profile.objects.filter(user=user)
        
        serializer_profile = UserProfileSerializer(user_data, many=True)
        
       
        
        if serializer_profile.data:
            birth_date = serializer_profile.data[0]['birthday']
            gender = serializer_profile.data[0]["sex"]
            
            
            if gender in "M":
                
                     sex = "Male"  
            elif gender in "F":
                
                sex = "Female"
                
            else:
                
                sex = "Other"
                    
            
            
            
            if birth_date:
             birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
             today = datetime.today()
             age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

            else:
             age_years = None
          
        else:
            age_years = None
            age_months = None
            age_days = None

      
            
        
      
        text_generator = GeminiAi()
        generated_text = text_generator.text_gemini_text_generator(
            bmi=serializer_bmi.data, Calories=serializer_Calories.data , age=   age_years , gender= sex )

   
        print(generated_text)

        return Response({"message": "Diet plan generated successfully!", "diet_plan": generated_text}, status=status.HTTP_200_OK)
