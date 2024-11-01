# Sales Development Representative Email Outreach System

## Purpose

The AI-Powered SDR Email Outreach System aims to enhance sales development processes by automating email generation and follow-up responses. Utilizing advanced AI technologies, it streamlines prospect research, improves communication efficiency, and increases engagement rates, ultimately driving better sales outcomes.

## Demo Video

<a href="https://www.youtube.com/watch?v=vSr9O0YUv3k" target="_blank">
  <img src="https://img.youtube.com/vi/vSr9O0YUv3k/maxresdefault.jpg" width="400" />
</a>


## Project Features

- **Technologies Used**: FastAPI, Streamlit, LLM, SQLite, SMTP, IMAP
- Integrated **Google Custom Search API** with **Sumy's LSA Summarizer** to generate prospect research reports from the web.
- Utilized **Gemini's GenAI API** to generate and review personalized email drafts, incorporating automated feedback and improvements.
- Implemented **SMTP** for sending emails and **IMAP** for monitoring replies, along with automated responses and SQLite storage.


## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- Required libraries (FastAPI, Streamlit, SQLite, etc.)

## Installation

### 1. Download and Extract the Compressed File
- Download the compressed file containing the project from the provided link.
- Extract the contents of the compressed file to a directory of your choice.

### 2. Navigate to the Project Directory
- Open a terminal or command prompt.
- Change to the directory where you extracted the files

```bash
cd <directory-of-extracted-files>
```

### 3. Create and Activate a Virtual Environment
- Create a virtual environment

```bash
python -m venv myenv
```

- Activate the virtual environment

```bash
venv\Scripts\activate
```

### 4. Install Required Libraries
- Install the necessary libraries using the requirements.txt file

```bash
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
- Create a file named .env in the root directory of the project.
- Add the following content to the .env file, replacing placeholders with your actual credentials
  
```makefile
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

## Running the System

### 1. Start the FastAPI Backend
- Run the FastAPI server.
```bash
uvicorn backend.main:app --reload
```
- The server will be accessible at http://127.0.0.1:8000.

### 2. Start the Streamlit Backend
- Run the Streamlit application.
```bash
streamlit run frontend/app.py
```
- The server will be accessible at http://127.0.0.1:8501.


## Usage

### 1. Prospect Research 
- Open the Streamlit UI.
- Enter prospect name and company name.
- Submit to generate a research report.
- Download the report in txt format.

### 2. Email Generation
- Upload the research report and your product catalog.
- Generate the personalized email draft.
- Download the email draft in txt format.

### 3. Email Review / Send Mail
- Select the subtask: 
  - Upload and Review Template
  - Send Email

### 3.1. Upload and Review Template
- Upload the draft email and sales/winning email templates in .txt format.
- Submit to receive review feedback and make adjustments as needed.
- If you'd like to apply the feedback to your email, click the "Apply Feedback" button and download the updated email in .txt format.
- Otherwise, you can skip directly to the Send Email subtask.
  
### 3.2. Send Email
- Enter the email subject and recipient email address.
- You can either paste the email in the text area 
- You can either paste the email into the text area, or upload the downloaded email in .txt format.
- Click "Send Email" button to send the email.

### 4. My Data
- Select the subtask: 
  - Prospect and Company Reports
  - Sent Email

### 4.1. Viewing Stored Prospect Reports
- Use the search bar to enter a prospect name or company name manually.
- After entering the search query, press Enter to display the relevant research report.
- The detailed report will include key information on the prospect and their company, gathered during the research phase.
- You can download the research report in .txt format for offline access.
  
### 4.2. Viewing Sent Mails
- Use the search bar to find specific sent emails by entering any of the following:
  - Recipient's email address
  - Content of the email
  - Date sent
- Press Enter to view the list of matching emails.

#### Note:
Replace placeholders like <directory-of-extracted-files> with the actual directory name. This plain text format provides clear, step-by-step instructions for setting up and running your system.
