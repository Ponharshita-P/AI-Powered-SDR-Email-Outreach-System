import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def review_mail_template(template_file_text: str, sample_template_text: str = None):
    if sample_template_text:
        prompt = f"""
            Please rate the personalisation, clarity, and effectiveness of the call-to-action in this sales email template using a scale of 1 to 10. Once it has been scored, compare it to other successful sales email, emphasising areas that need work and the best strategies from the most effective templates.

            Email Template: {template_file_text}

            Successfull/Winning Sales Email: {sample_template_text}

            Give detailed feedback on each element and make recommendations for improvements that can be implemented after comparing our sales email to those of other successful/winning sales email.

            Fill in the placeholder with actual values.
        """
    else:
        prompt = f"""
            Please rate the personalisation, clarity, and effectiveness of the call to action in this sales email template using a scale of 1 to 10. Give thorough input on every aspect and recommend particular changes that could improve the email's effectiveness and appeal.

            Email Template: {template_file_text}

            Provide doable recommendations to raise this email's overall efficiency.
        """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error generating feedback: {e}")

def apply_feedback_changes(feedback: str, template_content_text: str):
    prompt = f"""
        Please make the required changes to the email on the basis of the feedback, taking into account the following email template and the comments that have been provided. Implement the recommendations to improve call-to-action efficiency, individualisation, and clarity. Provide only the revised email template.

        Email Template: {template_content_text}

        Feedback: {feedback}

        Guidelines:
        - Utilise the input to adjust the email template, making sure that the modifications take the improvement suggestions into consideration.
        - Make sure the call-to-action is more effective, more personalised, and more clear.
        - Don't give any placeholders, use the actual data.
        - Provide only the revised email template with the recommended adjustments, with no extra messages and subject.

        Please make sure the updated email maintains its professionalism and clarity.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error generating feedback changes: {e}")