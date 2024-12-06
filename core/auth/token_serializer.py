from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

# Custom Token Obtain Pair Serializer
# -------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for generating JWT tokens with additional claims.

    This serializer extends the `TokenObtainPairSerializer` to include custom 
    claims in the token payload, such as the user's role.

    Methods:
        get_token(cls, user):
            Override the base `get_token` method to add custom claims.

    Custom Claims:
        role (str): The role of the authenticated user, retrieved from the 
                    `Profile` model associated with the `User`.

    Example Token Payload:
        {
            "token_type": "access",
            "exp": <expiry_timestamp>,
            "jti": <unique_token_id>,
            "user_id": <user_id>,
            "role": <role>
        }
    
    Returns:
        Token: A JWT token with the added custom claims.
    """
    @classmethod
    def get_token(cls, user) -> Token:
        """
        Generate a JWT token for the given user with additional claims.

        Args:
            user (User): The authenticated user for whom the token is being generated.

        Returns:
            Token: A JWT token with the user's role included in the payload.

        Custom Behavior:
            - Adds the `role` of the user to the token payload.
            - Logs a message when the token is generated.
        """
        token = super().get_token(user)
        token['role'] = user.profile.role # Inject the user's role into the token payload.
        return token
