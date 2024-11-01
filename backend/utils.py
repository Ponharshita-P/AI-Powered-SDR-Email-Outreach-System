import sqlite3
import nltk
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

"""Read data from a text file and return it as a string."""
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            data.decode("utf-8")
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
def create_db(DATABASE_FILE):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        # Create the prospect information table with a UNIQUE constraint
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prospectinformation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT,
            prospect_name TEXT COLLATE NOCASE,
            company_name TEXT COLLATE NOCASE,
            report TEXT,
            UNIQUE(entry_date, prospect_name, company_name)
        )
        ''')

        # Create the sent emails table without uniqueness constraints
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sent_date TEXT,
            to_address TEXT COLLATE NOCASE,
            email_content TEXT COLLATE NOCASE,
            UNIQUE(sent_date, to_address)
        )
        ''')

        conn.commit()

def check_punkt_tokenizer():
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        print("Downloading NLTK tokenizer resources...")
        nltk.download('punkt_tab')

def initialize_summarizer(LANGUAGE):
    try:
        stemmer = Stemmer(LANGUAGE)
        summarizer = LsaSummarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)
        return summarizer
    except Exception as e:
        raise RuntimeError(f"Failed to load summarization model: {e}")