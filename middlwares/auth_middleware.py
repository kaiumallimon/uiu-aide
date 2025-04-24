import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class SupabaseAuth(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            response = requests.get(
                f"{settings.SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": settings.SUPABASE_API_KEY
                }
            )

            if response.status_code != 200:
                raise AuthenticationFailed("Invalid or expired token")

            user_data = response.json()
            user_metadata = user_data.get("user_metadata", {})

            user = {
                "id": user_data["id"],
                "email": user_data["email"],
                "role": user_metadata.get("role", "student")  # default to student
            }

            return user, None
        except Exception as e:
            raise AuthenticationFailed(str(e))
