import os
import openai
from dotenv import load_dotenv
import boto3

# Load API key from .env file


ssm = boto3.client("ssm", region_name="us-east-1")  

def get_ssm_parameter(name):
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]



# Initialize OpenAI API
openai.api_key = get_ssm_parameter("OPENAI_API_KEY")

def generate_project_idea(prompt):
    """Generates project ideas and planning suggestions using GPT-4."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert project planner helping users generate structured project ideas."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"
