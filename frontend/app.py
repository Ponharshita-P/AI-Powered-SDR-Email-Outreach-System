import streamlit as st
import requests

BASE_API_URL = "http://localhost:8000"
            
# Function to get the report and display the summary
def fetch_report():
    prospect_name = st.text_input("Prospect Name")
    company_name = st.text_input("Company Name")

    if st.button("Research"):
        if prospect_name and company_name:
            data = {
                "prospect_name": prospect_name,
                "prospect_company_name": company_name,
            }
            response = requests.post(
                f"{BASE_API_URL}/generate_report/", 
                json=data
            )
           
            if response.status_code == 200:
                result = response.json()
                st.write("Summary:")
                st.write(result["summary"])

                # Display download button
                st.download_button(
                    label="Download Report",
                    data=result["file_content"],
                    file_name=result["file_name"],
                    mime="text/plain"
                )
            else:
                st.error(f"Failed to generate report: {response.content}")     

    else:
        st.warning("Please provide both Prospect Name and Company Name.")

# Function to generate and get the email template
def generate_mail():
    # Form for uploading files and entering other details
    with st.form("mail_form"):
        sales_rep = st.text_input("Sales Rep Name")
        sales_company_name = st.text_input("Your Company Name")
        prospect_name = st.text_input("Prospect Name")
        
        prospect_info_file = st.file_uploader("Upload Prospect Info File", type=["txt"])
        products_catalog_file = st.file_uploader("Upload Product Catalog File", type=["txt"])

        submitted = st.form_submit_button("Generate Email")

    # Send to FastAPI when form is submitted
    if submitted:
        if prospect_info_file and products_catalog_file:
            
            data = {
                "prospect_name": prospect_name,
                "sales_rep": sales_rep,
                "sales_company_name": sales_company_name,
                "prospect_info_text": prospect_info_file.getvalue().decode('utf-8'),
                "products_catalog_text": products_catalog_file.getvalue().decode('utf-8')
            }
            
            # Send files and other data to FastAPI
            response = requests.post(
                f"{BASE_API_URL}/generate_mail_template/",
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                st.write("Generated Email:")
                st.write(result["mail"])

                # Display download button
                st.download_button(
                    label="Download Template",
                    data=result["file_content"],
                    file_name=result["file_name"],
                    mime="text/plain"
                )
            else:
                st.error(f"Failed to generate email: {response.content}")

        else:
            st.error("Please provide both Prospect Info and Product Catalog Files (In .txt Format).")


# Function to review, validate and send the email
def review_and_send_mail():
    # Sub-tabs within the "Review/Send Email" section
    sub_tab = st.sidebar.radio("Select a Tab", ["Get Feedback", "Send Email"])
    
    # 1st Sub-tab: Upload and Review Email Template
    if sub_tab == "Get Feedback":
        st.header("Get Feedback")

        # Use session state to store feedback
        if 'feedback' not in st.session_state:
            st.session_state['feedback'] = ""
        
        with st.form("review_form"):
            # Upload the generated email template
            uploaded_template = st.file_uploader("Upload Generated Email Template", type=["txt"])
            
            # Optional: Upload sales email template/winning email sample for comparison
            uploaded_sample = st.file_uploader("Upload Sales Email Template (Optional)", type=["txt"])
            
            if uploaded_template:
                # Display uploaded template
                template_content = uploaded_template.read().decode("utf-8")
                st.subheader("Generated Email Template:")
                st.text_area("Generated Template", template_content, height=200, key="generated_template")

                # Optional feedback based on uploaded sales email template
                if uploaded_sample:
                    sample_template_content = uploaded_sample.read().decode("utf-8")
                    st.subheader("Sales Email Template (Optional Review):")
                    st.text_area("Sales Email Sample", sample_template_content, height=200, key="sample_template")
            
            submitted = st.form_submit_button("Review Email")

            if submitted and not uploaded_template:
                st.warning("Please upload the generated email template for review.")
            elif submitted and uploaded_template:
                # Feedback Logic
                data = {
                    "template_content_text": uploaded_template.getvalue().decode('utf-8'),
                    "sample_content_text": uploaded_sample.getvalue().decode('utf-8') if uploaded_sample else ""
                }
                    
                # Send files and other data to FastAPI
                response = requests.post(
                    f"{BASE_API_URL}/review_mail_template/",
                    json=data
                )
                    
                if response.status_code == 200:
                    result = response.json()
                    st.session_state['feedback'] = result["feedback"]  # Store feedback in session state
                    st.text_area("Feedback", st.session_state['feedback'], height=100, key="feedback_text")
                else:
                    st.error(f"Failed to review email: {response.content}")
        
        # Button to apply feedback changes
        if st.button("Apply Feedback Changes"):
            if uploaded_template and st.session_state['feedback']:
                data = {
                    "feedback_content": st.session_state['feedback'],  # Get feedback from session state,
                    "template_content_text": uploaded_template.getvalue().decode('utf-8')
                }

                # Send files and other data to FastAPI
                response = requests.post(
                    f"{BASE_API_URL}/apply_feedback_changes/",
                    json=data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    modified_template = result["updated_mail"]
                    st.text_area("Updated Template", modified_template, height=200, key="updated_template")

                    # Option to download the updated template
                    st.download_button(
                        label="Download Updated Template",
                        data=result["file_content"],
                        file_name="updated_template.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Failed to make the feedback changes: {response.content}")
            else:
                st.warning("Please ensure feedback is available.")


    # 2nd Sub-tab: Send Email
    elif sub_tab == "Send Email":
        st.header("Send Email")

        # Text input for entering the subject
        subject = st.text_input("Subject", placeholder="Enter the email subject")

        # Text input for entering the 'To' address
        to_address = st.text_input("To Address", placeholder="Enter recipient's email address")

        # Upload or type the email content
        email_content = st.text_area("Email Template", placeholder="Upload or type the email content here",height=200)
        
        # Optionally allow users to upload an email content file instead of typing
        email_template_file = st.file_uploader("Upload Email Content (optional)", type=["txt"])
        if email_template_file:
            st.text_area("Email Content (Uploaded)", email_template_file.read().decode('utf-8'), height=200, key="uploaded_email_content")

        # Send Button
        if st.button("Send Email"):
            if not email_template_file and not email_content:
                st.error(f"Please enter the mail content or upload the mail template")

            # Taking the file content, if not given manually
            if not email_content or not email_content.strip():
                email_content = email_template_file.getvalue().decode('utf-8')

            if subject and to_address:
                # Call the send_email function
                data = {
                    "subject": subject,
                    "to_address": to_address,
                    "email_content_text": email_content,
                }
                
                # Send files and other data to FastAPI
                response = requests.post(
                    f"{BASE_API_URL}/send_email/",
                    json=data
                )

                if response.status_code == 200:
                    st.success("Email sent successfully!")
                else:
                    st.error("Failed to send the email.")
            else:
                st.warning("Please fill all required fields before sending the email.")

# Function to get saved prospect research report from the FastAPI backend
def get_report(prospect_name=None, company_name=None):
    params = {}
    params["search_term"] = prospect_name or company_name 
    response = requests.post(
        f"{BASE_API_URL}/report/", 
        json=params
        )
    if response.status_code == 200:
        report = response.json().get("reports", [])
        return report
    return None

# Function to get sent emails from the FastAPI backend
def get_sent_emails(search_term):
    response = requests.post(
        f"{BASE_API_URL}/sent_emails/", 
        json={"search_term": search_term}
        )
    if response.status_code == 200:
        sent_emails = response.json().get("sent_emails", [])
        return sent_emails
    return []

# Function to view the prospect info and sent mails
def my_data():
    tab = st.sidebar.radio("Select a Tab", ["Prospect and Company Reports", "Sent Mails"])

    if tab == "Prospect and Company Reports":
        st.header("Prospect and Company Reports")

        search_term = st.text_input("Search for a prospect or company:")

        if search_term:
            # Retrieve and display the report
            reports = []
            reports = get_report(prospect_name=search_term)
            if reports is None:
                reports = get_report(company_name=search_term)

            # Display results
            if reports:
                st.subheader("Reports:")
                for result in reports:
                    st.write(f"**Entry Date:** {result['entry_date']}")
                    st.write(f"**Prospect Name:** {result['prospect_name']}")
                    st.write(f"**Company Name:** {result['company_name']}")
                    st.write(f"**Report:**")
                    unique_key = f"{result['entry_date']}__{result['prospect_name']}"
                    st.text_area(
                        label="", 
                        value=result['report'], 
                        height=300, 
                        key=unique_key
                    )
                    # Option to save the report to a file
                    st.download_button(
                        label="Download Report",
                        data=result["report"],
                        file_name=f"{result['prospect_name']}_{result['entry_date']}.txt",
                        mime="text/plain"
                    )
                    st.write("---")
            else:
                st.warning("No report found for the entered name or company.")

    elif tab == "Sent Mails":
        st.header("Sent Mails")

        search_term = st.text_input("Search for sent emails by address or content:")

        if search_term:
            sent_emails = get_sent_emails(search_term)

            if sent_emails:
                st.subheader("Sent Emails:")
                for email in sent_emails:
                    st.write(f"**Date:** {email['sent_date']}")
                    st.write(f"**To Address:** {email['to_address']}")
                    st.write(f"**Content:**")
                    st.text_area("", email['email_content'], height=200, key=email['sent_date'])
                    st.write("---")
            else:
                st.warning("No sent emails found.")


# ******** Streamlit app layout ********
st.set_page_config(
    page_title="My SDR AI App",
    page_icon=":sparkles:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
    <style>
        .main-title {
            font-size: 45px;
            color: #C68FE6;
            text-align: center;
        }
    </style>
""", 
unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">AI-Powered Sales Development Representative</h1>', unsafe_allow_html=True)

# List of options
options = ["Prospect Research", "Email Generation", "Review/Send Email", "My Data"]

# Default tab
default_tab = "Prospect Research"

# Sidebar Radios
tabs = st.sidebar.radio("Choose a Option", ["Prospect Research", "Email Generation", "Review/Send Email", "My Data"], index=["Prospect Research", "Email Generation", "Review/Send Email", "My Data"].index(default_tab))

# Title Icons
icon_prospect = "🔍"
icon_email = "✉️"
icon_review = "📤"
icon_mydata = "📊"

if tabs == "Prospect Research":
    st.title(f"{icon_prospect} Prospect Research")
    fetch_report()
elif tabs == "Email Generation":
    st.title(f"{icon_email} Generate Sales Email")
    generate_mail()
elif tabs == "Review/Send Email":
    st.title(f"{icon_review} Review/Send Email")
    review_and_send_mail()
elif tabs == "My Data":
    st.title(f"{icon_mydata} My Data")
    my_data()

