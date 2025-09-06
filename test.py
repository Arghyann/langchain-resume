from supabase import create_client
from dotenv import load_dotenv
import os
import supabase
# Initialize the Supabase client
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

# Download a file from the 'resumes' bucket
file_name = "aditya-sangwan-1757090476495.pdf"
bucket_name = "resumes"

# Download the file
response = supabase.storage.from_(bucket_name).download(file_name)

# Save the file locally
with open(file_name, "wb") as f:
    f.write(response)