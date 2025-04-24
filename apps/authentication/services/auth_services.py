
from config.supabase.supabase_client import supabase

# register function to complete registration process in supabase auth
def register(full_name, email, password, role):
    try:
        # Perform the sign-up process with the provided user details
        response = supabase.auth.sign_up({ "email": email, "password": password, "options":{
            "full_name": full_name,
            "role": role
        }})


        # Check for any errors in the response
        if hasattr(response, 'error') and response.error:
            print("Error creating user:", response.error.message)
            return None

        # Parse the response to make it more usable
        user_data = {}
        for key, value in response.user:
            user_data[key] = value

        # Print out the formatted user data for inspection
        print("User data:", user_data)

        # If no error, return the user data
        if 'user_metadata' in user_data:
            return user_data['user_metadata']  # Return user metadata if available
        else:
            print("Unexpected response format:", response)
            return None

    except Exception as e:
        # Handle any exceptions during the registration process
        raise Exception(f"Error creating user: {e}")



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
