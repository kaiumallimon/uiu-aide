# middlwares/auth_middleware.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from supabase import create_client, Client
from apps.authentication.models.supabase_user import SupabaseUser
from config import settings

class SupabaseJWTAuthentication(BaseAuthentication):
    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
            
        try:
            token = auth_header.split(' ')[1]
            if not token:
                return None

            # Verify token
            user = self.supabase.auth.get_user(token)
            if not user:
                raise AuthenticationFailed('Invalid token')
                
            user_id = user.user.id
            
            # Fetch profile
            response = self.supabase.table("profiles").select("*").eq("id", user_id).execute()
            if len(response.data) == 0:
                raise AuthenticationFailed("User profile not found")
                
            # Wrap profile in SupabaseUser
            return (SupabaseUser(response.data[0]), None)
            
        except Exception as e:
            raise AuthenticationFailed(str(e))