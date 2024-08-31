from rest_framework import serializers
from .models import Profile , Health , Calories_Burned
from django.contrib.auth.models import User




class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['birthday', 'sex']
        
        
        
class UserData(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['id','username','password','email']       
        
        
        
class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email','password', 'userprofile']
        
        


        
        
           
    def create(self, validated_data):
        user_profile_data = validated_data.pop('userprofile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **user_profile_data)
        return user
    
    def update(self, instance, validated_data):
        user_profile_data = validated_data.pop('userprofile')
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        profile = instance.profile
        profile.birthday = user_profile_data.get('birthday', profile.birthday)
        profile.sex = user_profile_data.get('sex', profile.sex)
        profile.save()
        
        return instance
    
    
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        
        
class HelthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health
        fields = ['id', 'weight' , 'height']
        
        
class Calories_Burned_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Calories_Burned
        fields = ['id', 'duration_hours','weight' , 'activity']