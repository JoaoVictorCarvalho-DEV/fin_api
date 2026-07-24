from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


def create_user(validated_data):
    password = validated_data.pop("password")

    user = User(**validated_data)
    user.set_password(password)
    user.save()

    return user

def update_user(user, validated_data):
        for field, value in validated_data.items():
            setattr(user, field, value)

        user.save()

        return user
    
def logout_user(refresh_token: str):
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

    except TokenError:
        raise ValueError("Refresh token inválido ou expirado.")
    

def change_password(user, old_password, new_password):
    if not user.check_password(old_password):
        raise ValueError("Senha atual incorreta.")

    validate_password(new_password, user)

    user.set_password(new_password)
    user.save()

    return user