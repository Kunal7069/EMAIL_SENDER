import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Streamlit app title
st.title("Data Fetching App")

# Get user input
password = st.text_input("Password:")
recipient_email = st.text_input("Recipient Email:")
send_date = st.date_input("Select Date")
subject = "HII"
body ="DAY 2 CONCLUDED FINALLY TODAY"

# Gmail credentials (replace with your own)
sender_email = "teamryuks@gmail.com"
sender_password = "lokw ofym loze wupx"

# Function to send email
def send_email(recipient, subject, body):
    try:
        # Create the MIME object
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject

        # Attach the body to the email
        message.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            # Login to the sender's email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient, message.as_string())

        st.success("Email sent successfully!")

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Button to send email
if st.button("Get Data"):
    if password=="12345":
        send_email(recipient_email, subject, body)
    else:
        st.error("Wrong Password!")
