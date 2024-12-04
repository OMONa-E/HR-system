from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from applications.onboarding.models import UserDevice

# Custom Token Obtain Pair API View
# --------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh = response.data.get("refresh")
            access = response.data.get("access")
            user = self.request.user
            device_name = request.data.get("device_name", "Unknown Device")

            # Save the refresh token to UserDevice model
            UserDevice.objects.create(
                user=user,
                device_name=device_name,
                refresh_token=refresh,
            )
        return response
    
# Device Logout View
# -------------------------------------------------
class DeviceLogoutView(APIView):
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
class PasswordResetConfirmView(APIView):
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
