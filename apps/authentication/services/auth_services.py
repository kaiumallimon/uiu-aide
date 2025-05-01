
from config.supabase.supabase_client import supabase

# register function to complete registration process in supabase auth
def register(full_name, email, password, role):
    try:
        # Step 1: Register user via Supabase Auth
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })

        # Check for sign-up error
        if not response.user:
            print("Error creating user:", response.error.message)
            return None

        # Extract user ID from response
        user_id = response.user.id  # This is the auth UID

        # Step 2: Insert additional data (full_name and role) into the database
        insert_response = supabase.table("profiles").insert({
            "id": user_id,
            "full_name": full_name,
            "role": role
        }).execute()

        return insert_response.data

    except Exception as e:
        raise Exception(f"Error during registration: {e}")


# login function to complete login process in supabase auth
def login(email, password):
    try:
        # Perform sign-in
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # Check if the response contains an error
        if hasattr(response, 'error') and response.error:
            return {
                "status": "error",
                "message": response.error.message
            }

        # Extract user and session cleanly
        user = response.user
        session = response.session

        result = {
            "status": "success",
            "message": "User logged in successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "created_at": user.created_at,
                "last_sign_in_at": user.last_sign_in_at,
                "role": user.role,
                "metadata": user.user_metadata,
            },
            "tokens": {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_in": session.expires_in,
                "expires_at": session.expires_at,
                "token_type": session.token_type
            }
        }

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Exception occurred: {str(e)}"
        }
