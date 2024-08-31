from django.urls import path
from .views import Create_User , CustomLoginView , CalculateBMI , Cal_Calories_Burned
urlpatterns = [
    path('register', Create_User.as_view(), name='register'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('bmi', CalculateBMI.as_view(), name='bmi calculate'),
    path('calories_burned', Cal_Calories_Burned.as_view(), name='calories_burned'),
]
