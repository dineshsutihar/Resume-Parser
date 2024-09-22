import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Validate API Key
API_KEY = os.getenv('GOOGLE_API_KEY')
if not API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY is missing in the environment variables.")
genai.configure(api_key=API_KEY)

# Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

def ats_extractor(resume_data):
    """Extracts structured data from resume text using the Gemini model."""
    try:
        prompt = """
        You are an AI bot designed to parse resumes. Extract the following information from the resume in JSON format:
        - Full Name
        - Email ID
        - GitHub Portfolio
        - LinkedIn ID
        - Employment Details
        - Technical Skills
        - Soft Skills
        
        Resume Text:
        """
        final_prompt = f"{prompt}{resume_data}"

        # Generate AI response
        response = model.generate_content(final_prompt)
        return response.text.strip()

    except Exception as e:
        logging.error(f"Error generating AI response: {e}")
        raise
