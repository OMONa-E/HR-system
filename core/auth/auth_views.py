from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, serializers
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from applications.onboarding.models import UserDevice
from .token_serializer import CustomTokenObtainPairSerializer

# Custom Token Obtain Pair API View
# --------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom API view for obtaining JWT tokens with additional functionality.

    This view allows authenticated users to obtain access and refresh tokens. 
    Additionally, it validates user account status and stores refresh tokens in 
    the `UserDevice` model for device tracking.

    Attributes:
        serializer_class: Specifies the serializer used to validate user credentials 
                          and generate tokens.

    Methods:
        post(request, *args, **kwargs):
            Authenticates the user, ensures their account is active, and generates tokens.
            Also logs the refresh token in the `UserDevice` model.

    Permissions:
        No explicit permissions are required for this endpoint.

    Returns:
        Response: 
            - HTTP 200: Tokens successfully generated.
            - HTTP 403: If the user account is inactive.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Retrieve the authenticated user
        user = serializer.user

        # Ensure the user is active and allowed to log in
        if not user.is_active:
            return Response({"error": "User account is inactive."}, status=403)

        # Generate tokens
        tokens = serializer.validated_data

        # Add the refresh token to UserDevice
        refresh = tokens.get("refresh")
        device_name = request.data.get("device_name", "Unknown Device")
        UserDevice.objects.create(
            user=user,
            device_name=device_name,
            refresh_token=refresh,
        )
        return Response(tokens, status=status.HTTP_200_OK)
    
# Device Logout View
# -------------------------------------------------
class DeviceLogoutView(APIView):
    """
    API view for logging out a specific device.

    This view allows authenticated users to log out of a specific device by 
    blacklisting its refresh token and deleting the corresponding record from 
    the `UserDevice` model.

    Permissions:
        - Requires authentication (IsAuthenticated).

    Methods:
        post(request):
            Logs out a specific device by ID, blacklists its refresh token, 
            and removes the device record.

    Args:
        request.data:
            - device_id (int): The ID of the device to log out.

    Returns:
        Response:
            - HTTP 200: Device successfully logged out.
            - HTTP 404: Device not found.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        device_id = request.data.get("device_id")
        try:
            device = UserDevice.objects.get(id=device_id, user=request.user)
            refresh_token = RefreshToken(device.refresh_token)
            refresh_token.blacklist()  # Blacklist the token
            device.delete()  # Remove the device record
            return Response({"message": "Device logged out successfully."}, status=200)
        except UserDevice.DoesNotExist:
            return Response({"error": "Device not found."}, status=404)

# Active Device View
# -------------------------------------------------
class ActiveDevicesView(APIView):
    """
    API view for retrieving a list of active devices.

    This view allows authenticated users to retrieve all devices associated 
    with their account that are actively storing refresh tokens.

    Permissions:
        - Requires authentication (IsAuthenticated).

    Methods:
        get(request):
            Retrieves a list of active devices for the authenticated user.

    Returns:
        Response:
            - HTTP 200: A list of active devices including:
                - id (int): Device ID.
                - device_name (str): Name of the device.
                - created_at (datetime): Timestamp of when the device was added.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        devices = UserDevice.objects.filter(user=request.user)
        return Response(
            [{"id": device.id, "device_name": device.device_name, "created_at": device.created_at} for device in devices],
            status=status.HTTP_200_OK
        )
    
# Password Reset Request View
# -------------------------------------------------
class PasswordResetRequestView(APIView):
    """
    API view for requesting a password reset.

    This view allows users to request a password reset by providing their email 
    address. A password reset link is sent to the user's email if the account exists.

    Methods:
        post(request):
            Generates a password reset token and sends a reset link via email.

    Args:
        request.data:
            - email (str): The email address of the user requesting a password reset.

    Returns:
        Response:
            - HTTP 200: Password reset email sent.
            - HTTP 404: If the email does not correspond to any user.
    """
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"

            # Send email
            send_mail(
                subject="Password Reset Request",
                message=f"Click the link to reset your password: {reset_link}",
                from_email="jobatwok1@gmail.com",
                recipient_list=[user.email],
            )
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

# Password Reset Confirm View
# -------------------------------------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmView(APIView):
    """
    API view for confirming a password reset request.

    This view validates the password reset token and updates the user's password 
    if the token is valid and not expired.

    Methods:
        post(request, uidb64, token):
            Validates the token and resets the user's password.

    Args:
        uidb64 (str): Base64 encoded user ID.
        token (str): Password reset token.
        request.data:
            - password (str): The new password to set for the user.

    Returns:
        Response:
            - HTTP 200: Password successfully reset.
            - HTTP 400: If the token is invalid, expired, or the request is malformed.
    """
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if PasswordResetTokenGenerator().check_token(user, token):
                new_password = request.data.get('password')
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid token or token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
