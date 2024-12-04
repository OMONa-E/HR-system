from rest_framework import serializers
from .models import Employee, Profile
from django.contrib.auth.models import User

# Profile Serializers
# -------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role']

# User Serializers
# -------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = [ 'id', 'username', 'password', 'email', 'first_name', 'last_name', 'profile' ]
        read_only_fields = [ 'id' ]

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) # Hash and update the password
        user.save()
        Profile.objects.update_or_create(user=user, **profile_data)
        return user
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if password:
            instance.set_password(password)  # Hash and update the password
        instance.save()

        # Update profile fields
        profile = instance.profile
        profile.role = profile_data.get('role', profile.role)
        profile.save()
        return instance

# Employee Serializers
# -------------------------------------------------------
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"