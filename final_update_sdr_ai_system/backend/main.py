from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import sqlite3
from pathlib import Path
from datetime import datetime
import time
import threading

# Custom Modules
from . import utils
from . import research
from . import email_generation
from . import email_review
from . import email_sender
from . import my_data
from . import email_monitor

app = FastAPI()

# Initialize the Sumy summarizer once when the app starts
LANGUAGE = "english"
summarizer = utils.initialize_summarizer(LANGUAGE)

# Ensure that the punkt tokenizer is downloaded
utils.check_punkt_tokenizer()

# Project root
project_root = Path(__file__).resolve().parents[1]

# Database setup
try:
    DATABASE_FILE = project_root / "data" / "my_data.db"
    if not Path(DATABASE_FILE).exists():
        utils.create_db(DATABASE_FILE)
except Exception as e:
    raise Exception("Failed to create DB")

# Method to check the mail replies and to send an automated response
def run_email_checking(interval):
    while True:
        print("Checking emails...")
        email_monitor.check_mails_and_reply()
        print(f"Waiting {interval} seconds before next check...")
        time.sleep(interval)

# Run the email checking task in a background thread
@app.on_event("startup")
async def startup_event():
    thread = threading.Thread(target=run_email_checking, args=(300,))
    thread.start()

# Define the input structure for generating reports
class ProspectResearch(BaseModel):
    prospect_name: str
    prospect_company_name: str

@app.post("/generate_report/")
async def generate_report(info: ProspectResearch):
    try:
        # Generate report
        report_text = research.generate_report(info.prospect_name, info.prospect_company_name)
        
        # Summarize the report
        try:
            # Use Sumy summarizer to summarize the report text
            parser = PlaintextParser.from_string(report_text, Tokenizer(LANGUAGE))
            summary_sentences = summarizer(parser.document, 10)  # Summarize to 10 sentences

            # Combine summarized sentences
            summarized_text = ' '.join(str(sentence) for sentence in summary_sentences)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

        # Save the report to SQLite database
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO prospectinformation (entry_date, prospect_name, company_name, report)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(entry_date, prospect_name, company_name)
                    DO UPDATE SET 
                        report = excluded.report
                ''', (datetime.now().strftime("%Y-%m-%d"), info.prospect_name.lower(), info.prospect_company_name.lower(), summarized_text))
                conn.commit()
                print("Successfully inserted the Prospect Info record")
            except sqlite3.IntegrityError as e:
                print(f"Failed to insert record: {e}")

        # Save the report as a text file
        file_name = f"{info.prospect_name}_{info.prospect_company_name}_report.txt"
        file_content = summarized_text.encode('utf-8')  # Encode the summary to bytes for download
        
        return {
            "summary": summarized_text,
            "file_name": file_name,
            "file_content": file_content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Define the input structure for generating mail template
class GenerateMailTemplate(BaseModel):
    prospect_name: str
    sales_rep: str
    sales_company_name: str
    prospect_info_text: str
    products_catalog_text: str

@app.post("/generate_mail_template/")
async def generate_mail_template(info: GenerateMailTemplate):
    try:
        # Generate mail template
        mail_template = email_generation.generate_mail_template(info.prospect_name, info.prospect_info_text, info.sales_rep, info.sales_company_name, info.products_catalog_text)
        # Save the report as a text file
        file_name = f"{info.prospect_name}_{info.sales_company_name}_email_template.txt"
        file_content = mail_template.encode('utf-8')  # Encode the summary to bytes for download
        
        return {
            "mail": mail_template,
            "file_name": file_name,
            "file_content": file_content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Define the input structure for reviewing mail template
class ReviewMailTemplate(BaseModel):
    template_content_text: str
    sample_content_text: str

@app.post("/review_mail_template/")
async def review_mail_template(info: ReviewMailTemplate):
    try:
        # Review mail template
        feedback = email_review.review_mail_template(info.template_content_text, info.sample_content_text)
          
        return {
            "feedback": feedback
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the input structure for applying the feedback changes
class ApplyFeedbackChanges(BaseModel):
    feedback_content: str
    template_content_text: str

@app.post("/apply_feedback_changes/")
async def apply_feedback_changes(info: ApplyFeedbackChanges):
    try:
        # Apply feedback changes
        updated_mail_template = email_review.apply_feedback_changes(info.feedback_content, info.template_content_text)
        # Save the report as a text file
        file_name = "updated_email_template.txt"
        file_content = updated_mail_template.encode('utf-8')  # Encode the summary to bytes for download
        
        return {
            "updated_mail": updated_mail_template,
            "file_name": file_name,
            "file_content": file_content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define the input structure for Sending mail
class SendEmail(BaseModel):
    subject: str
    to_address: str
    email_content_text: str

@app.post("/send_email/")
async def send_email(info: SendEmail):
    try:
        # Send mail
        email_sender.send_email(info.subject, info.to_address, info.email_content_text)

        # Insert the sent email record
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO sent_emails (sent_date, to_address, email_content)
                    VALUES (?, ?, ?)
                    ON CONFLICT(sent_date, to_address)
                    DO UPDATE SET
                        email_content = excluded.email_content
                ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), info.to_address, info.email_content_text))
                conn.commit()
                print("Successfully inserted the mail record")
            except sqlite3.IntegrityError as e:
                print(f"Failed to insert record: {e}")
    
    except Exception as e:
        breakpoint()
        raise HTTPException(status_code=500, detail=str(e))

# Define the input structure for getting the stored report
class GetReport(BaseModel):
    search_term: str

@app.post("/report/")
async def get_report(info: GetReport):
    try:
        reports = my_data.get_report_row(info.search_term)
        return {"reports": reports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define the input structure for getting the stored report
class SentEmails(BaseModel):
    search_term: str

# Endpoint to get sent emails
@app.post("/sent_emails/")
async def get_sent_emails(info: SentEmails):
    try:
        sent_emails = my_data.get_sent_emails(info.search_term)
        return {"sent_emails": sent_emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

