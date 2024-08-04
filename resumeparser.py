import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Choose the appropriate model
model = genai.GenerativeModel('gemini-1.5-flash')

def ats_extractor(resume_data):
    prompt = '''
    You are an AI bot designed to act as a professional for parsing resumes. You are given with resume and your job is to extract the following information from the resume:
    1. full name
    2. email id
    3. github portfolio
    4. linkedin id
    5. employment details
    6. technical skills
    7. soft skills
    Give the extracted information from the given data in json format only. \n
    '''
    finalPrompt = prompt + resume_data
 

    # Generate the response using the Gemini AI model
    response = model.generate_content(finalPrompt)

    # Print and return the extracted data
    return response.text
