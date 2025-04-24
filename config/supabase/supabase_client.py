import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # loads .env from project root

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
