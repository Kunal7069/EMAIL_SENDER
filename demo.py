import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
from prettytable import PrettyTable
import re

# --------------------- Configuration ---------------------

# MongoDB Configuration (Hardcoded)
MONGODB_URI = "mongodb+srv://TEST:12345@mubustest.yfyj3.mongodb.net/investz?retryWrites=true&w=majority"
DATABASE_NAME = "NALCO"
COLLECTION_NAME = "NALCO"

# Email Configuration (Hardcoded)
SENDER_EMAIL = "2100520100135@ietlucknow.ac.in"
SENDER_PASSWORD = "sejf cdkr wari uvtl"  # Use an app-specific password if using Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # For TLS

# Email Subject
EMAIL_SUBJECT = "DATABASE BACKUP"

# --------------------- Helper Functions ---------------------

def is_valid_email(email):
    """
    Validates the format of the email address.
    """
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}\b'
    return re.match(regex, email)

def fetch_mongodb_data():
    """
    Connects to MongoDB, fetches data from the specified collection,
    and returns it as a list of dictionaries.
    """
    try:
        client = MongoClient(MONGODB_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        documents = list(collection.find())

        if not documents:
            st.warning("No data found in the MongoDB collection.")
            return None

        # Remove the MongoDB '_id' field for readability
        for doc in documents:
            doc.pop('_id', None)

        return documents

    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

def create_html_table(data):
    """
    Converts a list of dictionaries to an HTML table using PrettyTable.
    """
    if not data:
        return "<p>No data available to display.</p>"

    # Initialize PrettyTable with headers
    headers = data[0].keys()
    table = PrettyTable()
    table.field_names = headers

    # Add rows to the table
    for entry in data:
        row = [str(entry.get(field, "")) for field in headers]
        table.add_row(row)

    # Convert PrettyTable to HTML
    html_table = table.get_html_string(attributes={"border": "1", "style": "border-collapse: collapse; width: 100%;"})
    return html_table

def send_email(recipient, subject, html_content):
    """
    Composes and sends an email with the given HTML content.
    """
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the HTML content
        msg.attach(MIMEText(html_content, 'html'))

        # Connect to the SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"An error occurred while sending the email: {e}")

# --------------------- Streamlit App ---------------------

def main():
    # App Title
    st.title("MongoDB Data Fetch and Email Sender")

    st.markdown("""
    ### Get your data via email
    Enter your email address below and click *Send Data via Email* to receive the latest data from the Database collection.
    """)

    # Recipient Email Input
    recipient_email = st.text_input("Recipient Email:")

    # Send Email Button
    send_button = st.button("Send Data via Email")

    # --------------------- Main Logic ---------------------
    if send_button:
        if recipient_email:
            if is_valid_email(recipient_email):
                with st.spinner("Fetching data from MongoDB..."):
                    data = fetch_mongodb_data()

                if data:
                    with st.spinner("Creating email content..."):
                        html_table = create_html_table(data)

                    with st.spinner("Sending email..."):
                        send_email(recipient_email, EMAIL_SUBJECT, html_table)
            else:
                st.error("Please enter a valid email address.")
        else:
            st.error("Please enter a recipient email address.")

if __name__ == "__main__":
    main()
