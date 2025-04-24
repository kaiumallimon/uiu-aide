from config.supabase.supabase_client import supabase


def get_all_users():
    """ Fetch all users from the database. """
    try:
        # Fetch all users
        response = supabase.table("test_user").select("*").execute()

        # Check if response contains data
        if response.data:
            users = response.data
            return {
                "status": "success",
                "message": "Users fetched successfully",
                "data": users,
            }
        else:
            # Handle error response
            print(f"Error fetching users: {response.error}")
            return {
                "status": "error",
                "message": f"Error fetching users: {response.error}",
            }
    except Exception as e:
        print(f"Error fetching users: {e}")
        return {
            "status": "error",
            "message": f"Error fetching users: {e}",
        }

def create_user(name, email):
    """ Create a new user in the database. """
    try:
        # Insert new user
        response = supabase.table("test_user").insert({"name": name, "email": email}).execute()

        # Print the full response for debugging
        print(f"Response from Supabase: {response}")

        # Check if the response contains data (user created)
        if response.data:
            user = response.data[0]  # Get the first user object from data
            return {
                "status": "success",
                "message": "User created successfully",
                "data": user,
            }
        else:
            # Handle error response
            print(f"Error creating user: {response.error}")
            return {
                "status": "error",
                "message": f"Error creating user: {response.error}",
            }
    except Exception as e:
        print(f"Error creating user: {e}")
        return {
            "status": "error",
            "message": f"Error creating user: {e}",
        }
