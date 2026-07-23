from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "password",
        )
    
    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Este email já está cadastrado."
            )

        return value
    
    def validate_phone_number(self, value):
        
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "Este número de telefone já está cadastrado."
            )

        return value
