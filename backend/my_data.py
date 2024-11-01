import sqlite3
from pathlib import Path

# Project root
project_root = Path(__file__).resolve().parents[1]

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(project_root / "data" / "my_data.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_report_row(search_term: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = '''
            SELECT entry_date, prospect_name, company_name, report
            FROM prospectinformation
            WHERE LOWER(prospect_name) LIKE ? OR LOWER(company_name) LIKE ?
        '''
        params = (f'%{search_term.lower()}%', f'%{search_term.lower()}%')
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        reports = [dict(row) for row in rows]
        return reports
    except Exception as e:
        print(f"Error in getting stored report: {e}")

def get_sent_emails(search_term: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = '''
            SELECT sent_date, to_address, email_content
            FROM sent_emails
            WHERE to_address LIKE ? OR email_content LIKE ?
        '''
        params = (f'%{search_term}%', f'%{search_term}%')
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        sent_emails = [dict(row) for row in rows]
        return sent_emails
    except Exception as e:
        print(f"Error in getting sent mails: {e}")