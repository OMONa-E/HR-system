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
        user.set_password(password)
        user.save()
        # Ensure only one Profile is created or updated for the User
        profile, created = Profile.objects.get_or_create(user=user)
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
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
    """
    Serializer for the Employee model.

    This serializer handles the serialization and deserialization of Employee 
    model instances, enabling easy conversion between complex data types 
    (e.g., querysets) and JSON for API responses.

    Meta:
        model (Employee): The model being serialized.
        fields ('__all__'): Includes all fields from the Employee model:
            - employee_id: Unique identifier for the employee (e.g., social security number).
            - employee_nin: National identity number of the employee.
            - full_name: Full name of the employee.
            - email: Email address of the employee.
            - job_title: Job title of the employee.
            - phone_number: Contact phone number of the employee.
            - date_joined: Date when the employee joined the organization.
            - date_created: Timestamp indicating when the employee record was created.
    """
    class Meta:
        model = Employee
        fields = "__all__"