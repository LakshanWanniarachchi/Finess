from django.urls import path
from .views import Create_User, CustomLoginView, CalculateBMI, get_calories, get_BMI, get_diet_plan
urlpatterns = [
    path('register', Create_User.as_view(), name='register'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('bmi', CalculateBMI.as_view(), name='bmi calculate'),
    path('get_calories', get_calories.as_view(), name='get_calories'),
    path('get_bmi', get_BMI.as_view(), name='get_bmi'),
    path('get_diet', get_diet_plan.as_view(), name='get_diet'),

]
