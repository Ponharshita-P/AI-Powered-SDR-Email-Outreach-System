import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def generate_mail_template(prospect_name: str, prospect_info: str, sales_rep: str, sales_company_name: str, products_catalog: str):
    prompt = f"""
        You are writing a personalized sales email from {sales_rep}, a sales representative at {sales_company_name}, to {prospect_name}. Your goal is to craft an engaging email that highlights how our products can benefit the prospect, using value-based selling.

        COMPANY INFORMATION:
        {sales_company_name} is a DataScience company. We offer a wide range of premium products and tools including:
        - {products_catalog}

        PROSPECT INFORMATION:
        Based on our recent research, we know that:
        - {prospect_name}
        - {prospect_info}

        EMAIL REQUIREMENTS:
        - Provide a brief, 2-5 sentence description of the selected products, emphasizing their benefits.
        - End with a call-to-action, inviting the prospect to set up a time to talk more about how our products can meet their needs.
        - Provide only the mail template, with no extra messages and subject.

        % YOUR RESPONSE:
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error generating content: {e}")

