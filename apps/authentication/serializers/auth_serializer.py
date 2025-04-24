from rest_framework import  serializers

class RegisterSerializer (serializers.Serializer):
    full_name = serializers.CharField(
        max_length=100,
    )
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
    )
    role = serializers.ChoiceField(
        choices= [
            'student',
            'admin'
        ]
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
    )